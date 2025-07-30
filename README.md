# BizDetails AI

BizDetails AI is a prototype application for mapping company names to verified domains and enriching business data. This repository currently contains a small HTML demo, but the intended platform will rely on a modern full-stack architecture.

## Core Technology Stack

| Layer | Tech Choices | Notes |
| --- | --- | --- |
| **Frontend** | React.js, Next.js, Tailwind CSS | SEO-friendly, scalable UI/UX |
| **Backend** | FastAPI, Python, Celery, Redis | Async API with background tasks |
| **Database (Transactional)** | PostgreSQL | Structured data for companies and domains |
| **Database (Graph)** | Neo4j or ArangoDB | Parent-subsidiary relationships |
| **Search** | Elasticsearch or Typesense | Fuzzy company/domain search |
| **Web Scraping** | Playwright, BeautifulSoup, Scrapy | Extract homepage and WHOIS data |
| **LLM Integration** | LangChain, OpenLLM, HuggingFace | Intelligent domain inference (optional) |
| **Task Queue** | Celery + Redis | For enrichment and validation jobs |
| **Containerization** | Docker, Docker Compose, Kubernetes (k3s) | Production ready deployment |
| **Version Control & CI/CD** | GitHub & GitHub Actions | Code pipeline and testing |
| **Auth** | Auth0 (free tier) or Keycloak | Secure login and RBAC |
| **Monitoring** | Grafana, Prometheus, Loki | Logs and metrics |
| **Governance (optional)** | OpenMetadata, Apache Atlas | Schema and audit trail |

## Layer‑Wise Architecture

1. **Frontend Web App**
   - Next.js with Tailwind CSS
   - State via Redux Toolkit or Zustand
   - Data fetching through SWR or React Query
   - Authentication using Keycloak or Auth0
   - Visualizations with Recharts or D3.js

2. **Backend / API Layer**
   - FastAPI with SQLAlchemy ORM
   - Graph database integration (Neo4j/ArangoDB)
   - Background jobs powered by Celery + Redis
   - OAuth2/OpenID via Keycloak or FastAPI Users
   - Optional LLM logic wrapped through LangChain

3. **Data Layer**
   - PostgreSQL for transactional data
   - Graph store such as Neo4j for ownership trees
   - Regular backups via `pg_dump`

4. **Search & Matching**
   - Typesense or Elasticsearch for fuzzy search and autocomplete

5. **Enrichment & AI (optional)**
   - WHOIS parsing and scraping via Playwright
   - LLM integration for domain inference
   - Celery queues for pipeline orchestration

6. **DevOps / Hosting**
   - Docker & docker-compose for local development
   - Kubernetes (k3s) for lightweight clusters
   - Monitoring with Grafana/Prometheus and logging via Loki

7. **Access Control & Admin**
   - Keycloak for authentication and RBAC
   - Admin dashboards built in Next.js or tools like Retool

This outline serves as a blueprint for future development while the HTML demo offers a preview of the product experience.
