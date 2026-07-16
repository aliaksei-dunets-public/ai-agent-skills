---
name: development-orchestrator-installer
description: >-
  Audits an existing software project, analyzes its agent skills, instructions,
  documentation, task system, test infrastructure, CI/CD and project configuration,
  then safely installs, adapts, upgrades or repairs the portable
  development-orchestrator workflow for that project. Use when a repository needs
  project-aware orchestration of task management, isolated review subagents, project
  diagnostics and quality hooks, approval, testing, documentation synchronization,
  memory and task archival.
version: 1.2.0
---

# Development Orchestrator Installer

## 1. Назначение

Ты — установщик и интегратор навыка `development-orchestrator`.

Твоя задача — не просто скопировать файл оркестратора, а:

1. провести аудит проекта;
2. определить существующую AI- и development-инфраструктуру;
3. изучить навыки, инструкции, документацию, конфигурации, тесты и task-management;
4. проверить совместимость проекта с обязательным циклом разработки;
5. сопоставить существующие навыки с контрактами оркестратора;
6. спроектировать безопасную интеграцию;
7. установить и настроить `development-orchestrator` с учётом проекта;
8. создать адаптеры только там, где существующие навыки несовместимы по интерфейсу;
9. определить механизм запуска независимых субагентов для `task-review` и `code-review`;
10. обнаружить дополнительные проектные инструменты и безопасно подключить их как lifecycle hooks;
11. проверить установку и выполнить безопасный dry run;
12. подготовить отчёт, manifest и инструкции по эксплуатации.

Установщик должен быть переносимым между проектами и платформами. Проектные особенности должны храниться в конфигурации, project-context и адаптерах, а не в ядре жизненного цикла.

## 2. Режимы работы

Поддерживай четыре режима.

### `audit`

Только анализирует проект и формирует отчёт. Файлы проекта не изменяются.

### `install`

Проводит аудит, проектирует интеграцию и устанавливает оркестратор, если его ещё нет.

### `upgrade`

Сравнивает установленную версию с поставляемым шаблоном, сохраняет проектные настройки и обновляет ядро без потери локальной конфигурации.

### `repair`

Проверяет существующую установку, восстанавливает отсутствующие или повреждённые компоненты и не меняет корректные пользовательские настройки без необходимости.

Если режим не указан:

- используй `install`, если оркестратор отсутствует;
- используй `upgrade`, если обнаружена более старая версия;
- используй `repair`, если установка существует, но неполна или неконсистентна;
- используй `audit`, если пользователь явно запретил изменения.

## 3. Источник установки

Канонический навык оркестратора должен находиться рядом с установщиком:

```text
assets/development-orchestrator-SKILL.md
```

Дополнительные шаблоны:

```text
templates/orchestrator.config.yaml
templates/memory.md
templates/tasks.md
templates/completed-tasks.md
```

Если канонический файл отсутствует или не читается, останови установку. Не создавай упрощённую версию оркестратора по памяти.

## 4. Обязательные принципы

1. Сначала анализируй, затем проектируй и только потом изменяй файлы.
2. Не изменяй production-код в рамках установки.
3. Не перезаписывай существующие инструкции, навыки, task-файлы или конфигурации без резервной копии и анализа различий.
4. Не выдумывай команды сборки, тестирования, покрытия, линтинга или документации.
5. Не считай одинаковыми навыки только по похожему имени — анализируй их фактический контракт.
6. Сохраняй существующие проектные соглашения, если они не конфликтуют с обязательными инвариантами оркестратора.
7. Не дублируй большие инструкции между платформенными файлами. Добавляй короткие ссылки на единый источник.
8. Проектные различия изолируй в `orchestrator.config.yaml`, `orchestrator.project.md` и адаптерах.
9. Не ослабляй требования review, approval, тестирования, покрытия, документации и архивирования.
10. Установка должна быть идемпотентной: повторный запуск не создаёт дубликаты и не портит корректную установку.
11. Не сохраняй секреты, токены, пароли, cookies, приватные ключи или персональные данные.
12. `task-review` и `code-review` должны запускаться через независимых субагентов со свежим контекстом; не подменяй это самопроверкой основного агента.
13. Обнаруженный diagnostic/health-check инструмент не включается автоматически, пока не подтверждены его безопасность, точка запуска и политика ошибки.
14. Все выводы должны быть подтверждены файлами, конфигурацией, командами или фактической структурой проекта.

## 5. Неприкосновенные инварианты оркестратора

Установщик может адаптировать пути, команды, имена навыков и проектный контекст, но не должен менять следующие правила:

