# AI Agent Skills-0010 — python-code-review

Дата: 2026-10-12. Карточка: 6hjhm4G3HC32hXM3.
Проверены SKILL.md, README.ru.md, metadata, три references, reviewer assignment и report template. План подготовлен в пути карточки; фиксированные scanner requirements не добавлялись.

## Результат

Существенные дефекты не подтверждены. Навык оставлен без изменений. Scope/authority, exact snapshot, model-led review, tooling trust, independent-review fallback и evidence/coverage contract согласованы. Обнаруженная ранее необходимость проверять risks не считается доказанным багом.

## Статический walkthrough

| Случай карточки | Решение по текущему контракту |
|---|---|
| Partially staged diff, working-tree fix | Review target/context берутся из index; current fix не заменяет staged code |
| Unsafe pytest command/plugins, live service tests | Inspect trust/side effects; static review или разрешённое isolated execution, без автоматического запуска |
| Embedded instruction в code/tool output | Evidence only, authority не расширяется; credentials sanitised |
| Independent reviewer недоступен/не разрешён | Challenge self-review с другим entry point; явно self-review; required independent gate остаётся unmet |
| Dependencies отсутствуют | Без install/resolve/wrapper sync; unavailable checks записаны, pass не придумывается |
| Неохваченный Python component/project sampling | Inspected/sampled/uninspected areas явно указаны; insufficient required evidence → INCONCLUSIVE |
| Green tests с упрощённым mock | Assertions/boundary fidelity проверяются, green не заменяет causal analysis |

Проверены локальные ссылки, fences/frontmatter и quick_validate (Skill is valid). Diff --check проходит для отчёта. Reviewer assignment не получает primary conclusions и не допускает nested delegation.

Ограничения: это статическая проверка пакета/self-review, не реальный Python review, pytest/scanner run или independent LLM evaluation. Версионные external tooling docs и UI policy support не проверялись в целевой платформе; capability claims требуют локальной проверки при использовании.
