# Production PDF cleanup: полный повторный прогон

Дата: 2026-10-05. Статус: **DEPLOYED / VERIFIED**. `PDF_CLEANUP_PRODUCTION_VERIFICATION=PASS`.

По прямому поручению оператора применён зафиксированный generic refinement,
предварительно очищен cleaned и повторно обработаны все текущие originals.
Это post-infrastructure application work; принятый Stage 13 не меняется.
Текущий результат supersedes прежний CANDIDATE / NOT DEPLOYED и ограничения
пяти документов в WA G3 expansion. Исторические записи не переписываются.

## Подтверждённый результат

- **95/95 PDF**, 14 каталогов моделей, 49 уникальных SHA256.
- **11 584 страницы / 6 579 007 полезных глифов** проверены для всех путей, включая дубликаты между моделями.
- 0 потерь полезного текста, 0 изменений свойств документа, 0 изменённых пикселей вне точных масок удаляемых элементов.
- В каждом конечном PDF отсутствуют удаляемые ссылки/Widgets; повторный анализ фактической сохранённой копии даёт 0 целей колонтитулов.
- Все 95 SHA256 originals совпали до/после. INDEX.md и translated сохранены.
- 95 cleaned опубликованы через Nextcloud WebDAV в аналогичные каталоги моделей; физические SHA256 совпали с проверенными копиями.
- INDEX.html имеет 95 отметок cleaned с датой и относительным путём. Названия, даты источников/предыдущих документов и интерфейс сохранены.
- В итоговых CLI результатах 0 ошибок и пустой stderr. n8n graphs/расписание/credentials/adapter/launcher не изменялись.

| Каталог | PDF | Страниц | Результат |
| --- | ---: | ---: | --- |
| WA5480 G3 | 11 | 1409 | PASS |
| WA5480 G5 | 13 | 1681 | PASS |
| WA5680 G3 | 1 | 128 | PASS |
| WA5680 G5 | 4 | 416 | PASS |
| WA5685 G5 | 3 | 189 | PASS |
| WA7780 G3 | 2 | 136 | PASS |
| WA7785a G3 | 2 | 125 | PASS |
| WA7880a G3 | 1 | 151 | PASS |
| WR3220 G5 | 5 | 481 | PASS |
| WR5215 G5 | 9 | 1278 | PASS |
| WR5220 G3 | 15 | 1761 | PASS |
| WR5220 G5 | 14 | 1789 | PASS |
| WR5225 G3 | 12 | 1586 | PASS |
| WR6220 G5 | 3 | 454 | PASS |

## Source и runtime

Upstream: Eugene-SN/documentation-ai `46f179e9e5c83ff2c12b7ba084efef124afaf338`.
Local executable source: `9c9bbb375751f85ca1e6f737504f3e99a68fd3d5` — import +
portable originals guard + проверенный generic refinement. Source Git clean.

Production image: `edge/pdf-cleanup:9c9bbb375751-fonts`:
`sha256:93ca37d01cdfbb68550cba9d0008aefac52f3b2d6e86ca481e5163fde1ca448e`.
Python 3.14.8, PyMuPDF 1.28.2, pypdf 6.19.0, cryptography 50.0.2,
fontTools 4.66.1, cleanup package 0.1.3. Source hashes и manifest:
[deployment.json](deployments/edge/pdf-cleanup/deployment.json).

Применена точная обработка text operands, pure-text Footer Forms и clipping,
геометрическое ограничение untagged pagination. Нет правил по именам PDF,
моделям или vendor-профилей. Полезные числа, таблицы, whitespace/order сохраняются.
`garbage=2`, deflate и object streams сохраняют содержимое без потерь.
При отсутствии любых целей выполняется точное копирование; отсутствие
колонтитулов не отменяет очистку ссылок/Widgets, если они есть.