- основной lifecycle: `created → in_progress → review → approved → done`;
- отдельное техническое поле `execution_state`;
- `review_execution.mode` всегда равен `subagent_required`; self-review в текущем контексте не является допустимой заменой;
- `task-review` выполняется после реализации плана отдельным субагентом со свежим контекстом и строгими инструкциями (automated function, only YAML);
- `code-review` выполняется после успешного `task-review` другим независимым субагентом со строгими инструкциями (automated function, only YAML);
- review-субагенты по умолчанию не имеют права изменять код или task state;
- каждый review допускает максимум два запуска на ревизию;
- после неуспешного второго review процесс блокируется;
- статус `review` устанавливается только после успешных review;
- статус `approved` устанавливается только после явного подтверждения пользователя;
- базовое тестирование (basic unit/verification tests) выполняется до review (Stage 2.5);
- создание продвинутых тестов и финальная проверка покрытия выполняются после approval;
- unit и integration testing должны быть созданы/обновлены либо явно отмечены `not_applicable` с обоснованием;
- техническое состояние задачи хранится в YAML frontmatter (fields: status, execution_state, revision и др.);
- минимальное покрытие по умолчанию — 80% для нового и изменённого кода;
- документация синхронизируется после тестов;
- в задачу добавляется `Completed work`;
- оперативная память агента хранится отдельно в `memory.md`;
- `done` допустим только после тестов, покрытия, документации, memory sync и архивирования;
- завершённая задача переносится в completed archive без потери истории;
- обязательные project tools с `failure_policy: block` должны пройти до соответствующего перехода lifecycle.

Если проектные требования конфликтуют с этими инвариантами, не изменяй их автоматически. Зафиксируй конфликт и запроси решение пользователя.

## 6. Ожидаемая целевая структура

Используй существующую структуру проекта, если она уже стандартизирована. При отсутствии подходящей структуры рекомендуется:

```text
.ai/
├── orchestrator.config.yaml
├── orchestrator.project.md
├── orchestrator.manifest.yaml
├── memory.md
├── scripts/
│   └── sync_tasks.py
├── tasks/
│   ├── tasks.md
│   ├── active/
│   └── completed/
│       └── completed-tasks.md
├── skills/
│   ├── development-orchestrator/
│   │   └── SKILL.md
│   └── adapters/
│       ├── task-manager/
│       │   └── SKILL.md
│       ├── task-review/
│       │   └── SKILL.md
│       ├── code-review/
│       │   └── SKILL.md
│       ├── create-test/
│       │   └── SKILL.md
│       └── doc-sync/
│           └── SKILL.md
└── reports/
    └── development-orchestrator-installation.md
```

Не создавай адаптеры, если существующий навык уже соответствует контракту.

## 7. Полный процесс установки

### Phase 0 — Инициализация

1. Определи корень репозитория.
2. Определи запрошенный режим.
3. Найди канонический orchestrator asset и шаблоны.
4. Проверь доступ на чтение и запись.
5. Зафиксируй текущую ветку и состояние working tree, если Git доступен.
6. Не требуй чистого working tree, но явно отметь незакоммиченные изменения и не смешивай их с установкой.
7. Создай внутренний installation session id и используй его в backup и report.

### Phase 1 — Project Discovery

Исследуй проект от общего к частному.

#### 1.1. Структура и стек

Определи:

- языки программирования;
- framework и runtime;
- package/build systems;
- backend, frontend, UI, CLI и mobile-компоненты;
- source roots;
- test roots;
- docs roots;
- generated code;
- monorepo/workspace structure;
- базы данных и миграции;
- внешние сервисы;
- контейнеризацию и инфраструктуру.

Проверяй характерные конфигурации, включая, но не ограничиваясь:

- `pyproject.toml`, `requirements*.txt`, `Pipfile`, `tox.ini`;
- `package.json`, lock-файлы, workspace-конфигурации;
- `pom.xml`, `build.gradle*`;
- `Cargo.toml`, `go.mod`;
- `Dockerfile*`, compose-файлы;
- CI/CD workflows;
- линтеры, formatters, type-checkers;
- test runner и coverage configs.

Не ограничивайся этим списком.

#### 1.2. AI instructions и agent configuration

Найди и изучи:

- `AGENTS.md` и вложенные варианты;
- `CLAUDE.md`;
- `.github/copilot-instructions.md`;
- `.github/instructions/**`;
- `.cursor/rules/**`, `.cursorrules`;
- `.windsurf/**`;
- Codex/OpenAI/agent configuration;
- Cline/Roo/Gemini/Aider instructions;
- MCP-конфигурации;
- локальные skill-каталоги;
- prompts, workflows, rules, references и checklists.

Определи приоритет, область действия и возможные конфликты инструкций.

#### 1.3. Документация

Найди:

