# Language Profiles

Read only the sections for the languages in scope. Each section lists where real
callers hide, which contract details commonly differ between look-alike code, and
what to check before calling code obsolete. Project configuration may add
mechanisms; it never removes these checks.

## Generic (any language)

- Callers: direct calls, imports/includes, inheritance and interface
  implementations, configuration files, build scripts, jobs, tests, and external
  clients (APIs, message consumers, other repositories).
- Hidden references: reflection, string-built names, registries, dependency
  injection, code generation, serialization by name.
- Contract details: null/empty handling, defaults, error type and propagation,
  numeric precision and rounding, encoding, time zones, units, ordering, mutation of
  inputs, I/O, transactions, caching, thread safety.
- Before `obsolete-candidate`: search string literals and configuration for the
  name, check public/exported API status, version history, and whether tests are the
  only callers.

## Python

- Hidden references: `getattr`/`importlib`, decorators and registries, entry points
  (`pyproject.toml`), framework routing (Flask/Django/FastAPI), Celery/RQ task names,
  pytest fixtures and plugins, `__all__` and package re-exports.
- Contract details: truthiness versus `None`, `Decimal` versus `float` and rounding
  mode, mutable default arguments, naive versus aware `datetime`, sync versus async,
  exceptions raised versus returned sentinels.

## JavaScript / TypeScript

- Hidden references: dynamic `import()`, barrel re-exports (`index.ts`), string event
  names, DI containers, framework conventions (file-based routes, Angular/Vue
  component registration), `package.json` `exports`/`bin`, bundler aliases.
- Contract details: `undefined` versus `null`, number precision (no decimal type),
  `==` coercion, Promise rejection versus thrown errors, immutability expectations,
  runtime validation versus compile-time types only, browser versus Node APIs.
- Tooling hints: TypeScript language-server references, `tsc --noEmit` after
  candidate changes.

## ABAP

- Hidden references: dynamic `CALL METHOD (name)`, `CALL FUNCTION lv_name`,
  `CREATE OBJECT TYPE (name)`, BAdIs and enhancement implementations, user exits,
  RFC-enabled function modules called from other systems, OData/Gateway services,
  background jobs and report variants, customizing tables holding class or FM names,
  workflows and BRF+.
- Contract details: exceptions (classic versus class-based), `sy-subrc` semantics,
  `COMMIT WORK` and LUW boundaries, update-task calls, authority checks, packed number
  decimals and rounding, client and language dependency, buffering.
- Tooling hints: ADT/SE80 where-used list does not see dynamic or cross-system
  calls; check transport history and package interfaces before removal.

## Java / C#

- Hidden references: reflection, annotations/attributes (Spring, JAX-RS, ASP.NET
  routing), DI configuration, service loaders, serialization frameworks, generated
  clients.
- Contract details: checked versus unchecked exceptions, `BigDecimal`/`decimal`
  scale and rounding, nullability annotations, equality/hash contracts, thread
  safety, transaction annotations.

## SQL and database code

- Hidden references: views, triggers, stored procedures, ORM mappings, reporting
  tools, ETL jobs, dynamic SQL strings.
- Contract details: NULL semantics, collation, implicit casts, isolation level,
  transaction ownership, index or performance assumptions.
