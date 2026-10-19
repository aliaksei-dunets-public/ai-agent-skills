# AI Agent Skills-0006 — abap-vs-reader

Дата: 2026-10-12. Карточка: 6hjhm4Jh3w7fmwX3.
Проверены SKILL.md, CONFIG_TEMPLATE.md, object-types.md и manager generation/validation contract. Локального плана не было; создан план в пути карточки.

## Находки и исправления

- High, Phase 0.5: unscoped name/type/URI индекс не различал подключения и workspace. Указан v2 key (system, connection, workspace, type/name/include), URI validation и fresh read; revision/hash передаются как observed evidence, а не гарантия snapshot.
- High, Phase 0.5/1.4: read request автоматически менял JSON и /memories. Default none, read-only index и explicit read-write; persistence требует lock + reread/merge + atomic replace. Недоступный write не ломает успешное чтение; corrupt/legacy index не переписывается автоматически.
- High, config discovery: init/validate ранее не покрывали system.md. Предыдущая задача 0004 исправила manager; здесь template явно задаёт shared required context и config entry point/link. Legacy system-only поддержан, TODO/missing owner не считается рабочим.
- Medium, ADT-path input: добавлены parsing/identity и проверка активной системы, чтобы repotree path не превращался целиком в display name.
- Medium, output: добавлены system/include/URI/revision и coverage gaps; cached source bytes не выдаются вместо fresh read.

## Проверка

Статический walkthrough: два подключения с одинаковым объектом → разные keys; unknown connection/workspace → bypass cache; legacy array → miss без migration; stale URI ENOENT → resolve; network error → error без удаления записи; concurrent cache update → lock/merge/atomic либо persistence skipped; denied write → source read остаётся успешным; missing system.md → точный stop. Git diff --check проходит; config headings сверены с inventory manager.

Ограничения: реальное переключение ADT-системы, cache concurrency/atomic implementation, VS Code и SAP не проверялись. Это контракт инструкций; если инструменты не дают требуемую защиту записи, persistence пропускается. Форматы extension API из object-types требуют подтверждения в целевом workspace; observed filename имеет приоритет. Независимого LLM-прогона не было.