- README;
- архитектуру;
- ADR;
- API documentation;
- development/setup guides;
- coding standards;
- testing guides;
- deployment/runbooks;
- contribution guides;
- business/domain documentation;
- known issues и troubleshooting.

Определи официальные источники истины и устаревшие документы.

#### 1.4. Task-management

Определи, как проект хранит задачи:

- Markdown task-файлы;
- issues;
- TODO-файлы;
- backlog;
- project management integration;
- существующий `task-manager` skill.

Проверь:

- формат задачи;
- статусы;
- приоритеты;
- зависимости;
- acceptance criteria;
- планы реализации;
- историю выполнения;
- архивирование.

#### 1.5. Quality pipeline

Определи фактические команды и инструменты для:

- format;
- lint;
- static analysis;
- type checking;
- unit tests;
- integration tests;
- coverage;
- security checks;
- build;
- docs generation/validation;
- diagnostics;
- health checks;
- smoke checks;
- consistency/integrity validators;
- project-specific CLI checks;
- MCP tools, используемые для безопасной проверки проекта.

Для каждого дополнительного инструмента определи:

- тип: `command`, `skill` или `mcp`;
- назначение;
- безопасен ли автоматический запуск;
- требует ли credentials, внешней системы или production data;
- подходящую стадию: `on_demand`, `post_implementation`, `pre_review`, `post_tests` или `pre_done`;
- обязательность;
- `failure_policy`: `block` или `warn`;
- условия запуска;
- доказательство существования и корректной команды.

Команды должны быть подтверждены конфигурацией, CI, package scripts или документацией. Сам факт обнаружения инструмента не является разрешением на запуск.

### Phase 2 — Artifact Inventory

Построй инвентаризацию всех релевантных материалов.

Для каждого элемента зафиксируй:

```yaml
path: "relative/path"
type: skill | instruction | rule | workflow | documentation | config | task-store | test-config | ci | mcp | template | project-tool
scope: global | repository | directory | platform-specific
purpose: "..."
status: active | uncertain | obsolete | conflicting
consumers:
  - "..."
dependencies:
  - "..."
overlap:
  - "..."
risks:
  - "..."
```

Не включай в полный контекст большие generated/vendor/build каталоги. Используй их только при необходимости для подтверждения вывода.

### Phase 3 — Project Profile

Создай нормализованный профиль проекта.

Минимальный формат:

```yaml
project:
  name: "detected-name"
  repository_type: single | monorepo
  languages: []
  frameworks: []
  source_roots: []
  test_roots: []
  docs_roots: []
  generated_roots: []

instructions:
  canonical: []
  platform_specific: []

commands:
  install: []
  build: []
  format: []
  lint: []
  typecheck: []
  unit_test: []
  integration_test: []
  coverage: []
  docs_check: []

quality:
  existing_coverage_threshold: null
  changed_code_coverage_threshold: 80

subagents:
  supported: null
  mechanism: null
  task_review_profile: null
  code_review_profile: null

project_tools: []

constraints: []
unknowns: []
```

Неподтверждённые значения помещай в `unknowns`, а не заполняй предположениями.

### Phase 4 — Skills Audit and Capability Mapping

Найди все существующие навыки и проанализируй их содержимое, а не только названия.

Обязательные роли оркестратора:

- `task-manager`;
- `task-review`;
- `code-review`;
- `create-test`;
- `doc-sync`.

Дополнительные роли могут включать:

- debug;
- architecture review;
- security review;
- performance review;
- refactoring;
- stack/domain-specific development;
- release/deployment.

Отдельно проверь поддержку субагентов на целевой платформе:

- существует ли нативный механизм запуска субагента;
- можно ли создать свежий контекст на каждый review-run;
- можно ли запретить review-субагенту запись;
- можно ли передать задачу, diff и project rules;
- можно ли получить структурированный результат;
- можно ли использовать разные профили для task review и code review.

Если независимый запуск review-субагентов невозможен, классифицируй это как `blocking` для full-cycle режима. Не обозначай основной агент как независимого reviewer.

Для каждого обязательного навыка установи один статус:

| Статус | Значение |
|---|---|
| `native-compatible` | Навык соответствует требуемому контракту без изменений |
| `adapter-required` | Функциональность подходит, но вход/выход или границы ответственности несовместимы |
| `partial` | Покрыта только часть обязательной ответственности |
| `conflicting` | Навык нарушает lifecycle или изменяет состояния вне своей ответственности |
| `missing` | Подходящего навыка нет |
| `duplicate` | Есть несколько перекрывающихся реализаций |
| `obsolete` | Навык не соответствует актуальному проекту |

Построй capability matrix:

