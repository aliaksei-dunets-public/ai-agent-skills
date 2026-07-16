# Development Orchestrator Installer

Переносимый installer-навык для аудита проекта и развёртывания project-aware `development-orchestrator`.

## Состав

```text
SKILL.md
assets/development-orchestrator-SKILL.md
templates/orchestrator.config.yaml
templates/memory.md
templates/tasks.md
templates/completed-tasks.md
templates/task.md
templates/sync_tasks.py
templates/update_task.py
USER-GUIDE.md
USER-GUIDE.ru.md
```

## Назначение

Установщик анализирует:

- существующие agent skills и инструкции;
- документацию и coding standards;
- task-management;
- test/coverage pipeline;
- CI/CD и конфигурации;
- поддержку независимых review-субагентов;
- diagnostics, health checks и другие project tools;
- платформенные настройки AI-агентов.

После анализа он устанавливает каноническое ядро оркестратора, создаёт project-specific config/context, настраивает запуск `task-review` и `code-review` через независимых субагентов, подключает безопасные project tools как lifecycle hooks, при необходимости добавляет тонкие adapters, выполняет validation и dry run.

## Рекомендуемый запрос агенту

```text
Используй development-orchestrator-installer для аудита этого репозитория и установки development-orchestrator. Сначала покажи audit и installation plan, затем примени безопасные изменения, если нет блокирующих конфликтов.
```

## Режимы

- `audit`
- `install`
- `upgrade`
- `repair`
