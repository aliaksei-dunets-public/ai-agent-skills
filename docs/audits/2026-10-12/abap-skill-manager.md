# AI Agent Skills-0004 — abap-skill-manager

Дата: 2026-10-12. Карточка: 6hjhm4P9pwjVRhGV.
Проверены SKILL.md, все пять references, README и все CONFIG_TEMPLATE.md шести навыков (у manager шаблона нет). План создан в пути карточки после подтверждения его отсутствия.

## Находки и исправления

- High, config-generation.md: генератор обрабатывал только config.md, игнорируя path heading с Required column reader/system.md. Init/update/validate теперь используют один inventory всех владельцев, полей и уровней обязательности; linked config создаётся даже при существующем config.md.
- High, SKILL.md validate/output-examples: config validation обещала self-tests pass без исполнения. Статусы config и тестов разделены; unavailable/skipped не превращаются в pass. Пример «9 tests passed» удалён.
- Medium, update/README: pull main без dirty/ref/detached preflight и автоматический staging. Добавлены SHA baseline, проверка локальных изменений, ref/upstream resolution, ff-only/clean detached handling, staging policy, partial failure/recovery.
- Medium, Phase 0/architecture/templates: .agents hardcode противоречил Claude setup. Учитываются explicit paths и active layout; неоднозначные установки не выбираются молча. Wrapper больше не читает несуществующий config навыка без шаблона.
- Medium, status: fetch main менял refs при проверке состояния и скрывал ошибку. Status использует cached upstream с freshness unknown.
- Medium, registry convention: запрет acquisition mechanics противоречил назначению reader. Механика оставлена в platform adapter, запрещено её дублирование в domain skills.
- Low, README/examples: удалён несуществующий push command; добавлены два отсутствовавших навыка. Recommended auth field не является обязательной ошибкой.

## Статические сценарии

| Пакет/сценарий | Проверенный контракт |
|---|---|
| code-review | Required local config; Recommended поля не повышают required gate |
| doc-writer | Optional YAML defaults сохраняются, нет фиктивных required fields |
| unit-test-creator | Shared namespace/platform + local prefixes; conventions остаются recommended |
| vs-reader | system.md: три required поля; shared primary_namespace; config.md link; optional mapping не обязателен |
| wiki-doc-creator | Shared namespace + output_path; пример system link требует verified owner |
| skill-manager | Нет template → нет обязательного configs/config.md |
| init twice/existing config.md | Inventory всех владельцев; append absent only, без duplicate fields/links |
| detached/dirty/manual update | Clean resolved SHA / stop conflicts / manual procedure; user work сохраняется |
| config passes, no runnable tests | Config OK + not executed/not available, без «all tests pass» |

Git diff --check выполнен успешно. Весь пакет повторно прочитан на согласованность.
Ограничения: это статическая проверка инструкций и шаблонов, а не executable E2E init→validate и не обновление live-проекта. Git update по новому workflow, SAP и независимый LLM-прогон не выполнялись.
