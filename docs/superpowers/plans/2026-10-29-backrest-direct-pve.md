# Прямой бэкап Edge в существующий PVE/D5 — план внедрения

> **For agentic workers:** выполнять последовательно в исходном чате через `executing-plans`. Этот документ задаёт план; runtime ещё не переключён. Делегирование и отдельный новый чат для внедрения не требуются.

**Goal:** убрать повторное создание полного локального Restic-репозитория на Edge, сохранив существующий репозиторий PVE, историю снимков и действующую серверную retention.

**Architecture:** Backrest на Edge выполняет online preparation и сразу пишет Restic backup в существующий append-only REST endpoint CT208. Последний снимок с прежними тегами служит parent; CT208 продолжает обслуживать тот же репозиторий локально. На Edge остаются кэш Restic и временные подготовленные данные приложений.

**Tech Stack:** Backrest 1.14.1, commit `875c9cb51e626a75276a64da42c6a9ec0695010a`; Restic 0.19.1; существующие REST credentials, native GetConfig/SetConfig и hooks.

**Spec:** запрос оператора в [исходном чате](codex://threads/01a18528-4577-7731-8813-a1195986700b); результат read-only проверки CT208 в [«Аудировать Backrest на PVE»](codex://threads/01a1851e-9918-7210-8902-f6e16c969a6c), turn `01a1854d-e130-7491-a3e3-25c77889cb77`; `OPERATING_RULES.md`, `AGENTS.md`, `backup/edge/README.md`. Более старые Stage 6 records описывают историческую топологию local → copy и не разрешают возврат к остановке приложений.

**Статус:** план завершён; внедрение, реальные новые backup/restore и удаление объектов по этому плану не выполнялись. Проверка CT208 прочитана из указанного чата; Edge config и runtime helpers дополнительно сверены непосредственно. Все времена ниже — Москва, UTC+3. Документ не меняет системные timezone.

## Global Constraints

- Не останавливать, не перезапускать и не приостанавливать приложения, контейнеры или пользовательские задачи ради backup.
- Сохранить текущие источники, исключения, расписания, instance и ID обоих планов.
- Не выполнять `init`, изменение chunker config, перенос истории, `tag`, `rewrite`, `repair` или принудительный `--force` для перехода.
- Не выполнять `forget/prune/tag` через append-only endpoint Edge → PVE. Retention принадлежит CT208.
- Не менять CT208 retention, проверки, ACL, Home knowledge или AI Node в рамках перехода.
- Не удалять исторические снимки ради внедрения. После перехода действует прежняя штатная retention, а не бессрочное хранение всех снимков.
- Секреты использовать из существующих защищённых файлов; не включать их в Git, журналы, аргументы shell или публикуемый diff.
- Не затрагивать несвязанные dirty changes рабочего дерева. Итог внедрения сохранять напрямую в `main`, только после проверок, с push/readback.

## Review Focus

| Условие | Требуемое поведение и проверка |
|---|---|
| Endpoint указывает не на прежний репозиторий или нет ожидаемого parent | До запуска backup сверить repository ID и последние снимки по тегам; при несовпадении остановить переход без init/fallback |
| Разные chunker parameters и изменившиеся inode/ctime staged-файлов | Переиспользовать неизменённые файлы через parent; отдельно учитывать новые блоки перечитанных файлов; не включать ignore-ctime/ignore-inode для искусственного уменьшения отчёта |
| Сбой PVE, частичный backup или сбой проверки снимка | Сохранить текущую staging generation; не объявлять flow успешным; не создавать локальную полную цепочку как скрытый fallback |
| Новая или занятая staging generation во время финализации старого снимка | Не удалять её; отдельный тест на busy lock, более новую generation и symlink |
| Изменение тегов, hostname или native retention defaults | Сравнить config до/после и фактический argv; не создавать новые группы retention и не запускать обслуживание удалённого repo с Edge |

## 1. Подтверждённый baseline

### Репозиторий и планы

| Объект | Подтверждённое значение |
|---|---|
| REST endpoint Edge | `rest:http://192.168.1.14:8000/edge/` |
| Локальное представление на CT208 | `/srv/backrest-storage/repositories/edge`, Backrest repo ID `edge-d5` |
| Restic repository ID | `e293ee008a257664a7e568787463a9cbab5d0573daf53c5ebd92477d1960cec7` |
| Chunker parameters | Конфигурации прочитаны; PVE, прежний local State и прежний local Knowledge используют разные polynomial. Значения не публикуются; конфигурация PVE остаётся существующей |
| Edge instance / текущий hostname | `edge` / `edge` |
| State plan / tags | `edge-state`; `plan:edge-state`, `created-by:edge` |
| Knowledge plan / tags | `edge-knowledge-local`; `plan:edge-knowledge-local`, `created-by:edge` |
| State schedule | `0 1,7,13,19 * * *`, `CLOCK_LOCAL` |
| Knowledge schedule | `0 4,10,16,22 * * *`, `CLOCK_LOCAL` |

На момент проверки Edge `config.modno=5`. Это значение не использовать вслепую при внедрении: новый SetConfig обязан использовать свежий modno. Runtime `/usr/local/sbin/edge-state-prepare` и `/usr/local/libexec/edge-tier-evacuate.py` совпадают с их source в `backup/edge/` по SHA-256.

Ориентир расхода места: последний State backup записал в пустой local repo 21 800 911 041 байт до сжатия и 11 445 486 379 байт packed. REST listing PVE показывал 42 328 785 655 байт data packs, около 39,42 GiB, для всей истории Edge. Эти цифры не являются измерением сетевого трафика или будущего прироста прямого backup.

### Retention на CT208

`/usr/local/sbin/d5-edge-maintenance` запускает native Restic с:

```text
forget --keep-daily 30 --keep-weekly 8 --keep-monthly 6
       --group-by host,tags --prune --retry-lock 10m
```

Нет фильтров host/tag/path. Область действия — весь репозиторий; отдельная группа для каждого hostname и полного набора тегов. Порядок тегов не создаёт другую группу. Это объединение календарных корзин, а не фиксированные 44 снимка или удаление через 30 дней. Старые группы `edge.escloud.us` сохраняют собственные корзины; их не переименовывать и не объединять для перехода.

Check назначен на воскресенье 05:30, structural-only. Только его `CONDITION_CHECK_SUCCESS` запускает maintenance. Отдельные scheduled forget/prune отключены. Последний подтверждённый flow 25.10.2026: check 1407, hook 1499, `STATUS_SUCCESS`; hook 05:32:01–05:34:58. Сохранены 31 State + 1 acceptance, удалены 48 State. Restic сообщил `total prune: 2.956 GiB`; независимого `df`-замера нет. Knowledge в этом старом запуске не было.

Следующий check в срезе CT208 — операция 1500, 01.11.2026 05:30. Maintenance выполнится после успешной проверки; ошибка check не запустит cleanup.

Native локальный CT208 dry-run от 29.10.2026 ничего не удалил:

| Hostname | Plan/tag group | Сейчас | Оставил бы | Удалил бы |
|---|---|---:|---:|---:|
| `edge.escloud.us` | `edge-state` | 63 | 32 | 31 |
| `edge.escloud.us` | `edge-knowledge-local` | 146 | 32 | 114 |
| `edge` | `edge-state` | 6 | 3 | 3 |
| `edge` | `edge-knowledge-local` | 8 | 4 | 4 |
| `edge.escloud.us` | `weblate-deployment-acceptance` | 1 | 1 | 0 |
| Всего | | 224 | 72 | 152 |

Числа описывают этот срез, не команду на удаление. Прирост новых снимков изменит результат следующего обслуживания. Удаление 152 metadata records не означает освобождение 152 полных копий: объём освобождаемых packs здесь неизвестен.

Все 223 ID из предшествующего аудита сохранились; появился Knowledge-снимок 29.10 04:00. До/после dry-run набор ID одинаков. Это доказательство сохранности metadata, не полная проверка всех исторических данных.

## 2. Механизм перехода при разных chunker parameters

Оставить PVE repository ID, ключи, config и packs на месте. Не копировать снимки повторно и не создавать второй репозиторий для «выравнивания» parameters.

В установленном Backrest `SnapshotsForPlan` выбирает записи по двум прежним тегам; `Backup` передаёт последний snapshot ID как `--parent`. Поэтому сохранение plan IDs и instance даёт продолжение существующей истории штатным механизмом. Дополнительный permanent `--parent` не нужен и закрепил бы устаревший снимок.

Restic сравнивает metadata файлов с parent. У неизменённого файла он переиспользует прежний список content blobs, включая блоки, скопированные из репозитория с другим polynomial. Файлы, которые Restic считает изменёнными, перечитываются с PVE polynomial: для крупных файлов это может один раз добавить существенно больше, чем объём изменённых байтов. Последующие изменения используют PVE chunking. Полный `--force`, обновление всех timestamps или смена всех путей лишили бы переход этого преимущества.

Ранее в этом чате выполнен disposable тест установленного Restic 0.19.1: два файла по 4 MiB, разные independently initialized polynomial, copy в destination, затем direct backup с copied parent. Без изменений: 0 data blobs, 287 packed bytes metadata. После изменения 64 байт одного файла: один другой файл переиспользован, около 4 MiB packed добавлено для изменённого. Следующий неизменённый запуск снова дал 0 data blobs. Test directories удалены. Это доказательство механизма, не прогноз экономии production.

Пересоздаваемые pg_dump/SQLite/staging files имеют новые metadata и могут перечитываться. Не устранять это через `--ignore-ctime`, `--ignore-inode`, ручное выравнивание metadata или изменение форматов dumps в данном переходе. Фактический объём определить по production backup, отдельно от total bytes processed.

Последние известные parent-кандидаты: State `b7aaeab05f97d5fdfc9178a081835b5d02a3ae699d087ecd01c5e007afeb8ad3`, Knowledge `c07dd39d2dfc848b2d55397de7c86e29f8303f8018689685cae5a8f47e0a84be`. Они являются свидетельствами среза; перед переключением прочитать актуальные записи.

## 3. Целевая конфигурация Edge

Добавить native Backrest repo с новым локальным UI ID `edge-pve`, указанными endpoint и существующим Restic GUID. Это новая запись конфигурации Edge, а не новый физический репозиторий. `autoInitialize=false`, `autoUnlock=false`; native repo `checkPolicy`, `prunePolicy` и `forgetPolicy` schedules явно disabled. Retention обоих планов оставить `policyKeepAll=true`: native per-plan forget в 1.14.1 иначе может запускаться даже при disabled repo forget schedule.

Credentials взять из `/etc/backrest/edge-d5.env` и `/etc/backrest/edge-d5-password`. В repo.env использовать `RESTIC_PASSWORD_FILE=/etc/backrest/edge-d5-password`, очистить альтернативные `RESTIC_PASSWORD`/`RESTIC_PASSWORD_COMMAND`, а существующие REST username/password передать в native repo.env внутри защищённого config. Поле repo.password оставить пустым. Не использовать `${VAR}` для отсутствующих переменных окружения Backrest-процесса и не добавлять systemd environment/restart ради credentials. Все чувствительные SetConfig payloads держать в памяти или защищённом temporary recovery context, не печатать.

Кэш оставить `/root/.cache/restic`, явно выбрав этот путь для нового repo. Он уже существует, на момент проверки около 50 MiB, и исключён State правилом `/root/.cache/**`. Это metadata/tree cache, не полная локальная backup chain; будущий размер измерить, не обещать фиксированный предел. Для конкуренции с штатным обслуживанием PVE использовать существующую native семантику `--retry-lock 10m`.

Перепривязать оба существующих плана к `edge-pve`. Сохранить paths/excludes/schedules, текущий hostname и instance, поля backup flags и `skipIfUnchanged`. Не добавлять переходных тегов. Не переименовывать `edge-knowledge-local`: его имя входит в исторический тег, а переименование потребовало бы отдельной миграции.

У State оставить start-hook `/usr/local/sbin/edge-state-prepare`. Success-hook copy/evacuate заменить на финализацию только конкретной generation после readback прямого snapshot. Knowledge success-hook evacuation удалить: у него нет State staging.

В исследованном коде установленной версии поле `skipIfUnchanged` само по себе не превращается в аргумент `--skip-if-unchanged`. Переход не исправляет эту отдельную семантику: новый маленький snapshot record с повторными content blobs не является полной копией. Добавление фактического skip требует согласования с monitor freshness, который сейчас ориентируется на успешные записи с непустым snapshot ID; не включать его незаметно в этот переход.

## 4. Последовательность внедрения и проверок

### Task 1 — свежий baseline и ограниченный recovery context

**Файлы/интерфейсы:** native GetConfig, `/var/lib/backrest/config.json`, оба local repo, `/etc/backrest/edge-d5.env`, `/etc/backrest/edge-d5-password`; мутации пока не требуются.

- [ ] Проверить отсутствие in-progress backup/hook/prune и выбрать время вне подтверждённого maintenance CT208. Не прерывать занятые операции.
- [ ] Через existing credentials прочитать `cat config` и `snapshots --json` PVE без lock/cache; сверить полный repository ID. Зафиксировать список исторических ID и ключевых полей tree/time/hostname/paths/tags/original, актуальные latest parents обоих планов.
- [ ] Убедиться, что оба latest parent имеют нужные теги, ожидаемые пути и доступны через endpoint; сверить их с native Backrest выборкой после регистрации repo. Отсутствующий parent — основание исправить обнаружение до backup, а не запускать без него.
- [ ] Проверить local snapshots. Если после baseline появились непереданные снимки, завершить существующий проверенный transfer до переключения и повторить manifest. Непереданные local snapshots не удалять. Не запускать copy заведомо уже присутствующей истории ради перехода.
- [ ] Снять свежий GetConfig с modno, hashes и mode/owner затрагиваемых helpers/config. Сохранить маленький закрытый rollback context в `/tmp` с mode 0700, secret files 0600; packs и историю туда не копировать. В Git хранить только nonsecret изменения.

**Результат:** доказана identity существующего repo и latest parents, нет неучтённой локальной истории, известен точный обратный config diff.

### Task 2 — безопасная финализация staging и native переключение

**Изменяемые source:** `backup/edge/edge-state-plan.json`, `backup/edge/README.md`.
**Новый source:** `backup/edge/edge-state-finalize` и `backup/edge/test_direct_finalize.py`.
**Runtime:** `/usr/local/sbin/edge-state-finalize`, root:root 0755; native Backrest config через GetConfig/SetConfig.

**Интерфейс финализатора:** один positional full snapshot ID; credential source — существующий `/etc/backrest/edge-d5.env`. Он читает именно этот snapshot из проверенного PVE repo, сверяет ID, `plan:edge-state`, `created-by:edge`, hostname и paths; никогда не выполняет backup/copy/forget/prune. Из remote time берёт cutoff и применяет существующий принцип `clean_staging`: lock `/run/lock/edge-state-prepare.lock`, фиксированный `/var/lib/backrest-staging/edge-state/current`, отказ от symlink, удаление только generation с ctime не позднее начала сохранённого snapshot. Новый/занятый current не удаляется; ошибки readback оставляют staging и дают видимую ошибку hook.

- [ ] Написать meaningful isolated regression tests: успешный exact readback удаляет старую generation; missing/mismatched ID/repo/tag/host/path сохраняет её; warning/error не вызывает финализацию; newer generation, busy lock и symlink не удаляются. Подмена Restic в тесте запрещает любые mutating subcommands. Повторный readback/cleanup после уже удалённого current идемпотентен.
- [ ] Выделить финализацию из прежнего evacuation helper, сохранив generation/lock защиту; существующий online prepare не менять. Hook использует native template `{{ .ShellEscape .SnapshotId }}`, не предполагаемые environment variables.
- [ ] Прогнать regression tests и существующие online-prepare tests; проверить синтаксис итогового helper и реально отрендеренного command hook. Shell payloads, предназначенные оператору, отдельно проверить `bash -n` по точному финальному тексту.
- [ ] Установить финализатор, затем применить один согласованный native SetConfig со свежим modno: добавить `edge-pve`, перепривязать два плана, убрать evacuation hooks, поставить State success-finalize с `ON_ERROR_FATAL`, отключить scheduled check/prune/forget старых local repo entries. Backrest не перезапускать. Не переписывать весь config по старому файлу и не менять auth.
- [ ] Прочитать GetConfig заново. Проверить diff разрешённых полей; сравнить source selection, расписания, instance, retention, flags. Убедиться в отсутствии Edge maintenance tasks для PVE. Native parser/SetConfig validation обязательны; generic JSON syntax check их не заменяет.

**Результат:** непосредственная запись обоих планов в существующий PVE repo, без потери online preparation и очистки staging.

### Task 3 — первый и повторный direct backup, чтение данных

**Интерфейсы:** native Backrest Backup/GetOperations/GetLogs, read-only Restic snapshot/list/dump и isolated restore в `/tmp`.

- [ ] Запустить по одному реальному native backup обоих планов. Не обходить hooks прямым backup CLI для приёмки. Сопоставить фактический `--parent` с актуальным preflight manifest. `files_unmodified` и readback должны подтвердить переиспользование подходящих неизменённых файлов; synthetic тест сам по себе этого не доказывает.
- [ ] Сравнить PVE manifest до/после: все прежние ID и metadata сохранены, добавились только ожидаемые прямые snapshots; у новых снимков прежние plan/instance tags, hostname `edge`, правильные paths/excludes и ожидаемый parent. Не требовать поле `original` у direct snapshot: оно относится к истории copy.
- [ ] Проверить успех полного flow, включая State finalizer. Успешная backup-запись при упавшем финализаторе недостаточна. Убедиться, что current удалён только для сохранённой generation.
- [ ] Прочитать выбранные старые и новые файлы из snapshot в isolated `/tmp`: сравнить SHA-256 неизменённого контрольного файла, выбранного по фактическому inventory; проверить наличие staged DB artifacts. Для восстановленных PostgreSQL dumps выполнить `pg_restore -l`, для SQLite — offline `integrity_check` на временной копии. Production DB и файловую систему не перезаписывать. После сохранения sanitized результатов временные восстановленные данные удалить.
- [ ] Выполнить повторный native State backup, чтобы проверить parent уже прямого снимка. Не изменять production файлы ради теста и не требовать нулевой записи при продолжающейся работе приложений. Knowledge также проверить повторно без изменения источника; учитывать существующее поведение skip поля.
- [ ] Отдельно записать `total_bytes_processed`, `files_new/changed/unmodified`, `data_added`, `data_added_packed`, длительность и прирост суммарных размеров PVE data packs по REST API v2 до/после окна. Обслуживание/другие writers делают такой delta неатрибутируемым — это обозначить, а не превращать в оценку трафика. Для traffic нужен отдельный достоверный счётчик; без него traffic остаётся UNKNOWN.
- [ ] Проверить offline/missing-readback/newer-generation сценарии на изолированном тесте; не разрывать рабочий NetBird/PVE канал ради эксперимента. При недоступности PVE backup должен сообщить ошибку, staging остаётся ограниченной текущей generation; prepare уже ограничивает next/current/previous lifecycle. Полноценной локальной очереди исторических снимков в прямой схеме нет.
- [ ] Проверить Edge Monitor freshness обоих прежних plan IDs и не-регрессию backup service и приложений без рестартов. Проверка выбранных restore artifacts не заменяет полную историческую restore acceptance.

**Результат:** история не потеряна, parent фактически используется в production, первые два цикла и bounded restore проверены. Нулевой прирост, процент экономии, полная читаемость истории или ускорение всего сервиса по этим проверкам не заявляются.

### Task 4 — точечная очистка и persistence

- [ ] До очистки оставить старые repo config entries, маленькие local repos/passwords и helpers как конкретный recovery path текущего перехода. Их schedules отключить, чтобы старый repo check/prune не продолжал выполняться без плана.
- [ ] После успешного Task 3 подтвердить native `snapshots` обоих local repos: пусто. Если есть записи, сначала проверить identity/content соответствующих PVE copies. Зафиксировать категории KEEP/REMOVE и ссылки; удалить только доказанно неиспользуемые local repo entries/directories, локальные passwords и старые deployed `edge-state-tier-copy`, `edge-knowledge-retention`, `edge-tier-evacuate.py`. Учитывать ссылки monitoring/maintenance/rollback; не удалять действующие PVE password/env.
- [ ] Удалить obsolete source helpers/tests, заменив их актуальными direct-finalize tests; Git сохранит историческую реализацию. Не удалять исторические acceptance records.
- [ ] Актуализировать `backup/edge/README.md`, nonsecret plan source и текущие sections `CURRENT_STATE.md`, `IMPLEMENTATION_PHASES.md`, `ARCHITECTURE.md`, `INVENTORY.md`, добавить superseding запись в `DECISIONS.md`. Существующие чужие изменения этих файлов не включать в commit; использовать точечное staging только своих hunks.
- [ ] Проверить отсутствие scheduled local backup/maintenance, evacuation subprocess и новых local packfiles, отсутствие удалённых task artifacts и сохранение активного финализатора/prepare. В `/tmp` убрать собственные временные backup/restore trees и recovery context после приёмки, когда восстановление обеспечено действующим backup и Git. Не создавать `.bak/.old` рядом с production.
- [ ] Прогнать proportionate final checks, `git diff --check`, commit только task-owned изменения напрямую в `main`, push и проверить remote commit плюс критические nonsecret файлы. Зафиксировать реально измеренные bytes и границы доказанного.

## 5. Откат и условия остановки

До финальной очистки восстановить ровно изменённые repo/plan/hook поля через свежий GetConfig/SetConfig. Старые local repos/passwords и evacuation helpers пока доступны; новые direct PVE snapshots сохраняются. Перед восстановлением расписаний исключить параллельный запуск обеих схем. Откат config не удаляет снимки, не откатывает PVE и не меняет его polynomial.

После окончательной очистки прежняя local → copy схема не является поддерживаемым fallback. Источники helpers остаются в Git, но их повторное развёртывание требует отдельного осознанного решения, а не ссылки на уже удалённый temporary rollback context. Для исправления direct config использовать актуальный защищённый config/recovery set и существующие PVE credentials. Полный проигрыш VPS не должен требовать local repository: recovery идёт из существующего PVE.

До mutation остановиться на несовпадении repository ID, неизвестных credentials, неожиданном config diff или неучтённых local snapshots. После mutation не объявлять приёмку при отсутствии правильного parent, потере старого ID вне согласованного maintenance окна, warning/partial flow, неуспешном readback либо несоответствии восстановленных контрольных данных. Не «исправлять» эти случаи init, принудительным полным backup, удалением истории или обходом warnings.

## 6. Primary references

- [Backrest exact deployed source: parent selection and repo credentials](https://github.com/garethgeorge/backrest/blob/875c9cb51e626a75276a64da42c6a9ec0695010a/internal/orchestrator/repo/repo.go).
- [Backrest exact deployed source: native validation](https://github.com/garethgeorge/backrest/blob/875c9cb51e626a75276a64da42c6a9ec0695010a/internal/config/validate.go).
- [Backrest exact deployed source: hook variables and ShellEscape](https://github.com/garethgeorge/backrest/blob/875c9cb51e626a75276a64da42c6a9ec0695010a/internal/orchestrator/tasks/hookvars.go).
- [Restic 0.19.1: unchanged-file content reuse](https://github.com/restic/restic/blob/v0.19.1/internal/archiver/archiver.go#L521).
- [Restic: file change detection](https://restic.readthedocs.io/en/stable/040_backup.html#file-change-detection).
- [Restic maintainer: copied parent with different chunker parameters](https://forum.restic.net/t/restic-copy-and-deduplication/3277/14).
- [Restic: retention rules](https://restic.readthedocs.io/en/stable/060_forget.html#removing-snapshots-according-to-a-policy).
