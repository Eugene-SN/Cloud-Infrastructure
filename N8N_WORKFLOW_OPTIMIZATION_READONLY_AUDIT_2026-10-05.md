# n8n — аудит эффективности семи оставшихся workflows

Дата: 2026-10-05. Чтение runtime: 13:26–13:34 UTC, то есть 16:26–16:34 UTC+3.
Статус: READ-ONLY / рекомендации, без изменения автоматизаций и принятия нового runtime-контракта.

## Область и доказательства

**CONFIRMED FACT:** в n8n 2.40.7 существуют семь активных, опубликованных workflows; архивных нет. Проверены опубликованные `workflow_history.nodes/connections`, связанные через `workflow_entity.activeVersionId`, настройки, сохранённые executions и установленный upstream-код. Черновик и опубликованная версия могут иметь разные ID, поэтому анализ canvas не подменяет анализ работающего графа.

| Workflow | ID | Опубликованная версия | Узлы |
|---|---|---|---:|
| AIExecution | wQ9ZqMisMCGadGEE | e9a2731b-b637-4dd1-a7c6-2b10f83b3583 | 8 |
| NextcloudTools | G0WysKToqsel8yL2 | b881ab95-fdae-4471-a490-8d7280564beb | 18 |
| LenovoPdfCleanup | ENo9jFkwcE4PFOyL | 382fc37d-61ec-4311-8c80-0bcb774a2221 | 17 |
| TechnicalDocumentationSync | QouVaVNhAqSiYq5D | 6ed111f3-306d-4cf1-8dc4-2a107c2c1b26 | 17 |
| Plane Event Ingress | PlaneEventIngress01 | e211a1e9-cecd-463a-be4a-9c977abde739 | 8 |
| Plane → Mattermost | PlaneMattermost01 | 725ad332-859f-4594-992d-e76c105ad4cd | 10 |
| Plane API deletion reconciliation | PlaneDeletionReconcile01 | 34a3d4af-9527-4c20-8e09-8d4c2fc360d6 | 8 |

**CONFIRMED FACT:** эти опубликованные версии не изменились между начальным и повторным чтением. В параллельной документной работе расширяется корпус: текущий опубликованный sync содержит 14 моделей. Executions 12122/12140 ещё выполнялись; child получил 16 путей. Их незавершённые результаты не включены в оценку успешности или скорости. Метрики 78 документов ниже относятся к завершённым версиям с девятью моделями, а не к текущему расширенному корпусу.

**CONFIRMED FACT:** host helpers `/usr/local/bin/edge-ai-exec`, `/opt/pdf-cleanup/job-command.py`, `/opt/pdf-cleanup/run` совпадают по SHA256 с файлами репозитория. Проверка чистой логики выполнялась в памяти, с искусственными входами, без HTTP/SSH-вызовов, создания workflows, документов, заданий или постоянных тестовых файлов.

**UNKNOWN:** текущая скорость/доступность всех AI backends, длительная эксплуатационная статистика новой документной цепочки и эффективность PDF-классификации на всём корпусе. Эти свойства не устанавливаются числом узлов или двумя успешно обработанными PDF. Успешный execution также не всегда означает успешную операцию: AIExecution/NextcloudTools намеренно возвращают прикладное `ok:false` как данные.

## Оценка каждого workflow