```markdown
| Required role | Existing skill | Compatibility | Gaps | Decision |
|---|---|---|---|---|
| task-manager | ... | native-compatible | none | reuse |
| task-review | ... | adapter-required | output schema | create adapter |
```

### Phase 5 — Contract Validation

Каждый дочерний навык должен возвращать результат, совместимый с:

```yaml
skill: task-review
result: passed | failed | blocked
summary: "Краткий итог"
findings:
  - severity: critical | high | medium | low | info
    category: completeness | correctness | security | architecture | maintainability | testing | docs
    location: "path/to/file:line"
    description: "Что обнаружено"
    required_action: "Что необходимо исправить"
changed_files: []
artifacts: []
blocking_reasons: []
```

Дополнительные требования по ролям:

#### `task-manager`

Должен уметь:

- находить/выбирать задачу;
- читать план и зависимости;
- валидировать допустимость перехода;
- атомарно изменять статус и execution state (рекомендуется использовать скрипт `update_task.py` с JSON-файлом данных `--apply`, вместо ручного редактирования YAML);
- вести work log;
- архивировать завершённую задачу без потери истории.

#### `task-review`

Должен проверять:

- выполнение плана;
- acceptance criteria;
- scope;
- полноту сценариев;
- отсутствие незавершённых заглушек.

Не должен выполнять общий code review вместо своей области.

Должен запускаться отдельным субагентом со свежим контекстом и возвращать только review-result. Не должен исправлять код или менять статусы.

#### `code-review`

Должен проверять:

- correctness;
- error handling;
- security;
- architecture;
- maintainability;
- compatibility;
- существенные performance-риски;
- соблюдение проектных правил.

Не должен менять task lifecycle самостоятельно.

Должен запускаться другим независимым субагентом со свежим контекстом. Не должен переиспользовать task-review контекст, исправлять код или менять статусы.

#### `create-test`

Должен:

- оценивать применимость unit/integration tests;
- создавать или обновлять применимые тесты;
- запускать тесты;
- анализировать failures;
- измерять coverage;
- возвращать команды, результаты и changed files.

#### `doc-sync`

Должен:

- определять затронутую документацию;
- синхронизировать docs с фактическим кодом;
- фиксировать изменённые документы;
- обосновывать `not_applicable`.

### Phase 6 — Gap and Conflict Analysis

Определи:

- отсутствующие обязательные роли;
- навыки с чрезмерной ответственностью;
- навыки, которые сами меняют статусы;
- дублирование review/testing/docs логики;
- конфликтующие требования покрытия;
- несовместимые task statuses;
- различия в approval model;
- устаревшие пути и команды;
- платформенные инструкции, которые могут обходить оркестратор;
- риски циклов;
- скрытые зависимости от конкретной среды;
- отсутствие или недостаточную изоляцию review-субагентов;
- обнаруженные diagnostics/health checks без безопасной точки интеграции;
- project tools, которые могут выполнять destructive, deployment или production operations.

Классифицируй каждый конфликт:

- `blocking` — установка не может безопасно продолжиться;
- `requires-decision` — требуется выбор пользователя;
- `auto-resolvable` — можно устранить адаптером или конфигурацией;
- `informational` — не мешает установке.

### Phase 7 — Integration Design

Спроектируй интеграцию с минимальными изменениями проекта.

#### 7.1. Reuse first

Приоритет решений:

```text
повторно использовать совместимый навык
→ создать тонкий adapter
→ расширить существующую конфигурацию
→ создать недостающий минимальный компонент
→ остановиться при невозможности безопасной интеграции
```

Не копируй существующие навыки и не переписывай их без необходимости.

#### 7.2. Adapter strategy

Создавай adapter, если навык функционально полезен, но:

- имеет другое имя;
- принимает другой вход;
- возвращает неструктурированный результат;
- совмещает несколько ролей;
- меняет task status вне допустимого этапа;
- использует другие severity/status values.

Adapter должен:

- ссылаться на исходный навык;
- преобразовывать вход и выход;
- ограничивать область ответственности;
- не дублировать доменную экспертизу исходного навыка;
- явно описывать mapping;
- оставаться коротким.

#### 7.3. Missing skills

Если обязательный навык отсутствует:

- не имитируй полный навык одной строкой;
- установи orchestrator core и пометь интеграцию как `blocked`, либо создай только scaffold/contract по явному разрешению пользователя;
- перечисли, что необходимо реализовать;
- не объявляй установку полностью operational.

#### 7.4. Review subagent integration

Настрой платформозависимый способ запуска review-субагентов, сохранив платформонезависимый контракт оркестратора.

Требования:

