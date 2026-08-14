---
id: intro
title: Overview
sidebar_label: Overview
slug: /
---

# minicloud Crew Agent

**Three-agent CrewAI pipeline** (Researcher → Analyst → Compliance Checker) exposed as an OpenAI-compatible FastAPI service. Registered as `model: deep-research-agent` in the minicloud LiteLLM proxy for compliance-validated financial and insurance research. Every answer is cross-checked by a regulatory compliance agent before being returned to the client.

## Responsibility

| In scope | Out of scope |
|---|---|
| CrewAI sequential pipeline (3 agents) | LiteLLM configuration (minicloud-gitops) |
| Researcher: `rag_search` + `web_search`, sourced citations | RAG ingestion (ai namespace manifests) |
| Analyst: synthesis into structured answer | Model serving (vLLM / LiteLLM) |
| Compliance Checker: regulatory claim validation via RAG | Open WebUI model registration |
| OpenAI-compatible `/v1/chat/completions` + streaming | |

## Stack

| Concern | Choice |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI + uvicorn (single worker — crew runs in executor) |
| Orchestration | CrewAI — sequential `Process` |
| LLM routing | LiteLLM proxy — `mistral-small` (Researcher) + `mistral-large` (Analyst + Compliance) |
| Tools | `rag_search` (RAG ingest API) + `web_search` (DuckDuckGo) |
| Container | `python:3.12-slim`, non-root UID 1000 |
| Registry | `harbor.10.0.0.200.nip.io/library/minicloud-crew-agent` |
| Namespace | `ai` (shared AI services namespace) |

## Agent pipeline

```
Client request
    │
    ▼
minicloud-crew-agent FastAPI
    │
    └─► CrewAI sequential crew
          │
          ├─ 1. Researcher (mistral-small, max_iter=8)
          │     tools: rag_search + web_search
          │     output: cited research findings [1][2]...
          │
          ├─ 2. Analyst (mistral-large, max_iter=4)
          │     input: research findings (context)
          │     output: structured answer — executive summary,
          │             key facts, regulatory context,
          │             practical implications
          │
          └─ 3. Compliance Checker (mistral-large, max_iter=8)
                tool: rag_search (regulatory cross-check)
                input: research + analysis (context)
                output: validated answer + optional "Compliance note:"
```

## Why a sequential crew rather than a single agent?

A single ReAct agent (`minicloud-agent`) answers general research questions. The crew adds **two extra review passes**:

1. **Analyst** rewrites raw findings into a structured, professional format suited for financial/insurance audiences.
2. **Compliance Checker** independently verifies every regulatory reference (ACPR, AMF, Solvency II, MiFID II, GDPR) using `rag_search`. Errors are corrected and flagged before the answer reaches the client.

The trade-off: latency is 3–5× higher than the single agent. Use `deep-research-agent` when accuracy matters more than speed.

## GitOps location

```
minicloud-gitops/services/minicloud-crew-agent/
  base/
    deployment.yaml      # no namespace, no image tag
    service.yaml
    kustomization.yaml
  minicloud-1/
    prod/
      kustomization.yaml  # namespace: ai, images.newTag bumped by CI on main push
      certificate.yaml    # crew-agent.10.0.0.200.nip.io TLS
      ingress.yaml        # internal-only; proxy-read-timeout 600s (3 agents × 8 iter)
```

## Links

- [GitHub repository](https://github.com/andrelair-platform/minicloud-crew-agent)
- [LiteLLM](https://litellm.devandre.sbs)
- [Open WebUI](https://chat.devandre.sbs)
- [Platform documentation](https://andrelair-platform.github.io/minicloud-platform-docs/)
