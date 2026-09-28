# Exact Scope and Safe Git Inspection

Run from the verified project root using the native shell and argument-safe paths. The examples show argument structure, not commands to paste with untrusted placeholders. Use separate arguments in a process API for paths/refs and `-z` when parsing filename lists. Resolve refs to commit SHAs before constructing comparisons. Do not fetch, initialize submodules, stash, checkout, reset, stage, or commit as part of review.

Content commands below can reveal secrets. Capture their output locally and sanitize before returning excerpts through tools/chat. Disable external diff and text-conversion drivers; repository attributes must not execute programs during inspection. Avoid filters when materializing snapshots.

## Common Inventory

```text
git rev-parse --show-toplevel
git status --porcelain=v1 -z
git rev-parse --verify HEAD
git ls-files --unmerged -z
git ls-files --stage -z
```

HEAD may not exist in a new repository. An unborn HEAD is not an empty index. Unmerged index entries prevent a trustworthy staged snapshot: report WARN for the unresolved scope, continue independent inspection, and do not choose a conflict side silently. Inventory symlinks and gitlinks; do not follow paths outside the root.

## Staged (Default)

```text
git diff --cached --no-ext-diff --no-textconv --name-status --find-renames -z
git diff --cached --no-ext-diff --no-textconv --find-renames --unified=40 -- .
git show :path/to/file
```

The cached diff works before the first commit. Read stage-0 blobs from the index (`:path` or blob IDs from `ls-files --stage`), including unchanged callers, middleware, scanner rules, manifests, and lockfiles needed for context. Use index line numbers in findings. Never substitute the working copy: partial staging can contain vulnerable code and a fixed on-disk version simultaneously.

For tools that require a directory, use a private temporary snapshot outside the repository. Read index blob bytes with `git cat-file blob <object-id>` and materialize regular files with a trusted filesystem helper; preserve relative paths, validate containment, and omit symlinks/gitlinks with explicit coverage notes. Do not use checkout-based export helpers that can invoke smudge filters. A full index export may be needed for context even when reportable findings are limited to changes. If a faithful snapshot cannot be scanned, report partial coverage; do not label a filesystem scan as staged.

If no staged changes exist, return WARN: nothing staged, no commit content assessed. Mention unstaged/untracked files as excluded; do not scan them or expand to project mode automatically. A deletion-only change is not empty: removing a guard or secure configuration can expose unchanged code. Renames may affect loading, routes, publication rules, or permissions.

## Working Tree

```text
git diff HEAD --no-ext-diff --no-textconv --name-status --find-renames -z
git diff HEAD --no-ext-diff --no-textconv --find-renames --unified=40 -- .
git ls-files --others --exclude-standard -z
```

This mode includes all local staged and unstaged changes plus non-ignored untracked files. If HEAD is unborn, use the index inventory and current untracked files as additions instead. Read the current file bytes; separately disclose staged differences that would make the next commit differ from the inspected current version. Missing files are deletions, not read errors.

## Commit

Resolve the user ref safely with `git rev-parse --verify --end-of-options <ref>^{commit}`. Use the resulting SHA:

```text
git diff-tree --root --no-commit-id --name-status -r -z <sha>
git show --format= --no-ext-diff --no-textconv --find-renames --unified=40 <sha> -- .
git ls-tree -r -z <sha>
git show <sha>:path/to/file
```

For a merge, explicitly compare its first parent to the merge commit unless requested otherwise; combined diff can omit changes relative to a parent. For a root commit, compare to the empty tree using `diff-tree --root`. Scanner input and context come from the selected commit, not HEAD. Use raw tree blob reads for any temporary export.

## Range / Pull Request

For a PR, resolve base and target, then `git merge-base <base-sha> <target-sha>`; compare the result to the target. For an explicit endpoint comparison, use the supplied endpoints and say so.

```text
git diff --no-ext-diff --no-textconv --name-status --find-renames -z <base-sha> <target-sha>
git diff --no-ext-diff --no-textconv --find-renames --unified=40 <base-sha> <target-sha> -- .
```

Read context at the target SHA. If a trusted base is unknown or unavailable (including shallow history), disclose the gap instead of inventing origin/main or an empty baseline.

## Initial / Full / Project / No Git

```text
git ls-files --cached --others --exclude-standard -z
```

Deduplicate file names and read existing current files. Initial is an alias of full: inventory and review every project component, including unchanged tracked files and non-ignored untracked files, regardless of staged content. In project mode additionally inspect the staged changes and index context as above. In initial/full mode only current contents are assessed. Without Git, enumerate the explicitly selected project directory with a filesystem tool; report that change attribution is unavailable and do not silently follow external symlinks. For a Git-only mode without Git, return WARN and explain that initial/full mode can be requested.

## History Secrets

Use the history scanner guidance in tooling.md. State selected refs/range and shallow-clone limitations. A credential removed from current files may still exist in history. History scanning is explicit, not part of staged/full by default.

## Exclusions and Publication Boundaries

- Never scan `.git` as ordinary files. Keep history analysis separate.
- Dependency caches and build outputs can be excluded from routine source review, but record exclusions. Tracked/generated/vendored files destined for publication still need secret and relevant supply-chain review; “generated” is not a security exemption.
- Ignored `.env` files are not staged changes. Inspect ignore/build/publish rules for accidental packaging; if a potential inclusion requires examining an ignored file, narrowly inspect it with redaction as context and label it outside Git scope.
- Changed gitlinks require review at the recorded submodule commit when locally available; otherwise report a gap. Do not silently assume the checked-out submodule matches the pointer.
- Missing Git LFS objects, unreadable files, unsupported binaries, sparse checkouts, or external symlink targets limit coverage. Report them instead of calling pointer files or missing content clean.
- Recheck status and relevant blob IDs before reporting. If files/index changed during the scan, identify stale results and recheck affected paths or return WARN.
