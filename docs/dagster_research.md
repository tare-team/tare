# Dagster Research

- Dagster is described as a "cloud-native data pipeline orchestrator for the whole development lifecycle" with integrated lineage and observability.
- Dagster exposes a GraphQL API that lets clients query runs and metadata and launch executions. The API is served from the webserver at the `/graphql` endpoint.
- Dagster's web interface (`dagit`) is a React application that can be run in development mode via `NEXT_PUBLIC_BACKEND_ORIGIN="http://localhost:3333" yarn start`.

These features inspired the layered layout for this repository's initial skeleton.
