# Stage 02.5 — Remaining Standalone Core Services / Hermes Selection Acceptance

Date: 2026-09-17

Status: **ACCEPTED**

## Scope result

The `Remaining Standalone Core Services` research block is complete.

Only one additional standalone full service is selected for deployment before cross-site connectivity-dependent services:

- **Hermes Agent — SELECTED**.

No other reviewed standalone candidate is part of Stage 3. Notification brokers remain a later Monitoring/Alerts decision; password/2FA remains optional; feed/change-detection/search/capture products remain post-infrastructure workflow decisions unless a later concrete requirement proves that a dedicated service is necessary.

## Why Hermes is a distinct infrastructure service

Hermes is not treated as a duplicate of n8n, CloudCLI, Codex CLI or Antigravity CLI.

Accepted role separation:

- **n8n** — deterministic automation/orchestration: schedules, webhooks, mail/API triggers, explicit workflow state and data routing;
- **Hermes** — persistent cloud-side agent runtime: agentic reasoning, tool use, supervisory logic and delegation;
- **CloudCLI** — manual web/remote Cloud AI workspace for the user;
- **Codex CLI** — specialized OpenAI coding/agent executor, directly usable by the user and delegatable by Hermes;
- **Antigravity CLI / `agy`** — specialized Google cloud-agent/coding executor, directly usable by the user and delegatable by Hermes;
- **OpenClaw in Home/PAI** — local personal-agent role centered on Home/PAI resources and local inference;
- **vLLM on `ai-node`** — local inference backend to be made available to Hermes only after cross-site connectivity is accepted.

CloudCLI is not an execution proxy between Hermes and Codex/Antigravity. Hermes should invoke supported providers/executors directly.

## Stage 3 composition

Future deployment stage:

`03 — Edge Hermes Agent Runtime`

Stage 3 contains **Hermes only** plus the infrastructure-level integration required to use already accepted executors.

Stage 3 does not contain Capture Inbox, vendor/document watchers, bounded research jobs, mail automations or other user-specific n8n/Hermes workflows.

## Runtime placement

Preferred deployment: **host-native under shared service account `core`**.

Reason:

- Codex CLI and Antigravity CLI are already installed and authenticated in the host-side `core` environment;
- Hermes needs direct executor/tool access;
- containerizing Hermes would require unnecessary binary/auth/runtime/keyring bridging into the container;
- for this use case Docker therefore adds complexity rather than improving the operating model.

This is an accepted exception to Docker-by-default. Reconsider containerization only if a concrete Stage 3 upstream/compatibility finding makes host-native materially worse.

## Accepted infrastructure flow

Stage 3 must be designed around the future flow:

```text
Internet / schedule / mail / webhook
                |
               n8n
                |
        deterministic steps
                |
                v
             Hermes
        agentic reasoning
          +-----+-----+
          |     |     |
          v     v     v
        Codex   AGY   vLLM
          |             ^
          v             |
       result     enabled after Stage 4
          |
          v
         n8n
          |
notification / storage / next step
```

Stage 3 should verify a minimal infrastructure path:

`n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`

This acceptance flow must prove integration without implementing user-specific business automation.

The Hermes -> vLLM branch is part of the accepted target architecture but remains **DEFERRED** until Stage 4 provides accepted `edge ↔ ai-node` connectivity.

## Public exposure

No public Hermes domain or listener is accepted by assumption. Stage 3 should keep Hermes private/loopback where possible and expose only what the concrete integration contract requires.

## Roadmap impact

The post-Stage-02.5 planned order is now:

1. Stage 3 — Edge Hermes Agent Runtime;
2. Stage 4 — Edge Cross-site Connectivity Foundation;
3. Stage 5 — Edge Cross-site Data & Knowledge Services;
4. Stage 6 — conditional Remaining Infrastructure Services;
5. Stage 7 — Edge Backrest & Recovery;
6. Stage 8 — Edge Maintenance & Update, including separate Codex `update.escloud.us` substage;
7. Stage 9 — Edge Monitoring, Heartbeats & Alerts;
8. Stage 10 — Edge Cloud Portal, including separate Codex `app.escloud.us` substage;
9. Stage 11 — Edge Final Integrated Infrastructure Acceptance;
10. post-infrastructure Automation & User Workflows continuous workstream.

If Stage 6 is empty at Stage 02.5 closure, it should be removed and downstream numbering normalized rather than creating an empty branch.

## Stage boundary

This acceptance selects Stage 3 composition only. Stage 02.5 remains ACTIVE / RESEARCH-ONLY.

No Hermes installation/configuration is authorized until the complete Stage 02.5 research matrix, normalized service inventory, dependency graph and final stage roadmap are accepted and persisted.

Immediate next research block:

**Cross-site Connectivity Foundation — базовая связь `edge ↔ ai-node ↔ PVE/Home`.**