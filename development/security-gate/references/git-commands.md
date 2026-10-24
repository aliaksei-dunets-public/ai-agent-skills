# Exact Scope and Safe Git Inspection

Run from the verified project root in the native shell. The examples show
argument structure; quote paths and refs, and use `-z` when parsing filename
lists. Resolve refs to commit SHAs with
`git rev-parse --verify --end-of-options <ref>^{commit}` before using them. All
commands are read-only; do not fetch, initialize submodules, stash, checkout,
reset, stage, or commit as part of review.

Content commands can reveal secrets: search with the location-only forms in
[leak-patterns](leak-patterns.md) and read secret-bearing lines only masked.
Keep `--no-ext-diff --no-textconv` on diffs so repository attributes cannot run
programs during inspection.

## Common Inventory

```text
git rev-parse --show-toplevel
git status --porcelain=v1 -z
git rev-parse --verify HEAD
git ls-files --unmerged -z
git ls-files --stage -z
```

HEAD may not exist in a new repository; an unborn HEAD is not an empty index.
Unmerged index entries prevent a trustworthy staged snapshot: report WARN for
the unresolved paths, continue with the rest, and do not choose a conflict side.
Inventory symlinks and gitlinks; do not follow paths outside the root.

## Staged (Default)

```text
git diff --cached --no-ext-diff --no-textconv --name-status --find-renames -z
git diff --cached --no-ext-diff --no-textconv --find-renames --unified=40 -- .
git show :path/to/file
```

The cached diff works before the first commit. Read stage-0 blobs from the
index (`:path`), including unchanged callers, middleware, manifests, and
lockfiles needed for context, and use index line numbers in findings. Never
substitute the working copy: partial staging can hold vulnerable code in the
index and a fixed version on disk at the same time.

If no staged changes exist, return WARN: nothing staged, no commit content
assessed. Mention unstaged and untracked files as excluded; do not review them
or expand to full mode automatically. A deletion-only change is not empty:
removing a guard or secure configuration can expose unchanged code. Renames can
affect loading, routes, publication rules, or permissions.

## Working Tree

```text
git diff HEAD --no-ext-diff --no-textconv --name-status --find-renames -z
git diff HEAD --no-ext-diff --no-textconv --find-renames --unified=40 -- .
git ls-files --others --exclude-standard -z
```

Covers staged and unstaged changes plus non-ignored untracked files. With an
unborn HEAD, treat the index inventory and untracked files as additions. Read
the current file bytes; separately disclose staged content that differs from
the inspected current version. Missing files are deletions, not read errors.

## Full

```text
git ls-files --cached --others --exclude-standard -z
```

Deduplicate names and read the current files of every component, unchanged
tracked and non-ignored untracked files alike, regardless of staged content.
Only current contents are assessed. Without Git, enumerate the selected
directory with a file listing, report that change attribution is unavailable,
and do not follow external symlinks.

## History Secrets

```text
git rev-parse --is-shallow-repository
git for-each-ref --format='%(refname)' refs/heads refs/tags refs/remotes
git log <refs> -G '<pattern>' --format=%H --name-only
```

Search the refs the user selected; when the request just says "history", use
all local branches and tags (`--branches --tags`) and say so. Remote-tracking
refs are local copies and are included only when requested; nothing is fetched.
Reflog, stashes, and unreachable objects are excluded unless requested. Report
a shallow clone as a coverage limit.

For each matched commit and path, confirm and locate the line with the
location-only `git grep` at that SHA, then record the commit, path, whether the
value still exists in current files, and which selected refs contain the commit
(`git branch --contains <sha>`, `git tag --contains <sha>`). A credential
removed from current files still exists in history. Rewriting history is a
separate request, never part of review.

## Exclusions and Publication Boundaries

- Never read `.git` as ordinary files.
- Dependency caches and build outputs can be excluded from routine source
  review; record the exclusion. Tracked, generated, or vendored files destined
  for publication still need leak review: "generated" is not an exemption.
- Ignored `.env` files are not staged changes. Check ignore and packaging rules
  for accidental inclusion; if that requires looking at an ignored file, search
  it location-only, label it outside Git scope, and never print its values.
- A changed gitlink needs review at the recorded submodule commit when it is
  available locally; otherwise report a gap. Do not assume the checked-out
  submodule matches the pointer.
- Missing Git LFS objects, unreadable files, binaries, sparse checkouts, and
  external symlink targets limit coverage. Report them instead of calling
  pointer files or missing content clean.
- Recheck status and relevant blob IDs before reporting. If files or the index
  changed during the review, recheck affected paths or return WARN.
