# AI Agent Skills-0005 — abap-unit-test-creator

Дата: 2026-10-12. Карточка: 6hjhm4H6g3v7rpx3.
Проверены SKILL.md, CONFIG_TEMPLATE.md, все пять references и девять examples. План подготовлен в пути карточки вместо отсутствовавшего локального файла.

## Находки и исправления

- Medium, Step 7: «until green» не ограничивал цикл исправлений. Введены один исходный запуск и максимум два correction/re-run; production defect, stale contract, environment/API/isolation failure останавливают цикл. Нельзя ослаблять assertions или менять production без запроса.
- Medium, isolation/RAP: LOCAL MODE и rollback не доказывают отсутствие productive DB/external effects. Добавлена проверка target/revision, dependency doubles, setup order и teardown перед запуском; непроверенная изоляция → not executed.
- Medium, interface-fake example: переменная типа интерфейса затем читала call_count, объявленный только на concrete fake. Тип ссылки исправлен на local fake; injection сохраняет production interface contract.

## Проверка

Статический walkthrough: missing seam → blocker; SQL double unavailable → not executed; draft EML → требуется actual BDEF/isolation; production contract changed → stop/re-read; generated-test failure → bounded corrections; env failure → stop; fake call_count доступен через concrete reference. Non-production edits и существующие testability controls сохранены. Git diff --check проходит.

Ограничения: SAP compilation/ABAP Unit и фактическая изоляция на системе не проверялись. Версионные API примеров требуют проверки на целевой системе; статическое чтение не выдаётся за pass/runtime evidence. Независимого LLM-прогона не было.
