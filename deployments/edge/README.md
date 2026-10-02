# Edge Deployment Manifests & Contracts (Stage 1 Steady State)

Данный каталог содержит санитизированные, непосредственно применимые deployment-манифесты и переопределения (overrides), зафиксированные в рамках **Stage 1 (PostgreSQL Consolidation & Service Normalization)** на production-узле `edge`.

Все секреты и пароли отделены от репозитория и управляются через `.env` или Secret файлы на хосте с правами `0600`/`root`.

---

## Соответствие путей в Runtime

| Сервис / Компонент | Манифест в Canonical Repo | Фактический путь на узле `edge` | Описание |
| :--- | :--- | :--- | :--- |
| **PostgreSQL 18** | `deployments/edge/postgres/compose.yaml` | `/opt/postgres/compose.yaml` | Единый сервис PostgreSQL 18 для Nextcloud, Mattermost и Plane |
| **PostgreSQL Init** | `deployments/edge/postgres/init/01-init.sh` | `/opt/postgres/init/01-init.sh` | Инициализация баз, ролей без elevated privileges и расширений |
| **PostgreSQL Env** | `deployments/edge/postgres/.env.example` | `/opt/postgres/.env` | Шаблон переменных окружения и учетных данных баз |
| **Mattermost** | `deployments/edge/mattermost/docker-compose.edge.yml` | `/opt/mattermost/docker-compose.edge.yml` | Edge-override: отключение embedded postgres, монтирование внешней `postgres_net` |
| **Nextcloud** | `deployments/edge/nextcloud/compose.yaml` | `/opt/nextcloud/compose.yaml` | Стек Nextcloud (app, cron, redis) с подключением к единому PostgreSQL |

---

## Архитектурные принципы Stage 1

1. **Единый PostgreSQL 18 (`postgres`)**:
   - Сервис работает в контейнере `postgres:18`, данные хранятся в `/srv/postgres` (`/var/lib/postgresql`).
   - Изолированная внешняя Docker-сеть `postgres_net`. Порт PostgreSQL на внешний интерфейс хоста не публикуется.
   - Раздельные базы данных (`mattermost`, `nextcloud`, `plane`) и выделенные непривилегированные роли. Plane Part 1 добавляет DB/роль отдельно по `deployments/plane/README.md`; его секреты остаются в Plane env и не добавляются в immutable Env общего postgres.
2. **Чистота Upstream Repositories**:
   - Upstream-репозиторий `/opt/mattermost` (`main`) сохраняется в абсолютно чистом состоянии (tracked files соответствуют `origin/HEAD`).
   - Все кастомизации вынесены в файлы переопределений: `docker-compose.edge.yml`.

## Interaction/AI tool and Nextcloud automation foundation — 2026-10-02

Canonical contract: [interaction-fabric/README.md](interaction-fabric/README.md). Native n8n exports and secret-free client definitions accompany the two one-shot helpers. Nextcloud app and cron join existing edge_internal (app alias nextcloud.edge.internal) for native WebDAV/OCS and cron webhook delivery; existing default/postgres networks and public OIDC/HTTPS remain. No added persistent service/network. Consolidated acceptance: `EDGE_INTERACTION_AI_TOOL_FABRIC_ACCEPTANCE_2026-10-02.md` at repository root.
