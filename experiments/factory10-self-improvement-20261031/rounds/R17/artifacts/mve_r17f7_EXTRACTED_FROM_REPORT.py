#!/usr/bin/env python3
# R17 F7 MVE (read-only, standard-library only). No network, no git, no writes outside cwd.
# Implements: T1 source/authorship admission gate; D1 DOI/retraction chain;
# D3 statistical hypothesis gate; Case-D unit conversion. Fail-closed by design.
import sys, os, json, hashlib, math, re, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))

ALLOWED_BASE_DOMAINS = {
    "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov",
    "pubs.usgs.gov", "crossref.org", "openalex.org", "arxiv.org",
    "ncbi.nlm.nih.gov", "rdkit.org", "doi.org",
}
FAKE_DOI_DENYLIST = {"10.1234/fake.2026.99999"}
DOI_RE = re.compile(r'^10\.\d{4,9}/.+$')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


# ---------------- T1: source / authorship admission gate ----------------
def classify_source(source_url):
    if not source_url or not isinstance(source_url, str):
        return (False, "EMPTY_OR_NONSTRING_URL", None)
    try:
        parts = urllib.parse.urlparse(source_url)
    except Exception:
        return (False, "URLPARSE_ERROR", None)
    scheme = (parts.scheme or "").lower()
    if scheme != "https":
        return (False, "SCHEME_NOT_HTTPS", {"scheme": scheme})
    if parts.username is not None or parts.password is not None:
        return (False, "USERINFO_PRESENT", None)
    hostname = (parts.hostname or "").lower()
    if not hostname:
        return (False, "NO_HOSTNAME", None)
    port = parts.port
    if port is not None and port != 443:
        return (False, "NONSTANDARD_PORT", {"port": port})
    ok_host = any(hostname == b or hostname.endswith("." + b) for b in ALLOWED_BASE_DOMAINS)
    if not ok_host:
        return (False, "HOST_NOT_ALLOWED", {"hostname": hostname})
    return (True, "HOST_OK", {"hostname": hostname, "scheme": scheme, "port": port})


def validate_doi(doi):
    if doi is None:
        return (True, "NO_DOI")
    if not isinstance(doi, str):
        return (False, "DOI_NOT_STRING")
    d = doi.strip()
    if d in FAKE_DOI_DENYLIST:
        return (False, "DOI_KNOWN_FAKE")
    if not DOI_RE.match(d):
        return (False, "DOI_FORMAT_INVALID")
    return (True, "DOI_FORMAT_OK")


def review_claim(claim):
    assertion = claim.get("assertion")
    if not assertion or not str(assertion).strip():
        return {"decision": "BLOCK", "reasons": ["EMPTY_ASSERTION"]}
    ok, reason, info = classify_source(claim.get("source_url"))
    if not ok:
        return {"decision": "BLOCK", "reasons": ["SOURCE_" + reason]}
    rights = claim.get("rights")
    license_evidence = claim.get("license_evidence")
    authorized = claim.get("authorized")  # explicitly NOT trusted
    if rights == "copyright_restricted":
        if not license_evidence or len(str(license_evidence).strip()) < 8:
            return {"decision": "REVIEW", "reasons": ["COPYRIGHT_NO_EVIDENCE", "authorized_flag_ignored"]}
        if not claim.get("human_approved"):
            return {"decision": "REVIEW", "reasons": ["COPYRIGHT_NEEDS_HUMAN_APPROVAL", "authorized_flag_ignored"]}
    doi_ok, doi_reason = validate_doi(claim.get("doi"))
    if not doi_ok:
        return {"decision": "BLOCK", "reasons": ["DOI_" + doi_reason]}
    retraction = claim.get("retraction")
    if retraction is not None:
        if not isinstance(retraction, dict):
            return {"decision": "BLOCK", "reasons": ["RETRACTION_MALFORMED"]}
        rel = retraction.get("authority_id") or retraction.get("relation")
        if not rel:
            return {"decision": "BLOCK", "reasons": ["RETRACTION_NO_AUTHORITY"]}
    return {"decision": "ADMIT", "reasons": ["ALL_CHECKS_PASSED"]}


# ---------------- D3: statistical hypothesis gate ----------------
def poisson_sf(k, lam):
    if lam < 0:
        return None
    if k <= 0:
        return 1.0
    logp = -lam + k * math.log(lam) - math.lgamma(k + 1)
    total = math.exp(logp)
    i = k
    while True:
        i += 1
        logp += math.log(lam) - math.log(i)
        term = math.exp(logp)
        total += term
        if term < total * 1e-18 or i > k + 100000:
            break
    return total


