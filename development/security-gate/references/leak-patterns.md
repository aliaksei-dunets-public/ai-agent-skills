# Leak Patterns

Apply every class below to the snapshot of the selected mode. The patterns are
POSIX extended regular expressions for `git grep -E`; they find candidates, not
proof. Token formats change and the list is not exhaustive: also judge
unfamiliar high-entropy values assigned to sensitive names.

## Search without printing values

Search output must contain locations only. Strip the matched text before it
reaches the tool output; never print `-o` matches, context lines, or whole
lines. Always pass the pattern with `-e`: a pattern starting with `-` is
otherwise read as an option.

- staged: `git grep --cached -I -n -E -e '<pattern>' | cut -d: -f1,2`
- working-tree, full: `git grep --untracked -I -n -E -e '<pattern>' | cut -d: -f1,2`
- full without Git: `grep -rnIE --exclude-dir=.git -e '<pattern>' . | cut -d: -f1,2`
- history-secrets: `git log <refs> -G '<pattern>' --format=%H --name-only`
  lists commits and files; then
  `git grep -I -n -E -e '<pattern>' <sha> -- <path> | cut -d: -f1-3`.

Add `-i` for the case-insensitive classes. Limit working-tree searches to the
changed paths after `--`; full searches the whole tree. In PowerShell replace
`cut` with `ForEach-Object { ($_ -split ':')[0..1] -join ':' }` (`[0..2]` for
the history form). Without Git on Windows use
`Select-String -Path <files> -Pattern '<pattern>' | ForEach-Object { "$($_.Path):$($_.LineNumber)" }`;
.NET regular expressions need `\s` instead of `[[:space:]]`.

To classify a candidate, view only its line, masked. The masks hide URL
passwords, values assigned to sensitive names, and every run of 16 or more
token characters:

```text
git show :<path> | sed -n '<n>p' | sed -E 's#(://[^/:@[:space:]]+:)[^/@[:space:]]+@#\1[REDACTED]@#g; s/((pass(word|wd)?|pwd|secret|token|key)[a-z0-9_]*["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"']?)[^"'"'"'[:space:];&,]+/\1[REDACTED]/Ig; s/[A-Za-z0-9+\/=_-]{16,}/[REDACTED]/g'
(Get-Content <path>)[<n>-1] -replace '(://[^/:@\s]+:)[^/@\s]+@','$1[REDACTED]@' -replace '((pass(word|wd)?|pwd|secret|token|key)\w*["'']?\s*[:=]\s*["'']?)[^"''\s;&,]+','$1[REDACTED]' -replace '[A-Za-z0-9+/=_-]{16,}','[REDACTED]'
```

The first form (POSIX shell, GNU sed) reads the index; use `<sha>:<path>` for
a revision or `cat <path>` for a current file. The second form (PowerShell)
reads a current file; use `git show ":<path>"` instead of `Get-Content` for the
index. Masking is best effort: a short secret under an unusual name can
survive it, so classify from the name, file, and neighbouring masked lines
before viewing more. Masking also hides placeholder words; find them with a
second location-only search on the same file and compare line numbers:
`example|sample|dummy|fake|placeholder|changeme|your[_-]|xxxx|<[a-z_-]+>`
(case-insensitive).

## 1. Private keys

`-----BEGIN ([A-Z0-9]+ )*PRIVATE KEY( BLOCK)?-----`

Covers RSA, EC, DSA, OpenSSH, PKCS#8, and PGP private keys. A real private key
is an effective secret wherever it is committed.

## 2. Provider tokens

