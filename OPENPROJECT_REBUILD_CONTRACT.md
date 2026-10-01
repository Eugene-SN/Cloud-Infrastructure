# OpenProject Adaptive Rebuild Contract

**Purpose:** allow a future Codex session to rebuild an OpenProject deployment with the same useful capabilities and integration intent, even if the host, software versions, container topology, paths, networks, reverse proxy layout, or surrounding services have changed.

**Status:** REBUILD REFERENCE / FUTURE EXECUTION CONTRACT  
**Current runtime authority:** none — this file is not a statement that OpenProject is currently deployed.  
**Historical source checkpoint:** `OPENPROJECT_PRE_DECOMMISSION_AUDIT_2026-10-01.md`

---

# 1. How Codex must use this document

This is **not** a literal restore script.

Do not blindly recreate the historical 2026 layout, versions, IP addresses, image digests, paths, Docker network names, container names, or proxy plumbing.

The goal is to restore the **capabilities, boundaries, operational behavior, and integrations** described below using the simplest current supported implementation that fits the environment at execution time.

Before any future rebuild:

1. audit the current host and canonical repository;
2. identify which surrounding services still exist and how they are currently deployed;
3. read the current official OpenProject installation and integration documentation;
4. use current stable releases and normal upstream-supported deployment/update paths;
5. inspect the latest applicable accepted decisions in the canonical repository;
6. adapt this contract to the current environment;
7. avoid carrying forward historical workarounds when the underlying problem no longer exists;
8. verify the completed deployment end-to-end before declaring success.

If current runtime facts conflict with historical values in this file, **current runtime wins**.

If current upstream architecture makes a historical implementation unnecessary, use the current supported approach as long as the functional contract remains satisfied.

---

# 2. Source-of-truth order for a future rebuild

Use the following precedence:

1. explicit current operator instruction;
2. fresh runtime audit of the target environment;
3. current official OpenProject documentation and supported deployment model;
4. latest applicable ACCEPTED decisions in the canonical Cloud Infrastructure repository;
5. this file's functional and integration contracts;
6. historical baseline in this file;
7. older historical reports.

Historical values are evidence, not mandatory configuration.

---

# 3. Primary objective

Recreate an OpenProject Community deployment suitable for the single-operator Cloud Infrastructure workflow with:

- a clean upstream-supported application deployment;
- persistent database and attachment storage;
- HTTPS public access through the existing edge ingress model;
- no unnecessary public container exposure;
- native authentication unless a future requirement explicitly changes it;
- Russian as the preferred default UI language unless the operator requests otherwise;
- outbound mail through the currently deployed mail service;
- native GitHub integration for the active canonical infrastructure repository when still applicable;
- native Work Package iCalendar export for Apple Calendar when still useful;
- OpenProject ↔ automation integration using the current n8n-equivalent automation service if present;
- dedicated Mattermost notifications when Mattermost still exists;
- integration into the current backup, monitoring and maintenance frameworks;
- minimal components and no duplicated infrastructure.

The rebuild must restore the **behavioral architecture**, not the exact historical container graph.

---

# 4. Non-goals

Do not automatically add or recreate:

- OpenProject Enterprise-only features;
- OpenProject MCP;
- direct Codex ↔ OpenProject integration;
- direct Antigravity ↔ OpenProject integration;
- Authelia/OIDC in front of OpenProject unless a new requirement exists;
- real-time collaborative editing / Hocuspocus unless there is a concrete need;
- a separate PostgreSQL instance when a suitable shared database service already exists;
- another reverse proxy layer merely because one existed historically;
- extra service-to-service TLS or auth layers inside the trusted single-operator edge environment without a concrete need;
- Nextcloud ↔ OpenProject integration if it still requires local patches, version downgrades, holds, or compatibility shims;
- custom updater logic when current upstream/native update mechanisms are sufficient;
- historical version pins or image digests without a current compatibility reason.

---

# 5. Future rebuild workflow

Codex should execute the rebuild in the following logical phases.

## Phase A — current-environment audit

Inspect only what is necessary to determine:

- host OS and architecture;
- Docker/Compose or current container/runtime platform;
- current ingress/reverse-proxy architecture;
- current domain namespace and TLS ownership;
- existing PostgreSQL or other supported database service;
- persistent storage conventions;
- current mail service;
- current automation service;
- current Mattermost deployment;
- current GitHub canonical repository;
- current backup framework;
- current monitoring framework;
- current maintenance/update framework;
- current internal application networking model;
- whether an OpenProject restore dataset exists and whether the operator wants old data restored.

