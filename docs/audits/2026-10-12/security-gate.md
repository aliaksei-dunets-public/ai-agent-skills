# AI Agent Skills-0009 — security-gate

Дата: 2026-10-12. Карточка: 6hjhm4Fxqhwvvvc3.
Проверены SKILL.md, все шесть references, README, metadata, два setup templates и три eval documents. План создан в пути карточки; критерии не требуют запускать проверяемый security workflow или устанавливать сканеры.

## Результат

Существенные дефекты инструкций не подтверждены. Навык оставлен без изменений; зафиксирован audit-only результат. FAIL/WARN/PASS согласованы с coverage, confidence и exact snapshot. Unavailable/crash не становится PASS, private data redacted, credential live validation запрещена, setup templates не устанавливаются при review.

## Статический walkthrough сценариев

| Сценарии из evals/scenarios.md | Решение по текущим инструкциям |
|---|---|
| 001, 005, 013 | Injection оценивается в index/historical snapshot; current fix не очищает staged gate |
| 002 | Placeholder не live secret; effective constant signing key требует отдельной оценки, redaction и FAIL |
| 003 | JSX text не XSS; complete applicable coverage → PASS, missing scanner → WARN |
| 004, 009, 015 | Existing/project components и release material в full scope; no Git не останавливает audit; partial coverage явно указана |
| 006 | Empty staged → WARN; unborn/deletion-only не empty scope |
| 007 | Exact affected version/advisory отдельно от reachability; unresolved manifest не создаёт фиктивный CVE/version |
| 008 | Parse error/no scanner/no DB cache → WARN, а не zero findings PASS |
| 010 | Project FAIL + staged PASS → overall FAIL; pre-existing issue вне narrow attribution |
| 011 | Embedded instructions/plugin не запускаются; packaging risk исследуется без raw secret upload |
| 012 | Medium/Low сохраняются, scanner hypothesis отдельно от confirmed |
| 014 | Unmerged/LFS/gitlink/symlink/changing index → gaps, stale evidence не clean |
| 016 | Два независимых High — две причины; правильный FAIL не оправдывает пропущенный blocker |

Это self-review walkthrough текстовых случаев, а не запуск fixtures/сканеров или независимая оценка. Trigger boundary, setup opt-in и criteria также сверены. Frontmatter/fences/local links проверены; diff --check проходит.

Ограничения: public-source URLs, scanner versions/flags, advisory freshness, hook execution и target-model behavior не перепроверялись в интернете/runtime. Они требуют проверки при фактическом использовании, как уже требует tooling.md. Security audit самого проекта не выполнялся.
