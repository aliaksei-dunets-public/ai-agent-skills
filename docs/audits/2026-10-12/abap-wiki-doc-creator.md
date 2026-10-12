# AI Agent Skills-0003 — abap-wiki-doc-creator

Дата: 2026-10-12. Карточка: 6hjhm4RjCPJpWMx3.
Проверены SKILL.md, CONFIG_TEMPLATE.md, все три references и README подмодуля.
Локального плана не было; создан план аудита и исправлений в пути карточки.

## Находки и исправления

- High, Phase 3: бизнес-контекст выводился из имён. Теперь факты имеют source pointers, бизнес-требования берутся из supplied docs, гипотезы маркируются; неизвестное не заменяется выдуманным назначением.
- High, UPDATE step 5: устранена двусмысленность обхода review gate. HTML создаётся после подтверждения либо в пределах уже явно данного разрешения.
- Medium, Phase 2: недоступный объект блокировал остальные чтения. Разрешено продолжать независимые чтения; частичная генерация требует разрешения и маркировки PARTIAL с перечнем gaps.
- Medium, Phase 3/diagram-guide/html-template: JOIN выдавался за FK, префикс view мог стать наследованием, сигнатура — flow. Отделены наблюдаемые связи, query relations и гипотезы; шаблон не доказывает архитектуру.
- Medium, UPDATE: changed-only не доказывает актуальность скопированных разделов, а имя с сегодняшней датой могло перезаписать предыдущий результат. Добавлены not revalidated и unique suffix.
- Medium, html-template: source/PlantUML должен выводиться как escaped text. Указаны escaping, проверка anchors/participants и сохранение coverage в HTML.
- Low, object-sort-order: исправлены устаревшие номера фаз.

## Проверка

Статический walkthrough: absent business requirements → unknown; missing source → gap, complete waits/authorized partial; UPDATE → тот же gate; changed-only → copied sections not revalidated; sorting → canonical type/name; TOC → проверка targets; PlantUML → только source-backed relations и escaped text. Frontmatter/fences/local reference integrity проверены; diff --check проходит.

Ограничения: фактическая HTML-генерация, PlantUML-renderer и SAP/IDE не запускались. Независимого LLM-прогона не было.