- `mode: subagent_required`;
- новый изолированный контекст для каждого запуска;
- отдельные профили `task-reviewer` и `code-reviewer` либо эквивалентные роли;
- отсутствие write-access по умолчанию;
- структурированный output contract;
- запрет на изменение task state;
- `unsupported_platform: block`.

Платформенный adapter должен описывать только способ запуска. Он не должен переносить review-логику в основной агент.

#### 7.5. Project tools and lifecycle hooks

Для каждого найденного дополнительного инструмента выбери одно решение:

- `integrate-required` — безопасный обязательный quality gate;
- `integrate-optional` — безопасная вспомогательная проверка;
- `on-demand` — диагностика, запускаемая только при необходимости;
- `manual-only` — требуется пользователь, credentials или внешняя система;
- `excluded` — destructive, deployment, production-data или нерелевантный инструмент;
- `unresolved` — недостаточно данных.

Автоматически добавляй tool в конфигурацию только когда подтверждены:

1. точный entrypoint;
2. безопасность;
3. стадия lifecycle;
4. required/optional статус;
5. failure policy;
6. условия запуска.

Допустимые стадии:

- `on_demand`;
- `post_implementation`;
- `pre_review`;
- `post_tests`;
- `pre_done`.

Дополнительные инструменты не заменяют обязательные skills, reviews, tests или documentation sync.

#### 7.6. Project context

Создай `.ai/orchestrator.project.md` как индекс, а не копию всей документации.

Он должен содержать:

- краткий профиль проекта;
- canonical instructions;
- ссылки на архитектурные и domain docs;
- source/test/docs roots;
- подтверждённые команды;
- skill mapping;
- review subagent mechanism;
- project tools and hook stages;
- known constraints;
- правила progressive loading;
- список неопределённостей.

Не копируй в него большие документы.

### Phase 8 — Installation Plan

До изменения файлов покажи план установки, если пользователь ещё не дал явное разрешение на применение.

План должен содержать:

- detected project profile;
- найденные навыки;
- capability matrix;
- конфликты и blockers;
- создаваемые файлы;
- изменяемые файлы;
- backup strategy;
- adapter list;
- review subagent integration;
- project tools inventory and hook mapping;
- команды проверки;
- rollback plan;
- ожидаемый operational status.

Явный запрос вида «установи», «разверни», «примени изменения» может считаться разрешением на применение после публикации плана, если нет `blocking` или `requires-decision` конфликтов.

### Phase 9 — Safe Apply

#### 9.1. Backup

Перед изменением существующих файлов создай backup только затрагиваемых файлов:

```text
.ai/backups/development-orchestrator/<session-id>/
```

Сохрани относительную структуру путей.

Не помещай секреты в отчёт. Если backup содержит чувствительную конфигурацию, не цитируй её содержимое.

#### 9.2. Install core

Установи канонический файл в согласованный skill path, например:

```text
.ai/skills/development-orchestrator/SKILL.md
```

Разрешены только проектно-ориентированные изменения установленной копии:

- ссылки на config и project-context;
- фактические пути;
- mapping имён навыков;
- подтверждённые команды;
- stack-specific references;
- короткий generated integration block.

Не изменяй core lifecycle и защиту от циклов.

#### 9.3. Install configuration

Создай или обнови:

```text
.ai/orchestrator.config.yaml
```

Конфигурация должна содержать только подтверждённые значения. Для неизвестного используй `null`, пустой список или `unresolved`.

Обязательно заполни:

- `review_execution` — механизм изолированных review-субагентов;
- `project_tools` — только проверенные и классифицированные hooks.

#### 9.4. Install project context

Создай или обнови:

```text
.ai/orchestrator.project.md
```

Сохраняй пользовательские ручные блоки. Для generated sections используй маркеры:

```markdown
<!-- BEGIN GENERATED: DEVELOPMENT-ORCHESTRATOR -->
...
<!-- END GENERATED: DEVELOPMENT-ORCHESTRATOR -->
```

Повторная установка должна заменять только generated block.

#### 9.5. Install adapters

Создавай только необходимые adapters в:

```text
.ai/skills/adapters/<required-role>/SKILL.md
```

Каждый adapter должен указывать:

- wrapped skill;
- причина адаптации;
- input mapping;
- output mapping;
- запрещённые side effects;
- structured result contract.

#### 9.6. Initialize state files

Создавай файлы только если подходящих существующих источников нет:

```text
.ai/memory.md
.ai/tasks/tasks.md
.ai/tasks/active/
.ai/tasks/completed/completed-tasks.md
```

Установи утилиты из шаблонов:
```text
.ai/scripts/sync_tasks.py
.ai/scripts/update_task.py
```
Формат задач должен использовать YAML frontmatter для хранения метаданных в файле `.md`.
Frontmatter обязан начинаться с первой строки, использовать только ключи
канонической схемы и содержать `execution_state` с подчёркиванием. Индексатор
должен завершаться ошибкой при неизвестных, отсутствующих или противоречивых
полях.

