# Edge Deployment Manifests & Contracts (Stage 1 Steady State)

Данный каталог содержит санитизированные, непосредственно применимые deployment-манифесты и переопределения (overrides), зафиксированные в рамках **Stage 1 (PostgreSQL Consolidation & Service Normalization)** на production-узле `edge`.

Все секреты и пароли отделены от репозитория и управляются через `.env` или Secret файлы на хосте с правами `0600`/`root`.

---

## Соответствие путей в Runtime

| Сервис / Компонент | Манифест в Canonical Repo | Фактический путь на узле `edge` | Описание |
| :--- | :--- | :--- | :--- |
| **PostgreSQL 18** | `deployments/edge/postgres/compose.yaml` | `/opt/postgres/compose.yaml` | Единый сервис PostgreSQL 18 для Nextcloud, Mattermost и OpenProject |
| **PostgreSQL Init** | `deployments/edge/postgres/init/01-init.sh` | `/opt/postgres/init/01-init.sh` | Инициализация баз, ролей без elevated privileges и расширений |
| **PostgreSQL Env** | `deployments/edge/postgres/.env.example` | `/opt/postgres/.env` | Шаблон переменных окружения и учетных данных баз |
| **Mattermost** | `deployments/edge/mattermost/docker-compose.edge.yml` | `/opt/mattermost/docker-compose.edge.yml` | Edge-override: отключение embedded postgres, монтирование внешней `postgres_net` |
| **OpenProject** | `deployments/edge/openproject/docker-compose.override.yml` | `/opt/openproject/docker-compose.override.yml` | Override: отключение db и hocuspocus, монтирование внешней `postgres_net` |
| **OpenProject Caddy** | `deployments/edge/openproject/caddy/Caddyfile` | `/opt/openproject/caddy/Caddyfile` | Чистый Caddy reverse proxy без несуществующего upstream hocuspocus |
| **Nextcloud** | `deployments/edge/nextcloud/compose.yaml` | `/opt/nextcloud/compose.yaml` | Стек Nextcloud (app, cron, redis) с подключением к единому PostgreSQL |

---

## Архитектурные принципы Stage 1

1. **Единый PostgreSQL 18 (`postgres`)**:
   - Сервис работает в контейнере `postgres:18`, данные хранятся в `/srv/postgres` (`/var/lib/postgresql`).
   - Изолированная внешняя Docker-сеть `postgres_net`. Порт PostgreSQL на внешний интерфейс хоста не публикуется.
   - Раздельные базы данных (`mattermost`, `nextcloud`, `openproject`) и выделенные непривилегированные роли.
2. **Чистота Upstream Repositories**:
   - Upstream-репозитории `/opt/mattermost` (`main`) и `/opt/openproject` (`stable/17`) сохраняются в абсолютно чистом состоянии (tracked files соответствуют `origin/HEAD`).
   - Все кастомизации вынесены в файлы переопределений: `docker-compose.edge.yml` и `docker-compose.override.yml`.
3. **Отключение Hocuspocus / Real-time Collaboration**:
   - Hocuspocus отключен на уровне Compose-профиля (`profiles: [disabled]`).
   - В OpenProject форсирован параметр `OPENPROJECT_REAL__TIME__TEXT__COLLABORATION__ENABLED="false"`.
