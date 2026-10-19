# AI Agent Skills-0002 — abap-doc-writer

Дата: 2026-10-12. Карточка: 6hjhm4PPr4fFcj3V.
Проверены SKILL.md, CONFIG_TEMPLATE.md, references/abap-doc-rules.md и связанный README подмодуля.
Локального плана не было; подготовлен план с критериями приёмки в пути карточки.

## Находки и исправления

- High, SKILL.md Phase 3/5: виртуальный URI превращался в «local path» без подтверждённого mapping. Теперь обязательна проверенная цель; без неё возвращается patch / NOT WRITTEN.
- High, Phase 5: полная перезапись без контроля baseline. Введены минимальный patch, защита revision во время записи, reread, проверка non-comment bytes и безопасное восстановление. Ошибка записи больше не объявляется гарантией неизменности файла.
- Medium, abap-doc-rules.md §4/5: update мог заменять объяснение по именам. Изменения теперь опираются на исходник/требования, неизвестные факты не выдумываются.
- High, Phase 5: INTF разрешён в Phase 3, но исключён из записи. Разрешён .intf.abap; реализация остаётся read-only.
- Medium, Phase 4: method-only scope мог менять class doc. Class doc ограничен whole-object scope; неоднозначные цепочки оставляются без записи.

## Проверка

Статический walkthrough: read-only ADT URI → patch; concurrent edit → conflict/stop; multi-include read failure → gap без записи; malformed chain → NOT WRITTEN; protected links/shorttext → сохранение; Unicode/newlines → проверка bytes; write failure → observed/unknown state без слепого rollback. Git diff --check выполнен успешно.

Ограничения: SAP/ADT/IDE, реальная гонка и выполнение ABAP не проверялись; это исправление контракта инструкций, не реализация нового write API. Runtime guarantees зависят от доступного инструмента; при отсутствии безопасного API возвращается patch.
