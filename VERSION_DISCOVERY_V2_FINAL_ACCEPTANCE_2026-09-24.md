# Version Discovery v2 — Final Acceptance — 2026-09-24

## Status

**COMPLETE / ACCEPTED**

Final marker:

`VERSION_DISCOVERY_V2_FINAL_ACCEPTANCE=PASS`

## Scope

This corrective work updates the already-accepted Edge Maintenance version-discovery path. It does not create a new infrastructure stage and does not alter the manual-only Maintenance execution policy.

## Accepted problem statement

The previous Docker remote-version implementation could reuse remote values from `status.json` and then rewrite the status timestamp on every refresh. That allowed stale remote data to become effectively self-refreshing. Registry-V2-only discovery also hit Docker Hub unauthenticated pull-rate limits, while GitHub REST release discovery could independently exhaust the anonymous GitHub API quota.

These were discovery-correctness defects, not update-driver failures.

## Accepted source model

- Persistent cross-run remote Docker cache is removed.
- Docker Hub images use the public Docker Hub Tags API for fresh floating-tag digest and version discovery.
- `docker.n8n.io/n8nio/n8n:stable` is resolved through the Docker Hub `n8nio/n8n` tag API; Docker Hub Registry V2 is not required for n8n discovery.
- Mattermost exact semantic version is resolved from same-digest Docker Hub tag aliases.
- Authelia, PostgreSQL and Stalwart use the corresponding same-digest alias model.
- Nextcloud exact patch resolution uses the official `nextcloud/docker` `versions.json`; the exact tag is bound to the floating tag by the Linux/amd64 descriptor digest.
- Redis exact patch resolution uses the official Redis release index; the exact tag is bound to the floating tag by the Linux/amd64 descriptor digest.
- Bulwark remains resolved through GHCR registry metadata.
- GitHub-native components resolve latest releases through the ordinary `github.com/<owner>/<repo>/releases/latest` redirect rather than `api.github.com`.
- Update availability remains based on the running local image digest versus the current floating remote digest.
- Unresolved current remote state remains fail-closed as `STABLE_UNRESOLVED` / `CHECK_FAILED`; stale persistent fallback is not restored.
- The existing `maintenance.json` freshness/safety constraint remains independent of remote-version caching.

## Runtime acceptance

The final runtime candidate was executed while both former bottlenecks were demonstrably unavailable:

- Docker Hub Registry V2 control returned HTTP 429;
- GitHub REST control returned HTTP 403.

Despite those controls being unavailable, the final candidate resolved all required external versions and passed:

- `FULL_CANDIDATE_GATE=PASS|COMPONENTS=16`;
- n8n: installed `2.40.5`, available `2.40.6`, `UPDATE_AVAILABLE`;
- Mattermost: installed `11.11.0`, available `11.11.1`, `UPDATE_AVAILABLE`;
- Antigravity: installed `1.2.9`, available `1.2.10`, `UPDATE_AVAILABLE`;
- Docker current rows retained matching running/remote digests;
- GitHub-native current rows resolved without GitHub REST latest-release dependency.

Production refresh then passed with:

- `DASHBOARD_UNRESOLVED_COUNT=0`;
- `CHECK_FAILED_COUNT=0`;
- `PRODUCTION_STATE_GATE=PASS`;
- `LEGACY_DEPENDENCY_GATE=PASS`;
- `SELF_REFRESHING_REMOTE_CACHE=NO`;
- `UNBOUNDED_STALE_FALLBACK=NO`;
- `GITHUB_REST_LATEST_DEPENDENCY=NO`;
- `DOCKER_HUB_REGISTRY_DISCOVERY_DEPENDENCY=NO`.

Accepted runtime collector Git blob:

`19397985821a1204cde4333b40775bc0a4cef306`

## Canonical repository acceptance

The exact accepted runtime collector was persisted byte-for-byte to the canonical repository.

Canonical commit:

`46c3a3a9e8eb650eb4b1b050320d4df128eed49e`

Commit message:

`fix(maintenance): make version discovery rate-limit resilient`

The obsolete `EDGE_MAINTENANCE_FORCE_REGISTRY_COMPONENT` path was removed from the update playbook because forced per-component registry refresh is no longer part of the accepted architecture.

Repository persistence gates passed:

- `RUNTIME_REPO_BYTE_IDENTITY=PASS`;
- `FINAL_SYNC_GATE=PASS`;
- `FINAL_WORKTREE_GATE=PASS`;
- `VERSION_DISCOVERY_V2_REPO_PERSIST=PASS`.

## Semaphore delivery-path acceptance

A fresh post-commit Refresh was executed through the normal operator path.

Semaphore task:

- task ID: `33`;
- template: `01. Refresh — Edge Maintenance Status`;
- started: `2026-09-24T20:57:44+03:00`;
- completed: `2026-09-24T20:58:09+03:00`.

After that task:

- checkout `HEAD` = `46c3a3a9e8eb650eb4b1b050320d4df128eed49e`;
- cached `origin/main` = the same commit;
- `FETCH_HEAD` contains the same commit and was refreshed at task execution;
- checkout collector blob = `19397985821a1204cde4333b40775bc0a4cef306`;
- status row count = `24`;
- `UNRESOLVED_COUNT=0`;
- `CHECK_FAILED_COUNT=0`;
- maintenance snapshot age at acceptance = 9 seconds.

Final delivery markers:

- `SEMAPHORE_POST_COMMIT_TASK=PASS`;
- `SEMAPHORE_CHECKOUT_UPDATE=PASS`;
- `VERSION_DISCOVERY_V2_FINAL_ACCEPTANCE=PASS`.

## Supersedes

This acceptance supersedes only the previous current implementation assumptions that:

- persistent cross-run Docker remote-version cache is part of the current Maintenance discovery model;
- Docker Hub Registry V2 is required for Docker Hub/n8n version discovery;
- GitHub REST API is required for latest-release discovery;
- `EDGE_MAINTENANCE_FORCE_REGISTRY_COMPONENT` is required by the post-update refresh path.

All non-conflicting Stage 7 / Stage 07.2 decisions, including native-first update ownership and strictly operator-triggered manual Maintenance execution, remain accepted.