Do not assume that historical names such as `postgres_net`, `edge_internal`, `/opt/openproject`, `projects.escloud.us`, or `openproject_opdata` still exist.

## Phase B — select the current supported OpenProject deployment model

Prefer the current upstream-recommended stable Community deployment method.

If upstream still provides an official Compose deployment and it fits the environment, using it is reasonable.

If upstream architecture has changed, adapt accordingly rather than forcing the historical Compose layout.

Keep upstream-managed source/configuration clean where practical. Put local edge-specific changes in clearly separated local configuration, override files, environment files, or other supported extension points.

Do not fork or patch upstream source unless a concrete requirement cannot be satisfied otherwise and the operator explicitly accepts the maintenance burden.

## Phase C — data plane

Establish:

- dedicated OpenProject database/schema ownership;
- application credentials;
- required OpenProject database extensions;
- persistent attachment/application data;
- supported migration lifecycle;
- backup inclusion.

If a suitable shared PostgreSQL service already exists, prefer a dedicated OpenProject database and non-privileged role in that service rather than deploying another database container.

If the future OpenProject release requires a different supported database topology, follow current upstream compatibility requirements.

Database service version must be chosen from current compatibility requirements, not historical PostgreSQL 18 merely because it was used in 2026.

## Phase D — application plane

Deploy the minimum OpenProject services required by the current supported upstream architecture.

Historically this required separate web, worker, cron, cache, proxy and autoheal roles. Future versions may differ.

Recreate only roles that remain necessary.

Do not enable real-time collaborative document editing unless the operator explicitly needs it.

Ensure application state survives container recreation and host reboot.

## Phase E — ingress

Expose OpenProject through the current edge ingress architecture.

Desired properties:

- public HTTPS endpoint;
- normal HTTP → HTTPS behavior where relevant;
- valid publicly trusted certificate;
- application generates its own URLs using the public hostname;
- backend should normally remain host-local or internal rather than directly exposed to the Internet;
- preserve current proxy headers required by OpenProject;
- do not register the public FQDN as a Docker/container DNS alias if that would cause internal DNS collisions;
- internal service aliases should use neutral names such as the application/service identity, not the public FQDN.

Historical endpoint was `projects.escloud.us`. Reuse it only if it remains the intended current namespace.

---

# 6. Authentication contract

The historical deployment intentionally used OpenProject's native authentication model.

Future default:

- keep native OpenProject authentication;
- do not place Authelia/OIDC/auth-proxy in front of OpenProject without a current requirement;
- do not introduce LDAP/SSO/RBAC infrastructure merely for architectural symmetry;
- preserve single-operator simplicity.

If OpenProject's current native authentication model materially changes, use the simplest supported equivalent.

---

# 7. Database contract

OpenProject requires its own logical database ownership boundary.

When a shared PostgreSQL service exists:

- create a dedicated OpenProject database;
- create a dedicated non-superuser login role;
- assign database/schema ownership appropriately;
- install only extensions required by the current OpenProject release;
- do not expose PostgreSQL publicly solely for OpenProject;
- connect through the current private/shared database network or equivalent.

Historical database extensions were:

- `btree_gist`;
- `pg_trgm`;
- `unaccent`;
- `plpgsql` as standard PostgreSQL language support.

Treat this list as historical evidence. Verify current upstream requirements during rebuild.

---

# 8. Persistent application-data contract

Persist user-uploaded files and attachments independently from ephemeral application containers.

Requirements:

- persistent data must survive application recreation/update;
- ownership and permissions must match the current OpenProject runtime user model;
- backup tooling must capture this state together with the logical database;
- do not rely on unnamed anonymous volumes for durable state;
- do not retain duplicate obsolete volumes after successful verification.

Historical deployment used one named volume for OpenProject application assets. The future implementation may use a named volume or host path according to current storage policy.

---

# 9. Restore modes

Codex must determine which rebuild mode the operator wants.

## Mode 1 — fresh OpenProject

Create an empty OpenProject deployment and recreate integrations/configuration only.

Use this if historical project/task data is not required.

## Mode 2 — restore historical OpenProject state

