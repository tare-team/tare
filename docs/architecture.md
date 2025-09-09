# Tare Architecture Overview

This document captures the initial design for the Tare data orchestration framework.  It draws inspiration from Dagster's proven patterns while laying out Tare's own structure.

## 1. Monorepo layout

```
tare/
├── python_modules/
│   ├── tare/
│   ├── tare-graphql/
│   ├── tare-webserver/
│   └── libraries/
├── js_modules/
│   └── tare-ui/
├── helm/
│   └── tare/
└── docs/
```

## 2. Core components

- **gRPC server architecture** – user code runs in isolated processes that communicate via gRPC.
- **Repository system** – repositories collect assets, jobs, and schedules through decorators.
- **GraphQL API** – exposes repositories, assets, jobs, and code locations.
- **Webserver** – serves the GraphQL API and React UI.

## 3. Deployment considerations

- Helm chart enables Kubernetes deployments with separate user code servers.
- Hybrid model supports cloud control plane with on‑prem execution.

## 4. Development phases

1. gRPC server, repository definitions, and CLI.
2. GraphQL schema, React UI, and workspace management.
3. Scheduling, partitioning, and extensible libraries.

## 5. Migration principles

- Definitions are loaded from workspace files.
- Decorator‑based APIs with backwards compatibility.
