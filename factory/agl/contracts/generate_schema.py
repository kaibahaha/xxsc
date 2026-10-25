"""Generate the structural JSON Schema from the frozen Python dataclasses.

Run: python -m factory.agl.contracts.generate_schema
Semantic authorization, DAG, fencing and runtime evidence checks live in the core.
"""
from dataclasses import MISSING, fields
from pathlib import Path
import json
import types
from typing import Any, get_args, get_origin, get_type_hints
from .. import schemas

NAMES = ("AgentRegistration", "ProviderSession", "TaskSpec", "ClaimProposal", "LeaseGrant",
         "StateTransition", "ArtifactEvidence", "Event", "Ack", "MemoryNote", "Handoff")


def annotation_schema(annotation):
    origin, args = get_origin(annotation), get_args(annotation)
    if origin is types.UnionType:
        return {"anyOf": [annotation_schema(a) for a in args]}
    if origin in (list, tuple):
        return {"type": "array", "items": annotation_schema(args[0])}
    if annotation is Any: return {}
    return {"type": {str: "string", int: "integer", float: "number", bool: "boolean", dict: "object", type(None): "null"}[annotation]}


def schema():
    definitions = {}
    for name in NAMES:
        cls = getattr(schemas, name)
        hints = get_type_hints(cls)
        properties = {f.name: annotation_schema(hints[f.name]) for f in fields(cls)}
        properties["schema_version"] = {"const": schemas.SCHEMA_VERSION}
        definitions[name] = {"type": "object", "additionalProperties": False, "properties": properties,
            "required": [f.name for f in fields(cls) if f.default is MISSING and f.default_factory is MISSING]}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "urn:agl:core:r01:2.0",
            "$defs": definitions, "oneOf": [{"$ref": f"#/$defs/{name}"} for name in NAMES]}


if __name__ == "__main__":
    Path(__file__).with_name("core.schema.json").write_text(json.dumps(schema(), indent=2) + "\n")