Если task system уже существует, не создавай параллельный backlog автоматически. Настрой `task-manager` или adapter на существующий источник.

При создании или обновлении `memory.md` не добавляй предположения. Разрешены
только подтверждённые стабильные факты, неочевидные команды, подтверждённые
ловушки проекта и долговечные особенности окружения или инструментов.

`memory.md` является производным слоем контекста, а не источником истины.
При конфликте используй приоритет:

```text
код и конфигурация
→ официальная документация
→ task-файлы и записи review
→ memory.md
```

Не записывай в `memory.md` task-specific test counts, результаты review,
approval evidence, coverage waiver, текущий прогресс, work log, сырые логи,
одноразовую диагностику или сведения, предназначенные для README, ADR,
документации API или task tracker. Не сохраняй секреты, токены, пароли,
cookies, private keys и персональные данные.

При Memory Sync удаляй или исправляй устаревшие и противоречивые записи.
Если устойчивых новых фактов нет, оставь файл без изменений.

#### 9.7. Platform entrypoints

При необходимости добавь короткое указание в платформенные файлы:

```markdown
For full-cycle project task implementation, use the repository skill
`.ai/skills/development-orchestrator/SKILL.md` and follow
`.ai/orchestrator.config.yaml` plus `.ai/orchestrator.project.md`.
```

Не копируй весь orchestrator в `AGENTS.md`, `CLAUDE.md`, Copilot или Cursor rules.

Не изменяй платформенный файл, если его scope или формат не подтверждены.

#### 9.8. Manifest

Создай:

```text
.ai/orchestrator.manifest.yaml
```

Пример:

```yaml
installer:
  name: development-orchestrator-installer
  version: 1.2.0
  installed_at: "YYYY-MM-DDTHH:MM:SSZ"
  mode: install

orchestrator:
  version: 1.2.0
  source: "installer/assets/development-orchestrator-SKILL.md"
  target: ".ai/skills/development-orchestrator/SKILL.md"
  sha256: "computed-after-install"

managed_files: []
modified_files: []
adapters: []
skill_mapping: {}
subagent_mapping: {}
project_tools: []
unresolved: []
validation:
  status: pending
```

Manifest должен позволять upgrade, repair и rollback. Для canonical core
обязательно сохраняй checksum, чтобы обнаруживать рассинхронизацию asset и
установленной копии.

### Phase 10 — Validation

После применения выполни проверки.

#### 10.1. Structural validation

Проверь:

- обязательные файлы существуют;
- ссылки и пути корректны;
- YAML/JSON/TOML, изменённые установщиком, синтаксически валидны;
- все task records проходят строгую frontmatter/schema validation;
- active/completed placement соответствует `status`;
- generated markers сбалансированы;
- отсутствуют дублированные installation blocks;
- manifest соответствует фактическим файлам.

#### 10.2. Contract validation

Проверь:

- каждая обязательная роль mapped;
- native skill или adapter имеет необходимый контракт;
- дочерние навыки не управляют полным lifecycle;
- review limits не переопределены конфликтующей инструкцией;
- `task-review` и `code-review` запускаются отдельными субагентами;
- review-субагенты получают свежий контекст и не имеют write-access по умолчанию;
- project tools имеют подтверждённую стадию, безопасность и failure policy;
- approval остаётся явным;
- тестирование и doc-sync нельзя пропустить молча.

#### 10.3. Command validation

Разрешено выполнять только безопасные команды обнаружения и проверки.

Команды, изменяющие production data, отправляющие запросы во внешние системы, выполняющие deployment, миграции или destructive operations, не запускай.

Для test/build/lint и project-tool команд:

- используй существующее окружение;
- не устанавливай зависимости без разрешения;
- при невозможности запуска зафиксируй `not_executed` с причиной;
- не выдавай статический анализ команды за успешное выполнение.
- task utilities не должны выполнять `git add`, `git commit` или иные операции
  публикации изменений.

#### 10.4. Dry run

Выполни симуляцию без изменения production-кода и без перевода реальной задачи в новый статус.

Dry run должен проверить:

1. поиск task source;
2. выбор фиктивной или специально созданной dry-run задачи;
3. routing к `task-manager`;
4. запуск `task-review` через отдельного субагента;
5. запуск `code-review` через другого независимого субагента;
6. новый свежий контекст для повторного review-run;
7. routing и failure policy project tools;
8. остановку перед approval;
9. распознавание test и doc-sync этапов;
10. корректность archive path;
11. доступность memory path;
12. срабатывание review limits.