Restore from a matching backup set containing:

- OpenProject database dump;
- OpenProject persistent attachment/application data.

Treat database and attachment state as one consistency set whenever possible.

Do not restore only one side blindly if doing so can produce broken attachment/database references.

Before importing an old database into a newer OpenProject release, follow the current supported upgrade/migration path rather than assuming direct compatibility.

---

# 10. Public hostname / internal hostname contract

The public hostname and internal service identity must remain logically separate.

Historical production required a correction because use of the public FQDN inside Docker networking could shadow public DNS for other containers.

Future rules:

- public FQDN is for public URL generation and external ingress;
- internal service discovery uses a neutral service alias;
- do not make the public FQDN an internal container-network alias unless current architecture explicitly requires it and collision behavior is understood;
- verify from at least one unrelated container that the public hostname resolves to the intended public path rather than unexpectedly to an application bridge address.

This is a functional requirement, not a requirement to recreate historical container names.

---

# 11. Outbound mail contract

If the current environment still provides Stalwart or another local mail service, integrate OpenProject directly using its native SMTP support.

Preferred properties:

- dedicated OpenProject sender identity;
- authenticated SMTP submission;
- TLS with peer verification;
- no additional relay/proxy unless required;
- sender address under the current Cloud Infrastructure mail domain;
- secret stored only in local runtime/native credential storage, not in Git.

Historical accepted implementation used:

- mailbox `openproject@escloud.us`;
- `mail.escloud.us`;
- port 465;
- implicit TLS;
- SMTP AUTH `plain`;
- peer verification;
- sender `OpenProject <openproject@escloud.us>`.

These values are a known-good historical reference, not future hard requirements.

Acceptance must include a real OpenProject-generated test message and confirmation that the mail service accepted/delivered it.

---

# 12. GitHub integration contract

When the canonical Cloud Infrastructure repository still uses GitHub and native OpenProject GitHub integration remains supported, recreate the native integration.

Intent:

- OpenProject project representing the canonical infrastructure workflow;
- native GitHub integration enabled for that project;
- dedicated non-admin integration actor;
- dedicated least-privilege project role;
- repository webhook authenticated using an OpenProject API token or current native equivalent;
- independent webhook signature verification when supported;
- no GitHub PAT if the native webhook integration does not require one;
- repository hooks created only for actual repositories that need OpenProject integration.

Historical project:

- display name: `Cloud Infrastructure`;
- identifier: `cloud-infrastructure`.

Historical integration actor:

- `github-integration`.

Historical requested permissions were limited to:

- view work packages;
- add work package comments;

plus any unavoidable OpenProject public-project permissions.

Future Codex must inspect the current OpenProject permission model and recreate the minimum equivalent.

Do not preserve old token values. Generate new credentials and store them only in their native stores.

Acceptance should verify a real GitHub webhook delivery and at least one harmless repository/PR integration path.

---

# 13. Calendar / Apple Calendar contract

If native Work Package iCalendar subscriptions remain supported and useful:

- enable only the required OpenProject calendar module;
- create a private saved Work Package calendar;
- generate a persistent tokenized iCalendar subscription;
- use the native OpenProject feed directly from Apple Calendar/iCloud;
- do not add n8n, CalDAV middleware, or a proxy solely for this;
- treat the subscription URL as a bearer credential;
- do not commit it to Git.

Historical saved calendar was named `Cloud Infrastructure`.

Historical external client was Apple Calendar/iCloud.

Meetings-calendar integration was intentionally not required.

Acceptance should verify a temporary dated Work Package appears in the feed and disappears after deletion.

---

# 14. Nextcloud integration contract

Historical OpenProject ↔ Nextcloud integration was explicitly left **DEFERRED / CLEAN** because the stable Nextcloud/OpenProject integration combination required a source compatibility patch.

Therefore a future rebuild must not blindly recreate Nextcloud integration.

At rebuild time:

1. check whether current stable Nextcloud and current stable OpenProject integration components support each other natively;
2. if yes, it may be implemented if still useful;
3. if completion requires local source patches, compatibility shims, downgrade, version hold, or pin solely for this integration, leave it disabled unless the operator explicitly changes the decision.

Do not recreate historical failed-test residue.

---

# 15. Internal application integration contract

When the current host has a private application-to-application network, connect only OpenProject components that actually need cross-service communication.

Historical intent:

