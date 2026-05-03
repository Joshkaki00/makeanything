Run through this checklist before merging any code that touches an external package, API, or service. Work through each item in order. Stop and fix before continuing if anything fails.

---

## Verification Checklist

**Tests**
- [ ] Run `pytest` or `npm test` — confirm exit code 0 and no skipped tests hiding failures

**Linter**
- [ ] Run `ruff check .` or `eslint .` — no new errors introduced

**Imports and packages**
- [ ] Every imported package exists on PyPI / npm (check with `pip show <pkg>` or `npm info <pkg>`)
- [ ] Every called method or function actually exists in that package's installed version — look at the source or docs, not the agent's description

**External APIs and endpoints**
- [ ] Every API endpoint the code calls actually exists — verify against live documentation
- [ ] HTTP methods match what the API expects (GET vs POST vs PUT)
- [ ] Required headers, auth tokens, and query params are correct

**Behavior**
- [ ] Run the code with real inputs — not just the happy path
- [ ] Test at least one edge case: empty input, null/None, zero, or large data
- [ ] Output matches the spec — not just "seems reasonable"

**Safety**
- [ ] No secrets, API keys, or passwords hardcoded in source files
- [ ] No `console.log`, `print()`, or debug statements left in production paths

---

Report which items passed and which failed. Do not skip any item.