def _num(v):
    if isinstance(v, str):
        if v.upper() == "NAN":
            return float('nan')
        if v.upper() == "INF":
            return float('inf')
        try:
            return float(v)
        except Exception:
            return None
    return v


def poisson_significance(spec):
    obs = spec.get("obs"); lam_h0 = spec.get("lam_h0"); lam_h1 = spec.get("lam_h1")
    unit = spec.get("unit"); seed = spec.get("seed"); method = spec.get("method", "exact")
    if unit is None or not isinstance(unit, str) or unit.strip() == "":
        return {"status": "REJECT", "reason": "UNIT_MISSING"}
    if unit.strip().lower() not in ("counts", "events", "n"):
        return {"status": "REJECT", "reason": "UNIT_UNSUPPORTED", "unit": unit}
    obs = _num(obs); lam_h0 = _num(lam_h0); lam_h1 = _num(lam_h1)
    if obs is None or lam_h0 is None or lam_h1 is None:
        return {"status": "REJECT", "reason": "NON_NUMERIC_INPUT"}
    for name, val in (("obs", obs), ("lam_h0", lam_h0), ("lam_h1", lam_h1)):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return {"status": "REJECT", "reason": name.upper() + "_NAN_INF"}
    if lam_h0 < 0 or lam_h1 < 0:
        return {"status": "REJECT", "reason": "NEGATIVE_RATE"}
    if obs < 0:
        return {"status": "REJECT", "reason": "NEGATIVE_OBSERVATION"}
    if method == "mc" and seed is None:
        return {"status": "REJECT", "reason": "MC_MISSING_SEED"}
    if not float(obs).is_integer():
        return {"status": "REJECT", "reason": "OBS_NOT_INTEGER"}
    p_h0 = poisson_sf(int(obs), lam_h0)
    p_h1 = poisson_sf(int(obs), lam_h1)
    return {"status": "OK", "obs": int(obs), "lam_h0": lam_h0, "lam_h1": lam_h1,
            "p_value_h0_right_tail": p_h0, "p_value_h1_right_tail": p_h1,
            "h0": "background_only", "h1": "signal_plus_background",
            "tail": "right", "unit": unit, "note": "TOY_SIM_not_IceCube_calibrated"}


# ---------------- Case D: unit conversion ----------------
def convert_units(qty, frm, to):
    factors = {("eV", "J"): 1.602176634e-19, ("A", "nm"): 0.1}
    if (frm, to) in factors:
        return qty * factors[(frm, to)]
    if (to, frm) in factors:
        return qty / factors[(to, frm)]
    return None


def unit_check(spec):
    qty = spec.get("qty"); frm = spec.get("from"); to = spec.get("to")
    if qty is None or frm is None or to is None:
        return {"status": "REJECT", "reason": "MISSING_FIELD"}
    try:
        q = float(qty)
    except Exception:
        return {"status": "REJECT", "reason": "QTY_NOT_NUMERIC"}
    if math.isnan(q) or math.isinf(q):
        return {"status": "REJECT", "reason": "QTY_NAN_INF"}
    res = convert_units(q, frm, to)
    if res is None:
        return {"status": "REJECT", "reason": "UNSUPPORTED_UNIT_PAIR", "from": frm, "to": to}
    return {"status": "OK", "value": res, "from": frm, "to": to}


# ---------------- harness ----------------
def check(cond, msg):
    if not cond:
        print("CHECK FAILED: " + msg, file=sys.stderr)
        sys.exit(1)