- application web/API reachable by n8n;
- background worker able to deliver outgoing webhooks;
- shared database traffic kept conceptually distinct from general application integration traffic.

Do not automatically recreate network name `edge_internal` or subnet `172.30.0.0/24`.

Instead:

- discover the current internal application network;
- use its current DNS/service aliases;
- attach only required OpenProject roles;
- do not attach unrelated OpenProject helpers merely for convenience.

If no such network exists and n8n/OpenProject integration is required, create the simplest suitable private communication path consistent with current architecture.

---

# 16. SSRF contract

Historical OpenProject required an explicit SSRF allowlist so its webhook subsystem could call n8n on the private application network.

Future behavior:

- preserve SSRF protection;
- if a native OpenProject webhook must target a private internal service, add only the minimum current allowlist necessary for that internal network/endpoint;
- do not globally disable SSRF protection;
- do not reuse historical subnet values unless they are still current.

---

# 17. n8n integration contract

If n8n remains the automation layer, rebuild the OpenProject integration using native OpenProject webhooks plus OpenProject API access.

Historical functional design:

### OpenProject → n8n

- outgoing webhook scoped to the relevant OpenProject project;
- events:
  - work package created;
  - work package updated;
- delivery over the private application path;
- signed request;
- n8n rejects invalid/missing signatures;
- successful ingress responds quickly and does not wait for downstream chat delivery.

### n8n → OpenProject

- dedicated OpenProject API credential;
- internal API endpoint when available;
- correct public Host/application-host semantics where required by OpenProject;
- credential stored natively in n8n, not in Git.

Historical n8n objects:

- workflow `OpenProjectEventIngress01`;
- display name `OpenProject Event Ingress`;
- HMAC credential `OpenProjectWebhookHMAC01`;
- API credential `OpenProjectAPI01`.

These names may be reused for continuity but are not mandatory if n8n conventions have changed.

Historical signature algorithm was HMAC-SHA1 because that was the OpenProject webhook contract at the time. Use the current native signature mechanism in the future; do not force SHA1 if upstream changes it.

Acceptance must include:

- missing/invalid signature rejected;
- valid signature accepted;
- real created event;
- real updated event;
- API read from n8n to OpenProject;
- cleanup of test objects.

---

# 18. Mattermost notification contract

If Mattermost remains deployed and OpenProject notifications are still desired, preserve the architectural separation:

- OpenProject emits event;
- n8n validates and normalizes;
- n8n dispatches asynchronously;
- dedicated Mattermost integration identity posts to a dedicated OpenProject channel.

Historical objects:

- bot username `openproject`;
- display name `OpenProject`;
- private channel `openproject`;
- n8n credential `OpenProjectMattermostAuth01`;
- n8n sub-workflow `OpenProjectMattermost01`.

Do not rely on historical Mattermost user/channel IDs or tokens.

Future Codex must discover or recreate the appropriate current IDs.

Keep notification dispatch decoupled so Mattermost failure cannot make OpenProject webhook delivery fail or block.

Acceptance should verify both created and updated Work Package notifications.

---

# 19. Hermes / Codex / Antigravity boundaries

Historical design intentionally avoided direct Codex or Antigravity integrations with OpenProject.

Future default:

- GitHub remains the code implementation boundary;
- n8n remains the general automation/event integration boundary where applicable;
- Hermes may use OpenProject API workflows if there is still a concrete user workflow;
- Codex and Antigravity do not require their own permanent OpenProject credentials merely because they can call APIs.

Do not create duplicate integration paths without a current requirement.

---

# 20. Backup contract

OpenProject must be incorporated into the current backup framework.

The backup must capture at minimum:

- logical database state;
- persistent attachment/application-data state.

For a consistent snapshot, use the current supported application/database consistency strategy. Historical implementation temporarily quiesced OpenProject web/worker/cron, dumped PostgreSQL, copied persistent opdata, then restarted and verified readiness.

Do **not** blindly recreate that exact quiesce script if the future stack has a better supported backup mechanism.

Requirements:

- backup failure must fail closed;
- empty/invalid database dump must not be accepted;
- application must be returned to its pre-backup running state after backup;
- post-backup application readiness must be verified;
- backup tooling must not disrupt unrelated applications on a shared PostgreSQL instance.

If a Backrest/Restic architecture remains present, integrate OpenProject through that current framework rather than adding a parallel backup product.

