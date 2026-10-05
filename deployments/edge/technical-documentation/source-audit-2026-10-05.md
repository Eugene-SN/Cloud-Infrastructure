# Источники документации Lenovo — список по моделям

Проверено: **2026-10-05**. Статус: **READ-ONLY AUDIT — в n8n не добавлено**.

Проверены каталог [Lenovo ASP](https://asp.atlenovo.com/asp-service/index.html#/deviceInfo) и поиск/страницы [Lenovo Press](https://lenovopress.lenovo.com/). Для каждой из 36 уникальных PDF-ссылок подтверждены HTTP 200, тип PDF и сигнатура `%PDF-` при чтении начала файла. Полные PDF не скачивались; originals, INDEX.html и автоматизация не изменялись.

Сортировка моделей: семейство WR, затем WA; номер модели по возрастанию. Внутри модели: Product Guide → Datasheet → User Manual → OS Installation → BIOS → BMC → Provisioning → XClarity → PSU → прочие справочники. Даты указаны отдельно и не влияют на этот порядок.

Дата для ASP — `updated` в каталоге модели; для Lenovo Press — Published/Updated на странице публикации. Это не гарантирует совпадение с датой редакции внутри PDF. Краткие названия — перевод названия источника для будущего каталога; исходные названия сохранены в JSON. Язык PDF Lenovo Press отдельно не проверялся.

Итого: **52 актуальные позиции ASP + 11 PDF Lenovo Press = 63 позиции по папкам моделей**, включая один дополнительный общий справочник SAP (LP1728). Уникальных ссылок — **36**: общие руководства повторяются в коллекциях. Примерный объём: **493,2 MB** для всех модельных копий; **396,5 MB** по уникальным ссылкам.

Парные модели сохраняют общую группу источника. В качестве будущего имени папки показана основная модель, как в уже используемой папке WR5220 G3. Папки из этого отчёта не созданы.

| Группа моделей | ASP, актуальные | Lenovo Press | Всего | Будущая папка |
| --- | ---: | ---: | ---: | --- |
| WR3220 G5 | 4 | 1 | 5 | `WR3220 G5/` |
| WR5215 G5 | 8 | 1 | 9 | `WR5215 G5/` |
| WR5220 G5/WR5228 G5 | 12 | 2 | 14 | `WR5220 G5/` |
| WR5225 G3 | 11 | 1 | 12 | `WR5225 G3/` |
| WR6220 G5 | 1 | 2 | 3 | `WR6220 G5/` |
| WA5480 G5/WA5488 G5 | 13 | 0 | 13 | `WA5480 G5/` |
| WA5680 G5 | 2 | 2 | 4 | `WA5680 G5/` |
| WA5685 G5 | 1 | 2 | 3 | `WA5685 G5/` |

Копии общих руководств привязаны к моделям согласно их собственным каталогам ASP. Отсутствующая в каталоге модели инструкция не добавлялась по аналогии с другими серверами.

## WR3220 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WR3220 G5/`

**Machine Type:** 7DQ6

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2FC342B075-351E-47EA-BE1F-DBAFE95A46A0) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WR3220%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WR3220 G5 | [lp2440.pdf](https://lenovopress.lenovo.com/lp2440.pdf) | 2026-07-22 | 4.76 |
| 2 | User Manual Lenovo Wentian WR3220 G5 | [lenovo_wentian_wr3220g5_user_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wr3220g5_user_guide.pdf) | 2026-05-21 | 17.75 |
| 3 | User Guide Lenovo XClarity Essentials BoMC cPlus | [lxce_bomc_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_bomc_cplus_ug.pdf) | 2026-08-27 | 0.64 |
| 4 | User Guide Lenovo XClarity Essentials OneCLI cPlus | [lxce_onecli_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_onecli_cplus_ug.pdf) | 2026-08-27 | 0.86 |
| 5 | User Guide Lenovo XClarity Essentials UpdateXpress cPlus | [lxce_ux_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_ux_cplus_ug.pdf) | 2026-08-27 | 0.78 |

## WR5215 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WR5215 G5/`

**Machine Type:** 7DMY

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2F2965B165-6320-4D06-BD34-8350DBC4B616) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WR5215%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WR5215 G5 | [lp2356.pdf](https://lenovopress.lenovo.com/lp2356.pdf) | 2026-09-04 | 2.56 |
| 2 | User Manual Lenovo Wentian WR5215 G5 | [lenovo_wentian_wr5215g5_user_guide_v2.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wr5215g5_user_guide_v2.pdf) | 2026-05-22 | 27.88 |
| 3 | User Guide Lenovo BMC Enterprise G5 | [lenovo_bmc_user_guide_g5_v6.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_user_guide_g5_v6.pdf) | 2026-07-31 | 13.74 |
| 4 | IPMI Command Specification Lenovo BMC G5 | [lenovo_bmc_commands_g5_v3.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_commands_g5_v3.pdf) | 2026-08-11 | 1.10 |
| 5 | SNMP Reference Guide Lenovo BMC G5 | [lenovo_bmc_snmp_guide_g5.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_snmp_guide_g5.pdf) | 2026-08-11 | 1.20 |
| 6 | Redfish Interface Specification Lenovo BMC G5 | [lenovo_bmc_redfish_guide_g5_v4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_redfish_guide_g5_v4.pdf) | 2026-08-11 | 9.39 |
| 7 | User Guide Lenovo XClarity Essentials BoMC cPlus | [lxce_bomc_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_bomc_cplus_ug.pdf) | 2026-08-27 | 0.64 |
| 8 | User Guide Lenovo XClarity Essentials OneCLI cPlus | [lxce_onecli_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_onecli_cplus_ug.pdf) | 2026-08-27 | 0.86 |
| 9 | User Guide Lenovo XClarity Essentials UpdateXpress cPlus | [lxce_ux_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_ux_cplus_ug.pdf) | 2026-08-27 | 0.78 |

## WR5220 G5/WR5228 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WR5220 G5/`

**Machine Type:** 7DFX

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2FEDF3440A-96A1-463B-9A35-C871B3B28AA1) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WR5220%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WR5220 G5 | [lp2014.pdf](https://lenovopress.lenovo.com/lp2014.pdf) | 2026-09-30 | 6.05 |
| 2 | User Manual Lenovo Wentian WR5220 G5 | [lenovo_wentian_wr5220g5_user_guide_v7.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wr5220g5_user_guide_v7.pdf) | 2026-03-20 | 46.29 |
| 3 | OS Installation Guide Lenovo Wentian | [lenovo_wentian_os_installation_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_os_installation_guide.pdf) | 2026-03-23 | 13.67 |
| 4 | User Guide Lenovo BMC Enterprise G5 | [lenovo_bmc_user_guide_g5_v6.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_user_guide_g5_v6.pdf) | 2026-07-31 | 13.74 |
| 5 | IPMI Command Specification Lenovo BMC G5 | [lenovo_bmc_commands_g5_v3.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_commands_g5_v3.pdf) | 2026-08-11 | 1.10 |
| 6 | SNMP Reference Guide Lenovo BMC G5 | [lenovo_bmc_snmp_guide_g5.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_snmp_guide_g5.pdf) | 2026-08-11 | 1.20 |
| 7 | Redfish Interface Specification Lenovo BMC G5 | [lenovo_bmc_redfish_guide_g5_v4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_redfish_guide_g5_v4.pdf) | 2026-08-11 | 9.39 |
| 8 | Event Reference Guide Lenovo BMC G3/G5 | [lenovo_bmc_event_reference_guide_g5_v4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_event_reference_guide_g5_v4.pdf) | 2026-07-31 | 1.75 |
| 9 | User Guide Lenovo XClarity Provisioning Manager Wentian | [lxpm_wentian_ug-v2.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxpm_wentian_ug-v2.pdf) | 2026-02-04 | 2.51 |
| 10 | User Guide Lenovo XClarity Essentials BoMC cPlus | [lxce_bomc_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_bomc_cplus_ug.pdf) | 2026-08-27 | 0.64 |
| 11 | User Guide Lenovo XClarity Essentials OneCLI cPlus | [lxce_onecli_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_onecli_cplus_ug.pdf) | 2026-08-27 | 0.86 |
| 12 | User Guide Lenovo XClarity Essentials UpdateXpress cPlus | [lxce_ux_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_ux_cplus_ug.pdf) | 2026-08-27 | 0.78 |
| 13 | PSU Label Matrix Lenovo | [psu_label_matrix.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/psu_label_matrix.pdf) | 2025-05-06 | 1.68 |
| 14 | SAP Certifications of Lenovo Servers | [lp1728.pdf](https://lenovopress.lenovo.com/lp1728.pdf) | 2025-09-01 | 0.27 |

`lp1728.pdf` — дополнительный общий справочник SAP, а не руководство сервера. WR5220 G5 явно присутствует в его разделах SAP Business Suite и SAP HANA. [Страница источника](https://lenovopress.lenovo.com/lp1728-sap-certifications-of-lenovo-servers). Product Guide LP2014 имеет название WR5220 G5; его применимость к WR5228 G5 отдельно не подтверждена.

Исключённые повторные/старые записи ASP:

- `lxpm_wentian_ug-v2.pdf` — 2026-02-04; повтор той же PDF-ссылки LXPM.

## WR5225 G3

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WR5225 G3/`

**Machine Type:** 7DG2

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2F738CA58A-E195-47E6-A61D-248870091B2C) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WR5225%20G3)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WR5225 G3 | [lp2129.pdf](https://lenovopress.lenovo.com/lp2129.pdf) | 2026-09-04 | 5.22 |
| 2 | User Manual Lenovo Wentian WR5225 G3 | [wr5225g3_user_guide_v6.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/wr5225g3_user_guide_v6.pdf) | 2026-05-29 | 31.02 |
| 3 | OS Installation Guide Lenovo Wentian | [lenovo_wentian_os_installation_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_os_installation_guide.pdf) | 2026-03-23 | 13.67 |
| 4 | BIOS Setup Specification Lenovo Wentian WR5225 G3 — Genoa | [wr5225g3_bios_setup_spec_v3.0-genoa.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/wr5225g3_bios_setup_spec_v3.0-genoa.pdf) | 2026-05-19 | 9.12 |
| 5 | BIOS Setup Specification Lenovo Wentian WR5225 G3 — Turin | [wr5225g3_bios_setup_spec_v2.9-turin.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/wr5225g3_bios_setup_spec_v2.9-turin.pdf) | 2026-05-19 | 9.52 |
| 6 | SNMP Reference Guide Lenovo BMC G3 | [lenovo_snmp_ug_g3.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_snmp_ug_g3.pdf) | 2026-04-21 | 1.14 |
| 7 | Redfish Interface Specification Lenovo BMC G3 | [lenovo_bmc_g3_redfish_guide_v11.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_g3_redfish_guide_v11.pdf) | 2026-04-10 | 8.33 |
| 8 | Event Reference Guide Lenovo BMC G3/G5 | [lenovo_bmc_event_reference_guide_g5_v4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_event_reference_guide_g5_v4.pdf) | 2026-07-31 | 1.75 |
| 9 | User Guide Lenovo XClarity Essentials BoMC cPlus | [lxce_bomc_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_bomc_cplus_ug.pdf) | 2026-08-27 | 0.64 |
| 10 | User Guide Lenovo XClarity Essentials OneCLI cPlus | [lxce_onecli_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_onecli_cplus_ug.pdf) | 2026-08-27 | 0.86 |
| 11 | User Guide Lenovo XClarity Essentials UpdateXpress cPlus | [lxce_ux_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_ux_cplus_ug.pdf) | 2026-08-27 | 0.78 |
| 12 | PSU Label Matrix Lenovo | [psu_label_matrix.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/psu_label_matrix.pdf) | 2025-05-06 | 1.68 |

BIOS Genoa и BIOS Turin — отдельные документы для разных процессорных платформ. Оба включены; общая версия BIOS между ними не выбиралась.

Исключённые повторные/старые записи ASP:

- `lenovo_bmc_event_reference_guide_g3_v3.pdf` — 2026-04-10; редакция V3 общего BMC G3/G5 Event Reference; текущая — V4. Совпадение семейства ранее подтверждено по области применения G3/G5 внутри документов.

## WR6220 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WR6220 G5/`

**Machine Type:** 7DR6

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2F96C91746-0B94-43FD-9679-AEE8D447ECFB) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WR6220%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WR6220 G5 | [lp2468.pdf](https://lenovopress.lenovo.com/lp2468.pdf) | 2026-08-30 | 9.35 |
| 2 | Datasheet Lenovo Wentian WR6220 G5 | [lp2502.pdf](https://lenovopress.lenovo.com/lp2502.pdf) | 2026-08-31 | 10.17 |
| 3 | User Manual Lenovo Wentian WR6220 G5 | [lenovo_wentian_wr6220g5_user_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wr6220g5_user_guide.pdf) | 2026-09-30 | 25.59 |

## WA5480 G5/WA5488 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WA5480 G5/`

**Machine Type:** 7DHQ

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2FFA7C53C0-E6C1-494C-9581-EA0B9EC4937F) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WA5480%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | User Manual Lenovo Wentian WA5480 G5 | [lenovo_wentian_wa5480g5_user_guide_v5.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wa5480g5_user_guide_v5.pdf) | 2026-03-20 | 43.64 |
| 2 | OS Installation Guide Lenovo Wentian | [lenovo_wentian_os_installation_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_os_installation_guide.pdf) | 2026-03-23 | 13.67 |
| 3 | BIOS Setup Specification Lenovo Wentian WA5480 G5 | [wa5480g5_bios_setup_spec.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/wa5480g5_bios_setup_spec.pdf) | 2025-03-05 | 8.59 |
| 4 | User Guide Lenovo BMC Enterprise G5 | [lenovo_bmc_user_guide_g5_v6.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_user_guide_g5_v6.pdf) | 2026-07-31 | 13.74 |
| 5 | IPMI Command Specification Lenovo BMC G5 | [lenovo_bmc_commands_g5_v3.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_commands_g5_v3.pdf) | 2026-08-11 | 1.10 |
| 6 | SNMP Reference Guide Lenovo BMC G5 | [lenovo_bmc_snmp_guide_g5.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_snmp_guide_g5.pdf) | 2026-08-11 | 1.20 |
| 7 | Redfish Interface Specification Lenovo BMC G5 | [lenovo_bmc_redfish_guide_g5_v4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_redfish_guide_g5_v4.pdf) | 2026-08-11 | 9.39 |
| 8 | Event Reference Guide Lenovo BMC G3/G5 | [lenovo_bmc_event_reference_guide_g5_v4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_event_reference_guide_g5_v4.pdf) | 2026-07-31 | 1.75 |
| 9 | User Guide Lenovo XClarity Provisioning Manager Wentian | [lxpm_wentian_ug-v2.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxpm_wentian_ug-v2.pdf) | 2026-02-04 | 2.51 |
| 10 | User Guide Lenovo XClarity Essentials BoMC cPlus | [lxce_bomc_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_bomc_cplus_ug.pdf) | 2026-08-27 | 0.64 |
| 11 | User Guide Lenovo XClarity Essentials OneCLI cPlus | [lxce_onecli_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_onecli_cplus_ug.pdf) | 2026-08-27 | 0.86 |
| 12 | User Guide Lenovo XClarity Essentials UpdateXpress cPlus | [lxce_ux_cplus_ug.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lxce_ux_cplus_ug.pdf) | 2026-08-27 | 0.78 |
| 13 | PSU Label Matrix Lenovo | [psu_label_matrix.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/psu_label_matrix.pdf) | 2025-05-06 | 1.68 |

В текущем поиске Lenovo Press по WA5480 G5 найден OS Interoperability Guide; отдельный Product Guide/Datasheet для скачивания не найден. Это результат проверенного поиска, а не утверждение об отсутствии публикации во всех ресурсах Lenovo.

Исключённые повторные/старые записи ASP:

- `lxpm_wentian_ug-v2.pdf` — 2026-02-04; повтор той же PDF-ссылки LXPM.
- `lenovo_wentian_wa5480g5_user_guide_v4.pdf` — 2026-02-02; старая редакция руководства WA5480 G5 (V4); текущая — V5.

## WA5680 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WA5680 G5/`

**Machine Type:** 7DP3

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2FF5C5B634-8B65-4226-84B1-4C05F13160D9) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WA5680%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WA5680 G5 | [lp2469.pdf](https://lenovopress.lenovo.com/lp2469.pdf) | 2026-09-16 | 7.30 |
| 2 | Datasheet Lenovo Wentian WA5680 G5 | [lp2506.pdf](https://lenovopress.lenovo.com/lp2506.pdf) | 2026-09-07 | 15.38 |
| 3 | User Manual Lenovo Wentian WA5680 G5 | [lenovo_wentian_wa5680g5_user_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wa5680g5_user_guide.pdf) | 2026-09-08 | 29.43 |
| 4 | BIOS Setup Specification Lenovo Wentian WA5680 G5 | [lenovo_wentian_wa5680g5_bios_setup_spec_v2.4.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_wentian_wa5680g5_bios_setup_spec_v2.4.pdf) | 2026-09-08 | 6.59 |

## WA5685 G5

**Будущий путь:** `/srv/cloud/technical-documentation/lenovo/originals/WA5685 G5/`

**Machine Type:** 7DMZ

**Источники:** [каталог ASP](https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide?fullGuid=339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E%2FE003AB30-9C7D-403E-B672-7B5EFB52C070%2FA9383A8C-EAA4-4DE9-BD5A-44E26ACF44D5) · [поиск Lenovo Press](https://lenovopress.lenovo.com/search?term=WA5685%20G5)

| № | Краткое название | Файл / скачивание | Дата источника | MB |
| ---: | --- | --- | --- | ---: |
| 1 | Product Guide Lenovo Wentian WA5685 G5 | [lp2399.pdf](https://lenovopress.lenovo.com/lp2399.pdf) | 2026-06-02 | 4.63 |
| 2 | Datasheet Lenovo Wentian WA5685 G5 | [lp2507.pdf](https://lenovopress.lenovo.com/lp2507.pdf) | 2026-08-20 | 2.69 |
| 3 | User Manual Lenovo Wentian WA5685 G5 | [wa5685g5_user_guide.pdf](https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/wa5685g5_user_guide.pdf) | 2026-06-11 | 15.97 |

## Примечания для последующего подключения

- Новые модели сейчас не включены в ежедневный workflow. Идентификаторы источников и полный список файлов находятся в [source-audit-2026-10-05.json](source-audit-2026-10-05.json). Это данные аудита, не импорт workflow.
- Для BIOS WR5225 G3 будущий ключ документа должен сохранять платформу Genoa/Turin и исключать номер редакции. Текущий шаблон удаления суффикса версии в workflow не обрабатывает окончания `v3.0-genoa` и `v2.9-turin`; при будущем подключении потребуется небольшой точечный разбор этих имён.
- У WA5480 G5 в ASP одновременно опубликованы V5 и V4 пользовательского руководства; для текущего каталога выбирается V5. Повторные записи одной ссылки LXPM удалены только из списка кандидатов.
- Общий [OS Interoperability Guide](https://lenovopress.lenovo.com/osig) найден как веб-справочник. Он указан отдельно от фиксированных PDF для скачивания.
- Дополнительные источники за пределами Lenovo ASP/Lenovo Press в этом аудите не проверялись. Firmware, drivers и утилиты не являются документацией и в список не включены.