def main():
    out = []
    log = out.append
    t1 = json.load(open(os.path.join(ROOT, "t1_claims.json")))
    d1 = json.load(open(os.path.join(ROOT, "d1_dois.json")))
    d3 = json.load(open(os.path.join(ROOT, "d3_inputs.json")))
    units = json.load(open(os.path.join(ROOT, "units.json")))
    log("=== T1 SOURCE/AUTHORSHIP ADMISSION GATE ===")
    for c in t1:
        r = review_claim(c)
        log("[%s] expect=%s got=%s reasons=%s" % (c["id"], c["expect"], r["decision"], r["reasons"]))
        if c["expect"] == "ADMIT":
            check(r["decision"] == "ADMIT", "%s expected ADMIT got %s" % (c["id"], r["decision"]))
        else:
            check(r["decision"] != "ADMIT", "FAIL-OPEN %s expected %s but ADMIT" % (c["id"], c["expect"]))
            check(r["decision"] == c["expect"], "%s expected %s got %s" % (c["id"], c["expect"], r["decision"]))
    log("T1 fail-open count = 0 (all negative cases non-ADMIT)")
    log("")
    log("=== D1 DOI / RETRACTION FROZEN SAMPLES ===")
    real = next(d for d in d1 if d["role"] == "REAL_PUBLISHED")
    rt = next(d for d in d1 if d["role"] == "RETRACTION_NOTICE")
    fake = next(d for d in d1 if d["role"] == "FAKE_DOI")
    for d in d1:
        log("[%s] doi=%s status=%s src=%s" % (d["role"], d["doi"], d["status"], d.get("source", "")))
    log("REAL published DOI=%s (Wolfe-Simon 2010, PMID %s)" % (real["doi"], real["pmid"]))
    log("RETRACTION notice DOI=%s date=%s (retracts %s)" % (rt["doi"], rt["date"], real["doi"]))
    log("FAKE DOI (frozen, never replaced)=%s status=%s" % (fake["doi"], fake["status"]))
    gate_fake = review_claim({"assertion": "x",
                              "source_url": "https://pubmed.ncbi.nlm.nih.gov/" + real["pmid"] + "/",
                              "rights": "open", "doi": fake["doi"]})
    check(gate_fake["decision"] == "BLOCK", "fake DOI must BLOCK in admission gate")
    log("Gate on fake DOI -> %s %s" % (gate_fake["decision"], gate_fake["reasons"]))
    gate_retract_ok = review_claim({"assertion": "Paper retracted 2025-07-24.",
                                    "source_url": "https://www.science.org/doi/" + rt["doi"],
                                    "rights": "open", "doi": real["doi"],
                                    "retraction": {"authority_id": rt["doi"],
                                                   "relation": "retracts:" + real["doi"]}})
    log("Gate on retraction-with-authority -> %s %s" % (gate_retract_ok["decision"], gate_retract_ok["reasons"]))
    log("")
    log("=== D3 STATISTICAL HYPOTHESIS GATE ===")
    for s in d3:
        r = poisson_significance(s)
        meta = {k: v for k, v in r.items() if k != "status"}
        log("[%s] expect=%s status=%s %s" % (s["id"], s["expect"], r["status"], meta))
        if s["expect"] == "OK":
            check(r["status"] == "OK", "%s expected OK got %s" % (s["id"], r["status"]))
            if "p_value_h0_right_tail" in r:
                log("   p(H0 lam=%s)=%.10f  p(H1 lam=%s)=%.10f" %
                    (r["lam_h0"], r["p_value_h0_right_tail"], r["lam_h1"], r["p_value_h1_right_tail"]))
        else:
            check(r["status"] == "REJECT", "%s expected REJECT got %s" % (s["id"], r["status"]))
    p_h0_5 = poisson_sf(14, 5)
    p_h1_8 = poisson_sf(14, 8)
    log("DEMO obs=14: H0 lam=5 -> p=%.10f ; H1 lam=8 -> p=%.10f" % (p_h0_5, p_h1_8))
    log("  Mixing H0=5 (p~0.0007) with H1=8 (p~0.0357) is the R07 D3 hypothesis-confusion error.")
    log("")
    log("=== CASE D: MATERIALS UNIT CONVERSION (stdlib frozen) ===")
    for u in units:
        r = unit_check(u)
        meta = {k: v for k, v in r.items() if k != "status"}
        log("[%s] %s%s->%s expect=%s status=%s %s" %
            (u["id"], u.get("qty"), u.get("from"), u.get("to"), u["expect"], r["status"], meta))
        if u["expect"] == "OK":
            check(r["status"] == "OK", "%s expected OK got %s" % (u["id"], r["status"]))
        else:
            check(r["status"] == "REJECT", "%s expected REJECT got %s" % (u["id"], r["status"]))
    log("")
    log("=== BYTE INTEGRITY (D2) ===")
    for fn in ["mve_r17f7.py", "t1_claims.json", "d1_dois.json", "d3_inputs.json", "units.json"]:
        log("SHA256 %s = %s" % (fn, sha256_file(os.path.join(ROOT, fn))))
    log("PYTHON=%s OPTIMIZE=%s" % (sys.version.split()[0], sys.flags.optimize))
    log("NOTE: source file ends with a single trailing newline; JSON files are UTF-8.")
    sys.stdout.write("\n".join(out) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