---

# 21. Monitoring contract

Integrate OpenProject into the current monitoring framework only to the level useful for this single-operator environment.

Monitor the current equivalents of:

- public OpenProject availability;
- primary web/API role;
- required worker/background processing;
- required scheduled-job role;
- required cache/proxy/helper roles only if they are still independent runtime components.

Do not preserve historical container checks for services that no longer exist in future OpenProject architecture.

Alerts must describe the actual current topology.

---

# 22. Maintenance / update contract

OpenProject should participate in the current Maintenance/Semaphore model if that framework still exists.

Future rules:

- current stable release track;
- standard upstream update mechanism;
- no historical major-version lock merely because 2026 used major 17;
- no historical digest pin unless required for a concrete rollback/regression condition;
- discovery must fail closed rather than inventing a fallback version;
- update should use the current supported application lifecycle;
- health validation must reflect actual persistent services;
- one-shot migration/seeding jobs must not be incorrectly treated as permanently running services;
- shared components must not be restarted or replaced unnecessarily.

If current OpenProject now has a simpler native updater, prefer it over maintaining a custom update driver unless the project has a concrete reason to keep the custom path.

---

# 23. Portal / navigation contract

If the edge portal still exists, add an OpenProject entry using the current portal design conventions.

Do not restore historical HTML literally.

Requirements:

- correct OpenProject public URL;
- consistent visual placement with current portal;
- responsive layout remains intact;
- no regression to unrelated portal actions.

---

# 24. Secrets and credentials

This file intentionally contains no reusable secret material.

During rebuild:

- generate or retrieve credentials using the native service lifecycle;
- store OpenProject local secrets in the current host-local protected configuration mechanism;
- store n8n secrets as n8n credentials;
- store Mattermost bot token in the corresponding native integration credential;
- store GitHub/OpenProject webhook authentication material only in the services that need it;
- keep bearer iCalendar URLs out of Git;
- do not commit SMTP passwords, DB passwords, API tokens, webhook secrets, session secrets, or private keys.

Historical credential values are not required for reconstructing the architecture.

---

# 25. Clean upstream / local customization principle

Where upstream deployment repositories are used:

- keep tracked upstream files clean whenever practical;
- place site-specific changes in supported local overrides/configuration;
- do not patch upstream source for normal host integration;
- document any unavoidable deviation and its reason.

Historical OpenProject upstream Git tree was clean and local behavior was implemented through environment and override files. Preserve that **principle**, not necessarily those exact file names.

---

# 26. Minimalism rules

A future Codex rebuild must actively avoid recreating unnecessary historical complexity.

Examples:

- if current OpenProject no longer needs a separate proxy container, do not recreate one;
- if current upstream no longer needs autoheal, do not add it;
- if current OpenProject integrates directly with the current internal service network without an SSRF exception, do not add an obsolete exception;
- if native backup hooks replace manual quiesce/restart, use them;
- if a current integration has become unsupported or irrelevant, report it rather than manufacturing compatibility layers.

The target is functional equivalence with fewer moving parts where possible.

---

# 27. Acceptance gates

A rebuild is not complete merely because containers start.

Codex must verify the relevant gates below.

## Core

- application starts successfully;
- persistent storage mounted and writable;
- database migrations complete;
- public HTTPS login/UI reachable;
- generated application URL uses intended public hostname;
- application survives recreation/restart;
- upstream source tree/config ownership is as designed;
- no unexpected public database/backend exposure.

## DNS / ingress

- public DNS resolves as intended;
- TLS certificate valid;
- HTTP/HTTPS routing works;
- internal containers do not accidentally resolve the public FQDN to an OpenProject-only private network alias;
- reverse-proxy headers and WebSocket behavior are correct for the features actually enabled.

## Database

- database role is non-superuser unless upstream absolutely requires otherwise;
- required extensions present;
- normal application DB operations succeed;
- unrelated shared databases remain unaffected.

## Mail

- OpenProject real test message sends successfully;
- SMTP authentication succeeds;
- peer certificate verification succeeds;
- expected sender identity appears.

## GitHub

When enabled:

- repository webhook exists;
- authentication/signature validation works;
- ping/test delivery succeeds;
- a harmless real PR/repository event is visible in OpenProject.

## iCalendar

When enabled:

- feed returns valid calendar content;
- temporary dated Work Package appears;
- event disappears after Work Package deletion;
- bearer URL remains outside Git.

## n8n

When enabled:

- invalid signature rejected;
- valid event accepted;
- real created and updated events delivered;
- n8n → OpenProject API query succeeds;
- test objects removed.

## Mattermost

When enabled:

- dedicated integration credential authenticates;
- private OpenProject channel exists;
- created/updated event messages arrive through the n8n path;
- webhook ingress does not block on Mattermost delivery.

## Nextcloud

If not natively compatible:

- integration remains absent and clean.

If enabled:

- native OAuth/storage/file workflow completes with no patches or version holds unless explicitly accepted by the operator.

## Backup

- database dump or equivalent valid;
- persistent application data captured;
- snapshot completes;
- OpenProject returns healthy afterward.

## Monitoring

- current OpenProject runtime appears correctly in monitoring;
- public availability check passes;
- no checks reference retired historical container roles.

## Maintenance

- OpenProject version discovery works;
- update preflight works;
- health validation matches current topology;
- no obsolete historical target lock remains without current justification.

## Non-regression

Verify at least the currently relevant shared services:

- PostgreSQL;
- Mattermost;
- Nextcloud;
- n8n;
- Hermes;
- edge ingress;
- backup framework;
- monitoring framework.

---

# 28. Failure and recovery behavior

If a rebuild step fails:

1. identify the exact failed layer;
2. do not blindly repeat the entire deployment;
3. preserve already-valid shared infrastructure;
4. inspect partial OpenProject state;
5. recover to a known safe point;
6. continue only the missing portion;
7. verify non-regression afterward.

Do not destroy an existing database or persistent data merely because a new application deployment failed.

---

# 29. Documentation after rebuild

After successful acceptance, Codex should update the canonical Cloud Infrastructure repository with:

- current OpenProject deployment contract/manifests where appropriate;
- CURRENT_STATE with confirmed runtime facts;
- DECISIONS only for new accepted architectural decisions;
- Maintenance/monitoring/backup definitions reflecting the new real topology;
- no secrets.

Do not rewrite this historical baseline as though the future deployment had always used the new architecture.

---

# 30. Historical 2026 baseline — non-authoritative reference

Everything in this section is **historical evidence only**.

It exists to help future Codex understand what capabilities were actually proven before OpenProject was replaced by Plane.

Do not use these values as mandatory future configuration.

## Host

- host: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS;
- kernel `7.0.0-34-generic`;
- Docker 29.8.1;
- Compose 5.5.1.

## OpenProject deployment

- historical path: `/opt/openproject`;
- upstream repository: `opf/openproject-docker-compose`;
- branch: `stable/17`;
- historical application track: `17-slim`;
- historical application image digest:
  `sha256:48952034215d2a8ecf07086db86be55c74819cc76aa26af61f8da9ce5f06eda2`;
- upstream tracked tree clean;
- local override and `.env` held edge-specific configuration.

## Historical runtime roles

Persistent running containers:

- web;
- worker;
- cron;
- cache;
- proxy;
- autoheal.

Seeder existed as a one-shot Compose service.

Embedded OpenProject PostgreSQL and Hocuspocus were disabled.

Real-time text collaboration was disabled.

## Historical persistent data

- named volume: `openproject_opdata`;
- historical size: approximately 908K;
- attachments under application assets/files;
- external consumers: zero.

## Historical database

Shared PostgreSQL service with:

- database: `openproject`;
- role: `openproject`;
- size at audit: approximately 46 MB;
- 212 non-system tables;
- 3 projects;
- 6 users;
- 93 work packages.

Historical required extensions observed:

- `btree_gist`;
- `pg_trgm`;
- `unaccent`.

## Historical networking

OpenProject-owned networks:

- `openproject_frontend`;
- `openproject_backend`.

Shared networks:

- `postgres_net` for DB access;
- `edge_internal` for application integration.

Historical application aliases on `edge_internal`:

- `openproject`;
- `openproject-worker`.

Historical public hostname:

- `projects.escloud.us`.

Historical loopback publication:

- `127.0.0.1:18082`.

The public FQDN was intentionally **not** used as an OpenProject Docker DNS alias after a collision was discovered.

## Historical mail