Во время первого полного прогона три документа Press (WA5680 G5/lp2506.pdf,
WA5685 G5/lp2507.pdf, WR6220 G5/lp2502.pdf) дали предупреждение об optional CFF
font decoder. По [официальному механизму pypdf](https://pypdf.readthedocs.io/en/6.19.0/user/installation.html)
и metadata/source установленной 6.19.0 добавлен её `fonts` extra (fontTools).
Остальные версии и три executable модуля не менялись. Native evidence этих
трёх PDF совпало, все objects/decoded streams сохранились; повторное сохранение
поменяло только служебный /ID в xref trailer. Затем эти три PDF повторно
обработаны **production adapter/launcher**, опубликованы и независимо проверены.
Всего 98 успешных CLI запусков: полный 95 + dependency repeat 3.
Остальные 92 результата не требовали CFF decoder и сохраняют прежние проверенные SHA.

## Как проверялось

Использован действующий `/opt/pdf-cleanup/job-command.py` → launcher → one-shot
production Docker image. Это авторизованный одноразовый full rebuild, **не**
95 n8n executions: synthetic numeric job IDs не являются execution ID n8n.
Не создавались временные workflows, nodes, credentials, сервисы или retries.
Перед первым прогоном 14 прежних cleaned PDF удалены через native WebDAV;
каталоги сохранены. Все 95 paths затем обработаны отдельно.

Независимый reviewer работал параллельно CLI и проверял реально опубликованные
копии: SHA, native validation, свойства PDF, Unicode/порядок/положение глифов,
все страницы PDFium 144 dpi и все пиксели вне glyph/Widget masks с двухпиксельным
допуском на antialiasing. Второй анализ использовал actual native inspection
конечного файла, не кеш предыдущего stage. Все 95 reviews PASS.
35 package tests, 6 independent verifier controls и 2 console controls PASS.
После fonts addition все 35 tests также подтверждены (21 + 14 setup recovery).

Сохранена защита originals: CLI запрещает output внутрь authoritative originals,
включая symlink alias. Реальные оригиналы не монтируются в обработчик; input
snapshot read-only, output отдельный. Разрешённая downloader replacement логика
originals не затрагивается этой защитой cleanup.

TechnicalDocumentationSync остаётся active version
`6ed111f3-306d-4cf1-8dc4-2a107c2c1b26`, LenovoPdfCleanup —
`382fc37d-61ec-4311-8c80-0bcb774a2221`; по 17 nodes / 3 groups.
Launcher динамически читает image_id из manifest, поэтому следующий обычный
вызов workflow использует новый runtime без изменения схемы.

## Условия и чистота evidence

У reviewer обнаружен дефект жизненного цикла кеша: планы source удерживались
после последнего использования. Остановлен только audit container, 68 готовых
PASS сохранены, оставшаяся работа завершена после eviction fix. Production
алгоритм и критерии не менялись. Последний reviewer завершился RC=0.

Сессия инструмента, управлявшая первым batch shell, потеряна после restart
Codex daemon; её RC **UNKNOWN**. Completion подтверждают batch-finished.json,
95 успешных adapter/CLI результатов, WebDAV readback и все независимые reviews.
Не выдаётся неизвестный shell RC за подтверждённый. Неудачные build/harness
вызовы (bare SHA FROM, отсутствующий TMPDIR, сравнение регенерируемого trailer ID)
отделены от production ошибок в lifecycle.json.

Own temporary jobs/containers и тестовые PDF/deps/credential export удалены.
Удалены ровно шесть собственных build-cache records и superseded code-only
image; старый accepted runtime остаётся только как подтверждённый build input
[Refinement.Dockerfile](deployments/edge/pdf-cleanup/Refinement.Dockerfile).
Originals, конечные cleaned, INDEX files и необходимые runtime данные сохранены.

## Граница подтверждения

Текущая production версия подтверждена на всём фактическом каталоге и является
базой для документов аналогичных исследованным форматам. Это не гарантия для
произвольного будущего PDF: новые типы layout/кодирования, password/scanned PDF
и mixed Forms могут потребовать отдельной проверки. Существующие защиты
содержимого не отключались и не заменялись fallback, угадывающим удаление.

[Полные результаты по каждому пути](deployments/edge/pdf-cleanup/production-2026-10-05/evidence.json),
[протоколы и harness](deployments/edge/pdf-cleanup/production-2026-10-05/README.md).