| Workflow | Что составлено рационально | Что улучшить |
|---|---|---|
| AIExecution | Явный выбор одного из четырёх backends, один вызов, общий результат; CLI имеет deadline и два host concurrency slots. Лишнего LLM-роутера нет. | Для Hermes проверить результат по переданной JSON Schema, если schema должна быть гарантией, а не подсказкой. Реальную скорость без новых backend-вызовов оценить нельзя. |
| NextcloudTools | Один универсальный adapter, исполняется одна ветка из 11 операций. Отдельная подготовка binary и разбор WebDAV XML имеют конкретную роль. 17 сохранённых успешных вызовов в среднем занимали около 0,33 с. | Не выдавать UTF-8 текст вместе с base64 для любого бинарного файла; стабилизировать формат list/find. Одинаковые list/find запросы можно свести в один узел, но это упрощает canvas, не уменьшает число API-вызовов. |
| Plane Event Ingress | HMAC по исходным байтам, фильтрация событий, coalescing и запись inbox до HTTP 204. Уведомление вынесено из webhook-ответа. | Существенных избыточных шагов в опубликованном пути не обнаружено. Coalescing — уведомление о последнем состоянии, не полный журнал каждого промежуточного изменения. |
| Plane → Mattermost | Семантическое сравнение, защита от устаревшего update, последовательная обработка и compare-delete именно обработанного payload. | Главная цена — пустые executions каждые 30 с и их сохранение. Есть окно повторной отправки между post и сохранением state. |
| Plane API deletion reconciliation | Удаление подтверждается native activity, а не одним HTTP 404; пагинация и исключение обработанных delete сохранены. | Стоимость растёт с числом живых задач и их activity pages. Фильтр tombstones можно перенести в чтение таблицы; при семи задачах это небольшое улучшение. |
| TechnicalDocumentationSync | Раз в сутки; при отсутствии изменений прекращается до скачивания, записи INDEX и очистки. Новые originals и INDEX сохраняются до child. | Дедуплицировать проверки одного source URL между моделями; затем оценить повторное скачивание общих manuals. Добавить наблюдение ошибок и, если требуется, повтор pending cleanup. |
| LenovoPdfCleanup | CLI отдельно от транспорта; последовательный batch; старый cleaned удаляется после нового PUT; успешные отметки INDEX сохраняются по каждому файлу. | Восстановить прикладной результат после последнего HTTP PUT; провести transport failure через удаление temporary job; при необходимости поддержать несколько одновременных callers явно. |

Это качественная оценка назначения узлов и поведения. Баллы «из 10» и неподтверждённые обещания ускорения не используются.

## Конкретные исправления и ограничения

### 1. Результат PDF-очистки теряется на последнем HTTP-узле

**CONFIRMED FACT:** execution 12016 успешно обработал два PDF. `Return Result` сформировал `ok/status/path/summary/temporary_job_removed`, но следующий `Save Cleanup INDEX` заменил item своим HTTP-ответом. Завершающий `Each PDF` возвратил два объекта с ключами `headers/statusCode/statusMessage`; родитель 12015 получил именно их.

**Рекомендация:** после успешной записи INDEX вернуть сводку очистки по файлу и выдать её caller. Сохранение PDF и ожидание child уже работают; недостаток относится к полезности машинного результата. Это соответствует upstream-механизму: caller получает данные завершающего узла sub-workflow, а Loop Over Items объединяет данные обработанных итераций. [Execute Sub-workflow](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow), [Loop Over Items](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches).

### 2. Один transport error обходит удаление PDF job

**CONFIRMED FACT / граф:** `Remove Previous Cleaned PDF` расположен после создания/обработки job, но не имеет `onError=continue…` и отдельной error-ветки. HTTP-коды возвращаются через `neverError`, а транспортная ошибка остановит граф до `Remove Temporary Job`. При HTTP 500 обычный путь до удаления job есть; эти случаи нельзя смешивать.

**INFERENCE:** сетевой сбой этого DELETE способен оставить рабочий каталог, даже без отмены execution. Такое событие не воспроизводилось на production; это подтверждённая структура графа и вывод о её failure path. Единственный наблюдавшийся `/tmp/pdf-cleanup-*` принадлежал ещё выполняющемуся 12140 и не является мусором.

**Рекомендация:** направлять ошибку DELETE через существующий cleanup, затем возвращать/поднимать исходную ошибку. Маскировать сбой успешным результатом не требуется. `Never Error` меняет обработку HTTP status codes, а не гарантирует выполнение запроса. [HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest).

### 3. JSON Schema в Hermes-ветке — подсказка, не проверка

**CONFIRMED FACT:** Hermes получает schema в тексте prompt. `Execution Result` делает только `JSON.parse`. Проверка опубликованного Code с искусственным ответом `{"unexpected":true}` при schema с обязательным строковым `answer` возвратила `ok:true`.

Это согласуется с ранее описанным отсутствием native constrained decoding у этой ветки; новый сбой backend не заявляется. **Рекомендация:** если вызывающий код должен полагаться на schema, валидировать объект после разбора и возвращать отдельную ошибку несоответствия. Повторный LLM-вызов для этого не нужен.

