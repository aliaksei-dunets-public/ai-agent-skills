# AI Agent Skills-0012 — prompter

Дата: 2026-10-12. Карточка: 6hjhm47PqvvqmFH3.
Прочитаны SKILL.md, references/universal-prompt.md и agents/openai.yaml. План подготовлен в пути карточки; findings старого snapshot перепроверены.

## Результат

Существенные дефекты не подтверждены; навык оставлен без изменений. GENERATE/IMPROVE/AUDIT/EXPLORE, source preservation, target capability boundaries и conditional reference loading согласованы. Нет оснований для искусственного rewrite.

## Статический walkthrough

- Prompt injection в анализируемом тексте: supplied prompt — data, embedded domain instructions не исполняются; user request и input разделены.
- Unknown platform: portable prompt без invented browsing/tools/files/delegation, platform question не обязателен если portable deliverable достаточен.
- Missing critical input: focused blocking question и ожидание реального ответа; nonblocking gap → explicit assumption/input slot, без выдуманного согласования.
- AUDIT only: critique с exact wording/evidence, без unsolicited revised prompt; numeric score только по запросу и без runtime claims.
- Mixed language: requested language/format соблюдены; identifiers/URLs/citations сохранены. В reference нет конкурирующего language rule.
- Agent template: failure/stop/action boundaries не дают новых прав и не запускают downstream task; research только для missing/current facts, от которых зависит prompt construction.

Quick_validate успешно; YAML/fences/relative links проверены. Git diff --check проходит для отчёта.
Ограничения: self-review walkthrough, не independent LLM execution и не оценка effectiveness target-model output. Все выводы статические.