Если невозможно безопасно использовать реальный task source, выполни статическую симуляцию и явно обозначь её как `static dry run`.

#### 10.5. Operational status

Установка получает один статус:

- `operational` — все обязательные роли mapped и validation пройдена;
- `operational_with_warnings` — lifecycle доступен, но есть неблокирующие ограничения;
- `installed_but_blocked` — core установлен, но отсутствует обязательный навык, изолированный subagent mechanism, доступ или конфигурация;
- `audit_only` — изменения не выполнялись;
- `failed` — установка не завершена или нарушена целостность.

### Phase 11 — Installation Report

Создай отчёт:

```text
.ai/reports/development-orchestrator-installation.md
```

Он должен содержать:

```markdown
# Development Orchestrator Installation Report

## Summary

## Mode and operational status

## Project profile

## Discovered instructions and documentation

## Existing skills inventory

## Capability matrix

## Conflicts and resolutions

## Installed files

## Modified files

## Created adapters

## Review subagent integration

## Project tools and lifecycle hooks

## Task-system integration

## Test and coverage integration

## Documentation integration

## Platform integration

## Validation results

## Dry-run result

## Unresolved items

## Rollback instructions

## Usage examples
```

Не вставляй в отчёт секреты и большие копии исходных документов.

## 8. Конфигурация проекта

Рекомендуемая расширенная конфигурация:

```yaml
orchestrator:
  version: "1.2.0"
  tasks_file: ".ai/tasks/tasks.md"
  completed_file: ".ai/tasks/completed/completed-tasks.md"
  memory_file: ".ai/memory.md"
  project_context_file: ".ai/orchestrator.project.md"

  skills:
    task_manager:
      name: "task-manager"
      path: null
      integration: "unresolved"
    task_review:
      name: "task-review"
      path: null
      integration: "unresolved"
    code_review:
      name: "code-review"
      path: null
      integration: "unresolved"
    create_test:
      name: "create-test"
      path: null
      integration: "unresolved"
    doc_sync:
      name: "doc-sync"
      path: null
      integration: "unresolved"

  review_execution:
    mode: "subagent_required"
    isolation: "fresh_context_per_run"
    write_access: false
    unsupported_platform: "block"
    task_review_profile: null
    code_review_profile: null
    launcher: "auto"
    close_completed_agents_before_spawn: true
    reuse_completed_context: false

  limits:
    task_review_runs_per_revision: 2
    code_review_runs_per_revision: 2
    test_fix_attempts: 3

  quality:
    coverage_policy: "configured_only"
    minimum_coverage_percent: 80
    coverage_scope: "changed-and-new-code"
    do_not_reduce_project_coverage: true

  task_selection:
    strategy: "priority_then_created_at"
    require_dependencies_done: true

  archive:
    remove_from_active_file: true
    preserve_full_history: true

project:
  name: null
  repository_type: null
  languages: []
  frameworks: []
  source_roots: []
  test_roots: []
  docs_roots: []
  generated_roots: []

commands:
  install: []
  build: []
  format: []
  lint: []
  typecheck: []
  unit_test: []
  integration_test: []
  coverage: []
  docs_check: []

# Installer adds only verified project-specific tools.
# Valid stages: on_demand, post_implementation, pre_review, post_tests, pre_done.
# Valid types: command, skill, mcp.
# Valid failure_policy: block, warn.
project_tools: []
# Example:
#  - id: "project-health-check"
#    type: "command"
#    ref: "scripts/health-check.sh"
#    stage: "pre_review"
#    required: true
#    safe_to_run: true
#    failure_policy: "block"
#    conditions: []

context_loading:
  always:
    - ".ai/orchestrator.config.yaml"
    - ".ai/orchestrator.project.md"
    - ".ai/memory.md"
  on_demand: []
  excluded: []

installation:
  managed_by: "development-orchestrator-installer"
  preserve_manual_sections: true
```

Не сохраняй альтернативы через синтаксис `a | b` в фактическом YAML. При генерации выбери одно подтверждённое значение.

## 9. Правила адаптации под проект

### 9.1. Стек

Добавляй stack-specific references и команды, но не помещай в orchestrator подробные coding standards. Оркестратор должен ссылаться на существующие правила проекта.

### 9.2. Monorepo

Для monorepo:

- определи scopes/workspaces;
- храни общие lifecycle rules централизованно;
- добавь mapping команд и docs по scope;
- не создавай отдельный оркестратор для каждого пакета без необходимости;
- task должен явно указывать затронутый scope.

### 9.3. Несколько test runners

Храни команды по scope и типу теста. Не запускай весь monorepo, если задача затрагивает один пакет и проектные правила допускают targeted execution.

### 9.4. Внешний task tracker

