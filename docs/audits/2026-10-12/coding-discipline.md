# AI Agent Skills-0011 — coding-discipline

Дата: 2026-10-12. Карточка: 6hjhm47xg5WmH3CV.
Прочитаны оба файла пакета: SKILL.md и agents/openai.yaml. План подготовлен в пути карточки вместо отсутствовавшего локального файла.

## Результат

Существенных дефектов нет; навык оставлен без изменений. «Smallest coherent change» прямо сохраняет correctness/security/compatibility и required safeguards; abstraction не запрещена по single-use. Правила не вводят дополнительную approval ceremony и не скрывают непройденные проверки.

## Статический walkthrough

- Маленький bug fix: только required behavior и affected callers; low-impact check вместо зеркального теста. Regression test добавляется когда practically valuable, а не ради процесса.
- Несколько интерфейсов: связанные callers/tests/config/docs входят в coherent change; unrelated cleanup исключён. Security/validation не удаляются ради уменьшения строки/объёма.
- Тесты с live/external effects: trusted existing checks выбираются по scope; dependency install/env changes/external destructive actions не получают автоматическую авторизацию.
- Pre-existing failure: отделяется от regression, unrun checks не объявляются pass; дальнейшее testing только при изменениях/новом evidence.
- Ясная reversible implementation choice: не требует design ceremony; действительно material scope/compatibility decision остаётся вопросом.

Quick_validate успешно; frontmatter, metadata YAML и fences проверены. У пакета нет локальных Markdown reference links. Diff --check проходит.
Ограничения: walkthrough инструкций — self-review, не выполнение кодовой задачи и не independent LLM evaluation. Наблюдаемое улучшение поведения/экономия токенов не заявляются.