### 4. Nextcloud download раздувает машинный ответ

**CONFIRMED FACT:** `Tool Result` для любого download читает весь binary buffer и одновременно выдаёт `content_base64` и `content=b.toString('utf8')`. Проверка с искусственным binary размером 1 MiB дала 1 398 104 base64 characters и полный JSON-ответ 4 543 988 bytes. Это пример на заданных байтах, не измерение размера реальных пользовательских файлов или RAM процесса.

**Рекомендация:** выбирать представление: текст для текстового запроса, base64 для binary. Для больших файлов полезнее ссылка/metadata, если вызывающему агенту не нужны сами bytes. Согласовать изменение с контрактом существующих callers.

**CONFIRMED FACT / чистая логика:** пустой native list с `alwaysOutputData` placeholder возвращает `{}`, один item — объект, несколько — массив. `find` фильтрует JSON представление списка текущей папки; recursive search в графе нет. **Рекомендация:** list/find всегда возвращают массив, пустой список — `[]`; описать область поиска явно. Это улучшает предсказуемость adapter, не производительность сервера.

### 5. Документная цепочка имеет ручное восстановление cleanup и общий INDEX

**CONFIRMED FACT:** unchanged source пропускается, даже если старый документ имеет `cleanup_status=pending`. Автоматической retry queue нет — это уже документированный предел принятой интеграции. Ни один из семи графов не содержит Error Trigger и ни один не задаёт `settings.errorWorkflow`. Текущий Edge Monitor следит за двумя Plane schedules, не за завершением документов.

