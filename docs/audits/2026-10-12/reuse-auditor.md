# AI Agent Skills-0008 — reuse-auditor

Дата: 2026-10-12. Карточка: 6hjhm4FFgJmPhGQ3.
Проверены SKILL.md, три references и agents/openai.yaml. План подготовлен в пути карточки после подтверждения отсутствия локального плана.

## Результат

High/Critical не подтверждены. Medium, config routing: literal .agents fallback оставлял discovery для уже выбранного project-local Claude wrapper неявным. Минимально уточнён приоритет explicit project path → active project-local wrapper config → legacy fallback/defaults. Global/shared copy не становится владельцем project policy. Синхронизирован template и добавлен config scenario; read-only/characterization/dynamic-reference gates сохранены.

## Статический walkthrough evaluation.md

- A: orders/fills normalize одинаковы по input/output/errors/effects, два consumers и tests → exact-duplicate/high; canonical owner выбирается по actual module ownership, characterization tests обоих callers нужны перед consolidation. Source edits нет.
- B: display currency half-up против exchange quantity down → intentional-divergence/high, owners wallet/orders, units и side effects различны, keep-separate.
- C: no static where-used не доказывает dead code; customizing CREATE OBJECT TYPE требует проверки entries/transports/dynamic sites. Obsolete candidate максимум low/medium, удаления нет.
- D: UI null → empty против exporter null → throw → semantic-duplicate/high; domain decision и characterization tests обоих paths до consolidation.
- Config: explicit owner выигрывает; selected .claude config доступен без scan; missing → defaults; global copy не подменяет target policy. Stale catalog остаётся hypothesis, не confirmed owner; external/dynamic consumers сохраняются как gaps.

Frontmatter, YAML, fenced blocks и локальные ссылки проверены; Git diff --check проходит.
Ограничения: walkthrough выполнен self-review по тексту сценариев, не независимым LLM-прогоном и не реальным refactor. Runtime quality не измерялась.
