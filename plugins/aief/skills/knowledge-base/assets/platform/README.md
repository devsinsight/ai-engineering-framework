# Platform assets

Tested, deterministic pieces for the Tier 2 platform. Copy them **as they are** into the project's repository; generate the rest following [../../references/platform.md](../../references/platform.md). Changing one of these files in a project means the asset is wrong or incomplete: propose the fix here instead of diverging.

| File | Copy to | What it gives |
| --- | --- | --- |
| `contract.py` | `packages/core/src/aief_core/domain/contract.py` | Contract v2 dataclasses; `normalize()` with the missing-metadata policy; deterministic `point_id()` (artifact, source version, heading path, position); `content_hash()`; chunk payload and embedding text |
| `test_contract.py` | `packages/core/tests/test_contract.py` (change the import to `aief_core.domain.contract`) | The behavior the framework requires of the contract |
| `importlinter.toml` | Workspace root `pyproject.toml` | Hexagonal layer contracts |

The first assets encode framework rules directly (the contract, identities, metadata policy and layer contracts) and are tested here. Rule for adding more (ADR-008): only pieces that ran in a real project, are deterministic, use as few dependencies as possible, and come with tests.

Verify the assets from this folder with:

```
uv run --python 3.12 --with pytest pytest -q
```
