# Verification

Passed:

```bash
python3 -m unittest tests.test_wily_cli
```

Result: 31 tests OK, 1 skipped.

```bash
python3 -m unittest discover
```

Result: 101 tests OK, 2 skipped.

```bash
python3 -m py_compile scripts/wily.py
```

Result: exit 0.

Manual mature repo smoke:

```bash
python3 /Users/wilycastle/Code/projects/wily-roadmap/scripts/wily.py init
```

Result in `/private/tmp/wily-06-4-mature-smoke`: printed `Existing project hints: README.md, scripts/, tests/`.
