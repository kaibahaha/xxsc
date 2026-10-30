# FACTORY24-20261030 20261030-1132-R11 A — Independent audit

- Source job_id: `e5909f9386404880`.
- Last observed: RUNNING (not DONE).
- Git source/tests: GIT_PENDING; independent tests NOT_RUN, exit code N/A; score N/A; audit_job_id=NONE.
- WorkBuddy self-tests, if later provided, are only SELF_TEST, not independent verification.
- After code appears: inspect source/test files and SHA256 against MANIFEST, run `python3 -m unittest discover -s tests -v` in isolated environment, add >=10 independent adversarial counterexamples, inspect recovery/idempotence/clock/failure semantics; report file:line evidence, P0-P3 severity, score /100, actual exit code, commit SHA. If remote disk only, mark UNVERIFIED until independently accessible.
