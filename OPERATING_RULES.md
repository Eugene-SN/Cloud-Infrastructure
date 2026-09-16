# Cloud Infrastructure — Operating Rules

## Project identity

- **Project name:** Cloud Infrastructure
- **Primary repository:** `Eugene-SN/Cloud-Infrastructure`
- **GitHub workflow:** ON
- **Target primary VPS node:** `edge`
- `edge` is a logical, location-agnostic name. Do not encode the current country, provider, or datacenter into target-state node naming.

## Project scope

Cloud Infrastructure is the cloud/public-facing layer of one personal infrastructure composed of three cooperating projects:

- **Home Infrastructure** — home general-purpose compute/service plane centered on Proxmox VE and home-network services.
- **Personal Agents Infrastructure (PAI)** — local AI/agent/data-processing plane centered on `ai-node`.
- **Cloud Infrastructure** — public/cloud layer using the strengths of an external 24/7 VPS: public routability, foreign location, external IP, Internet-facing services, cloud AI integrations, external coordination and off-site roles.

Cloud Infrastructure must complement Home Infrastructure and PAI rather than copy them without a concrete reason.

## Historical baseline invariant

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` is the canonical historical/as-is snapshot of the legacy VPS as of 2026-09-14.

- Keep its historical/current names such as `nl-core-vds` and legacy service/path terminology.
- Do not retroactively rename or rewrite it to match the new taxonomy.
- Do not treat its deployed architecture as the target architecture.
- Do not infer future necessity from current service activity, inactivity, installation, or lack of use.
- Apply `Cloud Infrastructure` and `edge` naming only to target-state, planning, architecture, deployment and migration materials.

## Current work stage

The project is in **service/function discovery and target-composition analysis**.

Current ordering is mandatory unless explicitly changed by a later ACCEPTED decision:

1. Evaluate existing legacy VPS services and decide what is worth carrying forward.
2. Identify missing high-value Cloud Infrastructure functions/services.
3. Agree the complete functional/service composition of `edge`.
4. Only then design service relationships, network topology, ingress, storage layout, runtime/container topology and deployment architecture.
5. Produce and accept a Cloud Infrastructure Architecture Contract.
6. Produce a migration/rebuild plan.
7. Only then mutate runtime infrastructure.

Do not design the future topology around the current legacy deployment before the service composition is settled.

## Runtime mutation gate

Until the Architecture Contract and implementation/migration stage are explicitly accepted, do not:

- install or remove VPS services;
- update packages or containers;
- change networking, firewall, DNS or routing;
- rename the host;
- install a private-backbone solution;
- modify the current deployment merely because research finds a newer approach.

GitHub project-context maintenance is allowed and is separate from runtime mutation.

## Source-of-truth and persistence rules

For project context, use the latest applicable ACCEPTED decisions as the controlling intent. Current factual runtime state must still be verified from runtime/configuration when implementation depends on it.

Before modifying project files:

1. read the current repository state;
2. avoid duplicate documents and duplicate facts;
3. update the existing canonical document for that topic;
4. read back critical writes.

Store structured project context, not chat transcripts. Preserve decision chronology in `DECISIONS.md`.

## Decision semantics

Decision statuses are:

- `PROPOSED`
- `ACCEPTED`
- `SUPERSEDED`
- `REJECTED`
- `DEPRECATED`

The latest applicable `ACCEPTED` decision has priority. A `SUPERSEDED`, `REJECTED` or `DEPRECATED` decision is historical only.

## Git and secrets

- Do not commit credentials or secrets to a public repository.
- Persistent configuration/design/runbooks may be stored in Git when secret material is excluded.
- The repository is shared persistent context for future Cloud Infrastructure branches and tools.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without a demonstrated use case.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are a separate function from any future private infrastructure backbone.
- A private backbone, if required, must be tested in the real Russia ↔ external-VPS path before being accepted; do not assume WireGuard-based connectivity will be reliable under DPI.
- Reinstallation/rebuild of the legacy VPS remains an allowed future migration outcome; do not optimize prematurely for in-place migration.
