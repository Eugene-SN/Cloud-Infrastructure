# Cloud Infrastructure — Architecture

## Status

**Architecture status:** discovery / target composition in progress.

This document is not yet the final Cloud Infrastructure Architecture Contract. Service composition is being determined before topology and implementation details.

## System model

Cloud Infrastructure is one layer of a three-part personal infrastructure:

```text
                        Internet / Cloud AI
                               |
                               |
                      Cloud Infrastructure
                              edge
                    /          |          \
            Public edge   Cloud services   AI integrations
                    \          |          /
                         Private backbone
                         /              \
                        /                \
          Home Infrastructure     Personal Agents Infrastructure
                 PVE                       ai-node
```

### Home Infrastructure

General-purpose home compute/service plane centered on Proxmox VE, the home LAN and home infrastructure services.

### Personal Agents Infrastructure

Local AI/agent/data plane centered on `ai-node`: local LLM inference, ASR/OCR, knowledge processing, RAG and AI-centric automation.

### Cloud Infrastructure

Public/cloud complement using the strengths of an external 24/7 VPS: public routability, foreign location, external IP, public endpoints, cloud AI subscriptions/providers, Internet-facing automation, external coordination and off-site failure-domain roles.

Cloud Infrastructure is not intended to become a second Home Infrastructure or a second local AI compute node.

## Target node naming

- Legacy/as-is host: `nl-core-vds`
- Future logical primary cloud node: `edge`

`edge` is deliberately provider- and country-agnostic.

## Accepted target application core

The following product choices are accepted for future `edge` and are not currently subject to replacement research:

### Public connectivity / ingress

- Xray
- Hysteria2
- nginx

Xray/Hysteria2 provide the user-facing foreign VPS/DPI-bypass function. This is separate from any future private infrastructure connectivity.

### Automation and cloud AI

- n8n
- CloudCLI
- Codex CLI
- Antigravity CLI

Codex CLI and Antigravity CLI form the accepted core for subscription-based cloud model usage. CloudCLI is the accepted cloud AI workspace/interface component. Exact integration paths between these components are not yet designed.

### Mail and web authentication

- Stalwart
- Bulwark
- Authelia

Authelia is intended as the common web authentication entry point for services exposed under `escloud.us`, with native application authentication disabled only where explicitly supported and operationally correct.

## Accepted replacement directions

### Backup operations

- Restic remains acceptable as the underlying backup engine.
- Future clean deployment will use **Backrest** as the backup management/orchestration layer.
- The legacy same-host Restic repository is not the final disaster-recovery design.

### Portal / status UI

- Legacy Homepage will not be carried forward as-is.
- A dedicated Cloud Infrastructure page will be created, conceptually similar to the existing `home.lan` experience, including status/monitoring and useful operational integrations.

### Maintenance

- Legacy custom Maintenance Center will not be carried forward.
- Target direction: maintenance page + Semaphore, following the currently accepted Home/PVE operational model.

## Open functional decisions

The following are intentionally unresolved until requirements and alternatives are evaluated:

### File/storage layer

Requirements already identified:

- selected VPS working storage should be mountable/usable from MacBook, iPhone and `ai-node`;
- web browsing, uploading, downloading and editing of selected VPS files should remain available;
- the same working data may need to be available to cloud AI/automation workflows.

Filestash is a candidate but not accepted as the final implementation.

### Synchronization

Syncthing is not yet accepted for the target state. Candidate uses include synchronization of working files, scripts and selected directories between `edge` and Home/PAI. Its role must be evaluated independently from cloud-AI task transport.

### Obsidian

Canonical vault remains on `ai-node`:

`/srv/ai-data/knowledge/obsidian`

The useful role of `edge` remains open. Requirements include free/self-hosted synchronization for MacBook/iPhone/iPad/`ai-node` without paid Obsidian Sync. Candidate mechanisms may include Syncthing-compatible iOS clients, Self-hosted LiveSync/CouchDB, or WebDAV/Remotely Save, but no mechanism is accepted yet.

## Explicitly deferred architecture questions

Do not settle these until the complete service/function set has been agreed:

- private-backbone technology;
- NetBird suitability for Russia ↔ external VPS;
- service-to-service network topology;
- ingress/domain layout;
- container vs systemd placement;
- Docker network structure;
- storage directory layout;
- authentication wiring between individual applications;
- monitoring implementation details;
- final backup/off-site DR topology;
- migration-in-place versus clean Ubuntu rebuild.