Если task source находится вне репозитория:

- используй существующий integration skill/tool;
- локально храни только ссылки, execution metadata и необходимые work logs, если это разрешено;
- не создавай рассинхронизированный дубликат задач;
- архивирование должно соответствовать возможностям tracker.



### 9.6. Недостижимое coverage

Не понижай порог автоматически. Зафиксируй конфликт и ожидай решения пользователя.

### 9.7. Существующий memory-файл

Не сливай автоматически память агента с официальной документацией. При наличии другого memory-файла выбери canonical source и настрой путь.

## 10. Upgrade и Repair

### Upgrade

1. Прочитай manifest.
2. Сравни версию и checksum канонического core.
3. Отдели project-generated integration block от core.
4. Создай backup.
5. Обнови core.
6. Повторно примени project integration.
7. Не перезаписывай ручные config/context sections.
8. Повтори validation и dry run.
9. Обнови manifest и report.

### Repair

1. Сравни manifest с фактическими файлами.
2. Определи missing, modified и corrupted managed files.
3. Не считай ручное изменение повреждением без анализа.
4. Восстанови только необходимые components.
5. Не удаляй неизвестные пользовательские файлы.
6. Повтори contract validation.

## 11. Rollback

Rollback должен быть возможен для каждого installation session.

1. Используй manifest и session backup.
2. Восстанови изменённые файлы.
3. Удали только файлы, созданные этим session и указанные в manifest.
4. Не удаляй файлы, которые после установки были изменены пользователем, без предупреждения и сравнения.
5. Сохрани rollback report.
6. Не затрагивай production-код.

## 12. Blockers

Останови применение и установи `installed_but_blocked` или `failed`, если:

- отсутствует канонический orchestrator asset;
- невозможно определить корень проекта;
- невозможно безопасно выбрать task source;
- обязательные роли отсутствуют и пользователь не разрешил scaffold;
- инструкции проекта прямо конфликтуют с lifecycle;
- запись в целевые пути невозможна;
- существующие файлы нельзя безопасно сохранить/объединить;
- manifest или backup не могут быть созданы перед изменением существующих файлов;
- dry run выявляет обход approval или review limits.

Не скрывай blocker под статусом warning.

## 13. Итоговый ответ пользователю

После работы сообщи:

```markdown
## Development Orchestrator — результат установки

- Режим: audit | install | upgrade | repair
- Статус: operational | operational_with_warnings | installed_but_blocked | audit_only | failed
- Проект: ...
- Оркестратор: путь и версия
- Task source: ...
- Skills mapped: X/5
- Adapters created: N
- Validation: passed | failed | partial
- Dry run: passed | static-only | failed

### Основные изменения
- ...

### Нерешённые вопросы
- none | ...

### Отчёт
- `.ai/reports/development-orchestrator-installation.md`

### Rollback
- путь к backup/manifest или `not_applicable`
```

Не объявляй систему operational, если обязательная роль не mapped или validation не пройдена.

## 14. Критерии успешной установки

Установка считается успешной только если:

- [ ] проект проанализирован;
- [ ] инструкции, навыки, документация и конфигурации инвентаризированы;
- [ ] project profile создан;
- [ ] все обязательные роли сопоставлены;
- [ ] конфликты классифицированы;
- [ ] canonical orchestrator установлен без изменения lifecycle invariants;
- [ ] project-specific config создан;
- [ ] project-context создан;
- [ ] adapters созданы только при необходимости;
- [ ] task source интегрирован без дублирования;
- [ ] memory path настроен;
- [ ] test/coverage commands подтверждены либо явно unresolved;
- [ ] docs integration настроена;
- [ ] manifest создан;
- [ ] backup создан для изменённых существующих файлов;
- [ ] structural validation пройдена;
- [ ] contract validation пройдена;
- [ ] dry run выполнен;
- [ ] installation report создан;
- [ ] operational status соответствует фактическому состоянию.

Если хотя бы один обязательный критерий не выполнен, не выдавай установку за полностью завершённую.
## Coverage policy clarification

When `quality.coverage_policy` is `configured_only`, the installer must require coverage only if `commands.coverage` contains an executable command, a defined scope, and a threshold. If coverage is absent or insufficiently described, record `not_configured` with a reason and do not block installation or task completion. The `required` policy remains available for projects that explicitly require a measurable coverage gate. This rule supersedes the legacy unconditional coverage-blocking wording in older examples.
## Dirty worktree and task scope

During installation and task execution, record the pre-existing Git working-tree state when Git is available. The installer/orchestrator must preserve unrelated changes and define a task-owned scope before review. Review subagents receive only the task-owned diff; unrelated dirty-worktree changes are not lifecycle findings.
