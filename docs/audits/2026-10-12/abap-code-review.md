# AI Agent Skills-0007 — abap-code-review

Дата: 2026-10-12. Карточка: 6hjhm4MhV3Ww5pwV.
Проверены SKILL.md, CONFIG_TEMPLATE.md и все 15 references. План подготовлен в пути карточки вместо отсутствовавшего локального плана.

## Находки и исправления

- High, Phase 2.5/7 и reporting-format: 0 CRITICAL давало зелёный header даже при failed ATC/tests. Единый combined rule: confirmed critical/failed check → red; unavailable/timeout/no tests/material gaps → yellow; green только при отсутствии этих условий. Manual counters не искажаются pre-check counts.
- High, pre-check: бесконечный polling. Ограничены время (300s) и polls (30), интервал ≥10s; stop на первом лимите, error/cancel/changed target; job ID и unknown status сохраняются, слепой повтор не разрешён.
- Medium, pre-check/reporting: diagnostic details скрывались. Добавлены concise sanitized diagnostics/result references и failed pre-checks в consolidated blockers; неизвестное не становится clean.
- Medium, Phase 2.6: вопрос «до evidence» стоял после execution. Output choice перенесён перед prechecks; historical/pasted source не проверяется против unrelated active object.
- Medium, unit precheck: проверяются safe target и isolation; необоснованное execution пропускается с видимым gap.
- Medium, lenses/exclusions: предположение «ATC would raise it» могло скрывать дефект. Dedup использует observed findings. Structural exclusions не подавляют independently proven defects. Catalog patterns — candidates, severity требует cause/impact и actual contract.
- Low, references: исправлены Phase 0.5, header ordering и несовпадающий no-tests suffix.

## Проверка

Статический walkthrough: ATC failed + 0 critical → red; unit fail + no findings → red; ATC timeout → yellow/job ID; tool missing → yellow/gap; mixed multi-object → worst signal с breakdown; no tests → ➖ и yellow; historical paste → not executed; source-confirmed defect совпадает с ATC → один cause без потери blocker. Broad transport сохраняет scoped evidence; expected checks не притворяются выполненными.

Git diff --check проходит. Markdown links/fences/frontmatter проверены: три ссылки в reporting-format — placeholders внутри кодовых примеров, не реальные отсутствующие зависимости.
Ограничения: ATC, ABAP Unit, cancellation и SAP/IDE не запускались. Header/poll behavior проверен статически, не отдельным LLM-прогоном. Справочники ABAP содержат baseline patterns, target API/platform остаются предметом проверки в реальном review.
