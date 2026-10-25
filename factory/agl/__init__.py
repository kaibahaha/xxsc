"""Agensh-Lite V4.2 adapter plane.

Modules owned by WorkBuddy in workorder AGL-WB-ADAPTERS-R01:

* ``agl.storage``   -- M02 GitHub Storage Adapter (immutable writes, readback, CAS)
* ``agl.adapters``  -- M06 provider adapters + registry view + admission gate
* ``agl.poll``      -- M06 dynamic poll / per-provider scheduling
* ``agl.execution`` -- M08 executor bridge (TEST_REQUEST/TEST_RESULT/ACK)
* ``agl.cli``       -- M10 command line entry points

Codex owns M01/M03/M04/M05/M07/M09 (config/schemas/events/controller/leases/
memory/handoff/audit). This package never re-implements those modules; where a
core capability is absent it degrades to an explicitly labelled reduced mode
(``PENDING_CORE`` / ``CONTROLLER_UNAVAILABLE``) instead of inventing a second
incompatible implementation.
"""

__version__ = "4.2.0r1"
SCHEMA_VERSION = "1.0"
