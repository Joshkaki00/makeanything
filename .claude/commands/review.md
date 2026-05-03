Review the current changes. Focus on correctness and boundaries — agents handle the happy path, so look hardest at the edges.

---

## Review Checklist

**Boundaries and edge cases**
- Empty input, empty list, empty string
- `null` / `None` / `undefined` values
- Zero, negative numbers, off-by-one
- Maximum values, very large inputs
- Concurrent access to shared state

**External references**
- Every imported package exists and is installed
- Every called method exists in that package's API — check the actual source or docs
- API endpoints match the live documentation (method, path, params)

**Error handling**
- No empty `catch {}` or `except: pass` blocks silently swallowing exceptions
- Errors are logged or re-raised with context — not just caught and dropped
- HTTP errors are checked (status codes, not just whether the call returns)

**Async correctness**
- Every `async` function call is properly awaited
- No `Promise` values being used as if they were resolved data

**Test coverage**
- There is at least one test for each function
- At least one test covers a non-happy-path input

**Spec match**
- The implementation does what the spec asked — not what seemed like a reasonable interpretation

---

For each issue: state the file name, approximate line, and what specifically is wrong or missing. Do not just say "looks good" — explain what you checked.