**Рекомендация:** обеспечить уведомление о production failure документного parent; native варианты — Error Trigger в существующем workflow либо общий error workflow. Если требуется полностью автоматическое восстановление, отдельно определить повтор только pending paths, без повторного скачивания unchanged originals. Достаточно одного механизма наблюдения; новые очереди/сервисы не являются необходимостью по этому аудиту. [Native error handling](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully), [Workflow settings](https://docs.n8n.io/build/manage-workflows/configure-workflow-settings).

**INFERENCE / ограничение concurrency:** последовательность Each PDF защищает порядок одного batch, но два независимых callers могут прочитать один INDEX и перезаписать отметки друг друга. Source sync тоже сохраняет INDEX из прочитанного в начале snapshot. В графах нет общей блокировки. Потеря отметок не наблюдалась; README уже требует избегать simultaneous callers. Если такое использование нужно поддержать, следует сериализовать записи общего каталога. Простое распараллеливание PDF этого ограничения не решает.

### 6. Обработка сетевых сбоев должна учитывать повторяемость операции

**CONFIRMED FACT:** `retryOnFail` не включён ни у одного узла семи опубликованных workflows. Для GET/HEAD документных источников можно рассмотреть ограниченные повторы с паузой, учитывая общий deadline. Повторная отправка AI task или Mattermost post не эквивалентна повтору чтения.

**CONFIRMED FACT / граф:** Mattermost post выполняется до `Persist Issue State`. **INFERENCE:** принятый сервером post при потерянном ответе либо сбое сохранения state может повториться при следующем drain. Dedup fingerprints предотвращают обычные повторные события, но не дают exactly-once на этой границе. Дубли не наблюдались в данном срезе: inbox был пуст. Не рекомендуется автоматически добавлять retry POST без проверки upstream-механизма idempotency и требуемой семантики.

## Измеримая цена расписаний и повторных запросов

Срез сохранённых executions до 13:27:30 UTC:

| Workflow | Успешные runs в срезе | Средняя длительность | Полезная работа в этих runs |
|---|---:|---:|---|
| Plane → Mattermost | 8 617 | 34,7 мс | Только Schedule и Read Inbox; во всех runs inbox пуст, post не выполнялся |
| Plane deletion reconciliation | 861 | 1,22 с | По семь activity node calls; 6 027 всего, подтверждённых delete нет |
| LenovoPdfCleanup 12016 | 1 batch / 2 PDF | 60,17 с | 53,16 с суммарно в Run PDF Cleanup CLI |
| TechnicalDocumentationSync 12073 | 1 | 6,30 с | 9 ASP responses, 78 HEAD, ноль changed; скачивания и child не выполнялись |

**CONFIRMED FACT:** у reconciliation есть один сохранённый failed trigger, 2026-10-02 15:15 UTC: `Task request timed out` в `Confirmed Deletion Only`. Корневая причина в этом аудите не установлена; это не доказательство текущего отказа API или pagination bug. Исторические manual errors PDF относятся к разработке прежних версий, не считаются отказами текущего опубликованного графа.

**CONFIRMED FACT:** два Plane schedules дают 2 880 + 288 = **3 168 executions/day**, плюс один документный daily run. Успешные polling JSON в срезе занимают логически около **113 MiB**, по среднему размеру — около **39,6 MB/day**. Это не измерение физического прироста SQLite, backup size, CPU или peak RAM.

Штатные config defaults установленной версии: pruning включён, age 336 часов, count 10 000; environment overrides отсутствуют, пользовательский config содержит только encryptionKey. **INFERENCE:** при текущем потоке count limit соответствует примерно **3,16 суток** истории, раньше age limit. Штатные периодические pruning/buffering и другие executions меняют точную границу. [Execution configuration](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions).

**Рекомендация / выбор задержки:** если ожидание следующего notification poll до 60 с приемлемо, смена 30→60 с сократит эту часть с 2 880 до 1 440 runs/day; с reconciliation останется 1 728/day. Это вариант, не принятая новая частота. При требовании прежней задержки рассмотреть event-driven drain с существующим inbox и recovery poll, предварительно определив concurrency/recovery. Полезность защитного reconciliation не исчезает из-за отсутствия удалений в нескольких днях.

**CONFIRMED FACT:** нельзя независимо выключить сохранение successful polling executions: `monitoring/edge/edge-monitor` использует их native `execution_entity` timestamps/status. Установленный lifecycle при save-success=none помечает execution для удаления, затем native pruning удаляет его. **INFERENCE:** такое «ускорение» без изменения health contract в итоге даст ложный stale-success incident. Изменение частоты тоже требует согласования monitor cadence/thresholds. Советы просто выключить successful history в текущем runtime некорректны.

**CONFIRMED FACT:** в завершённом sync 12073 **78 document paths соответствуют 42 уникальным source URLs**. Одни manuals встречаются в шести модельных папках. Проверка каждого path отдельным HEAD даёт 36 повторных запросов. **Рекомендация:** один HEAD на URL за run, затем раздать validator соответствующим document records. Это уменьшает число HEAD примерно на 46% для этого набора; такое же ускорение всего workflow не обещается. Проверка validators занимала лишь 1,24 с из 6,30 с. Дедупликация скачиваний/CLI общих документов — следующий отдельный шаг, с сохранением публикации и completion marker каждой папки.

**CONFIRMED FACT / чистая логика:** при отсутствии всех validators и у old, и у new текущий comparator принимает `null === null` как sameBytes. В 78 реальных HEAD такого случая не было: все имели Last-Modified и Content-Length. **Рекомендация:** не считать отсутствие признаков доказательством неизменности; определить fallback только если источник действительно перестанет отдавать validators. Это низкоприоритетный edge case, не текущий массовый пропуск обновлений.

## Порядок улучшений

1. Исправить полезный return PDF child и transport failure path до удаления job.
2. Сделать Nextcloud binary response компактным и list/find типизированным; определить гарантию schema в AIExecution.
3. Дедуплицировать HEAD по URL; обеспечить наблюдение production errors документной цепочки.
4. Выбрать допустимую задержку Plane notifications и согласованно оптимизировать schedule/history/monitoring.
5. Добавлять pending retry, общую сериализацию или дедупликацию PDF processing только под требуемое использование, сохраняя per-file completion и originals.

Работа audit не меняла workflows, credentials, schedules, таблицы, документы, helpers, monitor или активные jobs. Сохранён только этот аналитический отчёт; временные scripts, backups и workflow exports не создавались. Чужие изменения документации/моделей в worktree не включены в audit commit. Следующая оптимизация должна сверить актуальные опубликованные версии и выполнить ограниченные проверки конкретного изменения.
