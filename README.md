# Tare

Initial monorepo scaffolding for the Tare data orchestration framework.  The layout mirrors Dagster's separation of concerns with distinct Python packages, a React UI, and deployment configuration.

## Repository layout

- `python_modules/`
  - `tare/` – core library placeholder
  - `tare-graphql/` – FastAPI app exposing a Strawberry GraphQL schema
  - `tare-webserver/` – webserver placeholder
  - `libraries/` – space for extension libraries
- `js_modules/`
  - `tare-ui/` – React UI built with Vite that queries the GraphQL API
- `helm/`
  - `tare/` – starter Helm chart
- `docs/` – design notes and research

## Development

### Unified development environment

Spin up all services with a single command:

```bash
uv run tare dev
```

This starts Redis and Postgres via Docker, runs the GraphQL API server, and
launches the React development server. Stop with `CTRL+C`.

### Individual services

#### Python GraphQL API

```bash
# Install dependencies for the GraphQL package
uv sync --package tare-graphql

# Run the API
uv run --package tare-graphql uvicorn tare_graphql.main:app --reload

# Execute tests
uv run --package tare-graphql pytest python_modules/tare-graphql/tests -q
```

#### UI

```bash
npm install --prefix js_modules/tare-ui
npm run dev --prefix js_modules/tare-ui
npm test --prefix js_modules/tare-ui
```

The UI expects the API to be served from the same origin at `/graphql`.