- Stalwart;
- `mail.escloud.us:465`;
- implicit TLS;
- SMTP AUTH `plain`;
- verify peer;
- sender mailbox `openproject@escloud.us`.

## Historical GitHub integration

- project `Cloud Infrastructure`;
- identifier `cloud-infrastructure`;
- dedicated non-admin integration actor `github-integration`;
- dedicated integration role;
- native GitHub repository webhook;
- no GitHub PAT;
- webhook used OpenProject API-token authentication plus signature verification.

## Historical iCalendar

- native Work Package calendar;
- private saved calendar `Cloud Infrastructure`;
- Apple Calendar/iCloud subscription;
- read-only native feed;
- bearer URL excluded from repository.

## Historical Nextcloud state

Final state before replacement:

- OpenProject integration deferred;
- no active `integration_openproject` app/config;
- no integration-specific OAuth client;
- no OpenProject Storage/ProjectStorage link;
- no local patch, shim, version hold or downgrade.

## Historical n8n integration

- outgoing OpenProject webhook over private application network;
- events:
  - work package created;
  - work package updated;
- HMAC signature validation;
- ingress workflow `OpenProjectEventIngress01`;
- OpenProject API credential `OpenProjectAPI01`;
- webhook HMAC credential `OpenProjectWebhookHMAC01`;
- successful requests returned HTTP 204;
- invalid signatures returned HTTP 401.

Historical OpenProject SSRF allowlist covered the private application network rather than disabling SSRF globally.

## Historical Mattermost integration

- dedicated bot `openproject`;
- dedicated private channel `openproject`;
- n8n Mattermost credential `OpenProjectMattermostAuth01`;
- sub-workflow `OpenProjectMattermost01`;
- asynchronous dispatch;
- created and updated Work Package events verified end-to-end.

## Historical backup

Host backup preparation:

- quiesced web/worker/cron;
- dumped OpenProject PostgreSQL database;
- validated dump;
- copied persistent opdata;
- restarted application roles;
- waited for application readiness.

## Historical monitoring

Edge Monitor explicitly checked:

- public OpenProject availability;
- web;
- worker;
- cron;
- cache;
- proxy;
- autoheal.

## Historical Maintenance

Maintenance/Semaphore had a dedicated OpenProject update unit and update helper.

Historical implementation locked routine updates to the then-current major/track. This historical lock **must not be carried into a future rebuild** unless current compatibility independently requires one.

## Historical canonical drift at final audit

At the pre-decommission audit:

- canonical Caddyfile matched runtime;
- canonical `docker-compose.override.yml` was stale relative to runtime.

The live runtime override additionally contained:

- SMTP settings;
- internal application-network membership;
- neutral web hostname;
- OpenProject internal aliases;
- scoped SSRF allowlist.

Therefore the historical canonical override alone is **not** a complete reconstruction source.

The complete historical evidence set is:

1. this rebuild contract;
2. `OPENPROJECT_PRE_DECOMMISSION_AUDIT_2026-10-01.md`;
3. relevant latest ACCEPTED entries in `DECISIONS.md`;
4. historical OpenProject sections in `CURRENT_STATE.md`;
5. sanitized deployment files under `deployments/edge/openproject/`;
6. backup artifacts, if historical user data itself needs restoration.

---

# 31. Codex one-command task contract

When the operator asks Codex to restore OpenProject from this document, interpret the request as:

> Audit the current Cloud Infrastructure environment and rebuild OpenProject so that it restores the useful capabilities and integration boundaries defined in `OPENPROJECT_REBUILD_CONTRACT.md`. Use current stable upstream software and current supported deployment methods. Treat all historical paths, IPs, versions, image digests, container names and network names as reference only. Reuse current shared infrastructure where appropriate, avoid unnecessary new components, preserve native authentication and the project's single-operator trust model, recreate only currently useful integrations, verify all applicable acceptance gates, and update canonical documentation after successful acceptance. Do not introduce version pins, compatibility shims, source patches, extra auth layers or duplicate services without a concrete current need.

Codex must still perform the audit phase first. This is intentionally a high-level execution contract, not permission to mutate unknown current state blindly.

---

# 32. Final invariant

A successful future rebuild is one where the operator regains the same **useful OpenProject experience and integration behavior** with the simplest current architecture.

It is **not** one where the 2026 filesystem, container topology, versions, network subnets, image digests and workarounds have been reproduced byte-for-byte.