- AWS access key ID: `(AKIA|ASIA)[0-9A-Z]{16}`
- GitHub: `gh[pousr]_[A-Za-z0-9]{36}`, `github_pat_[A-Za-z0-9_]{22,}`
- GitLab: `glpat-[A-Za-z0-9_-]{20}`
- Slack: `xox[abposr]-[A-Za-z0-9-]{10,}`, `hooks\.slack\.com/services/`
- Stripe secret: `(sk|rk)_(live|test)_[A-Za-z0-9_]{16,}`
- Google API: `AIza[0-9A-Za-z_-]{35}`
- OpenAI, Anthropic: `sk-(proj-|ant-)?[A-Za-z0-9_-]{20,}`
- npm: `npm_[A-Za-z0-9]{36}`
- Telegram bot: `[0-9]{8,10}:AA[A-Za-z0-9_-]{33}`
- Azure: `AccountKey=`, `SharedAccessSignature=`
- JWT: `eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.`

A JWT is a secret when it is a usable session or service token, not when it is
an obviously expired documentation sample. Publishable keys (Stripe `pk_`,
public client IDs) are public by design.

## 3. Credentials in URLs and connection strings

- URL with user and password: `[a-zA-Z][a-zA-Z0-9+.-]*://[^/:@[:space:]]+:[^/@[:space:]]+@`
- Connection-string password (case-insensitive): `(password|pwd)=[^;&[:space:]]+`

## 4. Literal values in sensitive assignments

Case-insensitive:

```text
(password|passwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret|auth)[a-z0-9_]*["']?[[:space:]]*[:=][[:space:]]*["'][^"']{8,}["']
```

Only literals count. A reference to an environment variable, secret store, or
template variable (`os.environ[...]`, `process.env.X`, `${X}`, `{{ x }}`) is
not a leak. Long base64 or hex values (`[A-Za-z0-9+/]{40,}={0,2}`,
`[0-9a-f]{40,}`) matter only next to sensitive names or in configuration
files; elsewhere they are usually hashes, IDs, or test data.

## 5. Sensitive files

Match names in the scope's file list (`git diff --cached --name-only -z`,
`git ls-files --cached --others --exclude-standard -z`, or the history file
list), not their contents:

- `.env`, `.env.*`; `.env.example`, `.env.sample`, `.env.template` are
  expected, but still search their contents;
- `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `id_rsa`,
  `id_ecdsa`, `id_ed25519`, `*.kdbx`;
- `kubeconfig`, `.kube/config`, `credentials.json`, `service-account*.json`,
  `*.tfstate`, `*.tfvars`;
- `.npmrc`, `.pypirc`, `.netrc`, `.git-credentials`, `.dockercfg`,
  `.docker/config.json` that contain auth entries.

A sensitive file name is a finding to classify; its content decides whether it
holds an effective secret.

## 6. Personal and local data

Personal or local data that would be published is WARN (see
[severity](severity.md)). Case-insensitive:

- absolute user path: `([a-z]:[\/]|/[a-z]/)users[\/][^\/[:space:]]+`,
  `/(home|Users)/[^/[:space:]]+`
- email address: `[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}`
- private IP address: `(10|192\.168|172\.(1[6-9]|2[0-9]|3[01]))\.[0-9]{1,3}\.[0-9]{1,3}`
- internal host name: `[a-z0-9-]+\.(local|internal|corp|lan|intranet)`

Classify before reporting. Not leaks: `noreply`/`no-reply` addresses,
`example.com`/`.org`/`.net`, placeholder users such as `<user>`, and contacts
the project deliberately publishes. Leaks: a real person's personal address,
local paths revealing a user name, internal hosts, IP addresses, and system or
client identifiers. Real personal records of other people (customers, users,
employees) in fixtures, dumps, or logs are a sensitive-data exposure; rate
bulk records by [severity](severity.md). Commit author metadata is outside the
reviewed content.

## 7. Unwanted artifacts

Check added or tracked files that usually should not be committed: logs,
crash dumps, HAR files, database files (`*.sqlite`, `*.db`), archives, notebooks
with stored outputs, build outputs, editor or OS files, and agent temporary
files (`.tmp/`). Compare them with the ignore and packaging rules. Use
`git cat-file -s <blob>` for sizes; search the text files with the classes
above. An artifact with data is a leak to classify; an empty or harmless one is
Low hygiene.
