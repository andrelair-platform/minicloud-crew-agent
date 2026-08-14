# minicloud-crew-agent

[![CI](https://github.com/andrelair-platform/minicloud-crew-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/andrelair-platform/minicloud-crew-agent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Supply chain: cosign](https://img.shields.io/badge/supply%20chain-cosign%20signed-green)](https://github.com/sigstore/cosign)

> Three-agent CrewAI pipeline (Researcher → Analyst → Compliance Checker) exposed as an OpenAI-compatible FastAPI service. Registered as `model: deep-research-agent` in the minicloud LiteLLM proxy for compliance-validated financial and insurance research. Runs on the self-hosted minicloud k8s platform (5-node k3s cluster) in the `ai` namespace.

**Live docs:** https://andrelair-platform.github.io/minicloud-crew-agent/
**Platform docs:** https://andrelair-platform.github.io/minicloud-platform-docs/

---

## Table of Contents

- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [CI/CD Pipeline](#cicd-pipeline)
- [Endpoints](#endpoints)
- [Environment variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Architecture

```
Open WebUI / any OpenAI client
        │  model: deep-research-agent
        ▼
  LiteLLM proxy (ai ns)
        │  routes to minicloud-crew-agent:8081
        ▼
  minicloud-crew-agent (FastAPI)
        │
        ▼
  CrewAI — sequential process
  ┌─────────────────────────────────────────┐
  │ 1. Researcher   (mistral-small)         │
  │    tools: rag_search + web_search       │
  │            │                            │
  │ 2. Analyst  (mistral-large)             │
  │    synthesises research into answer     │
  │            │                            │
  │ 3. Compliance (mistral-large)           │
  │    verifies regulatory claims via RAG   │
  └─────────────────────────────────────────┘
        │
        ▼
  Validated answer returned to client
```

| Concern | Choice |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI + uvicorn |
| Agent orchestration | CrewAI (sequential, 3 agents) |
| LLM routing | LiteLLM proxy (`mistral-small` / `mistral-large`) |
| Tools | `rag_search` (internal KB) + `web_search` (DuckDuckGo) |
| Registry | `harbor.10.0.0.200.nip.io/library/minicloud-crew-agent` |
| GitOps | `minicloud-gitops/services/minicloud-crew-agent/` |
| Namespace | `ai` |

---

## Getting Started

```bash
# Prerequisites: Python 3.12
pip install -r requirements.txt

# Run locally
LITELLM_BASE_URL=https://litellm.devandre.sbs \
LITELLM_API_KEY=<your-key> \
uvicorn app.main:app --port 8081 --reload

# Lint + test
pip install -r requirements-test.txt
make lint
make test
```

---

## CI/CD Pipeline

| Step | Trigger | Tool |
|---|---|---|
| L0 lint | every push | ruff + mypy |
| L1 unit tests | every push | pytest (≥70% coverage) |
| Build + push | push to `main` | docker buildx → Harbor |
| Sign | push to `main` | cosign keyless |
| GitOps bump | push to `main` | `kustomize edit set image` in `services/minicloud-crew-agent/minicloud-1/prod/` |

**Branch strategy:** `dev` direct push · `staging` PR required · `main` PR required

| Secret | Scope | Purpose |
|---|---|---|
| `TS_OAUTH_CLIENT_ID` | org | Tailscale CI tag |
| `TS_OAUTH_SECRET` | org | Tailscale CI tag |
| `MINICLOUD_CA_CERT` | org | Harbor TLS trust |
| `HARBOR_USER` | org | Harbor push |
| `HARBOR_PASSWORD` | org | Harbor push |
| `GITOPS_TOKEN` | org | GitOps overlay update |

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness — returns `{"status":"ok"}` |
| GET | `/ready` | Readiness — returns `{"status":"ready"}` |
| GET | `/v1/models` | Lists available agent models |
| POST | `/v1/chat/completions` | OpenAI-compatible chat; supports `stream: true` |

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `LITELLM_BASE_URL` | `http://litellm.ai.svc.cluster.local:4000` | LiteLLM proxy base URL |
| `LITELLM_API_KEY` | `none` | LiteLLM master key |
| `RAG_INGEST_URL` | `http://rag-ingest.ai.svc.cluster.local:8001` | RAG query service URL |
| `CREW_SMALL_MODEL` | `mistral-small` | Model for Researcher agent (tool-calling) |
| `CREW_LARGE_MODEL` | `mistral-large` | Model for Analyst + Compliance agents |
| `CREW_MAX_ITER` | `8` | Max iterations per agent |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
