# AGENTS.md

## Project Overview

TARE (타래) is a modern data orchestration framework that implements a Queue-Worker architecture for flexible, distributed job execution. Unlike DAG-based systems, TARE enables workers to dynamically delegate jobs to other workers, creating thread-like (타래) execution patterns that can branch, wait, or proceed independently. The framework is designed for teams building complex data pipelines that require dynamic job routing, conditional execution paths, and real-time monitoring of distributed workflows.

## Technology Stack

### Backend
- **Python 3.12+** - Core framework and worker implementation
- **FastAPI** - High-performance async web framework for API server
- **Strawberry GraphQL** - Type-safe GraphQL implementation
- **SQLAlchemy 2.0** - ORM for metadata storage and job state management
- **gRPC** - Inter-process communication between workers and control plane
- **Redis Streams** - Message queue for job distribution and worker coordination
- **multiprocessing** - Process isolation for worker execution

### Frontend
- **React 18** - UI framework for monitoring dashboard
- **Vite** - Build tool and development server
- **GraphQL Client** - For querying job state and system metrics

### Infrastructure
- **Docker** - Containerization for workers and services
- **Kubernetes** - Orchestration via Helm charts
- **uv** - Fast Python package and project manager

## Core Architecture Concepts

### Queue-Worker Pattern
```
Client → API → Queue → Worker → [Queue → Worker]* → Result
                ↓         ↓
            Monitor   Dead Letter
```

### Key Components

1. **Control Plane**
   - GraphQL API server (`tare-graphql/`)
   - Web UI for monitoring (`tare-ui/`)
   - Metadata database (job states, worker registry)
   - Queue manager (Redis Streams)

2. **Execution Environment**
   - Worker processes (isolated via multiprocessing)
   - gRPC servers for worker communication
   - Job executors with retry mechanisms
   - Resource managers

3. **Message Flow**
   - Jobs are submitted via GraphQL mutations
   - Queue manager distributes to available workers
   - Workers can delegate to other workers via job forwarding
   - Results flow back through event streams

## Coding Guidelines

### Python Code Style
- Use type hints for all function signatures
- Follow PEP 8 with 88-character line limit (Black formatter)
- Use dataclasses or Pydantic models for data structures
- Prefer composition over inheritance for worker definitions

### Worker Implementation Pattern
```python
from tare import Worker, Job, Context

@worker("data_processor")
class DataProcessor(Worker):
    async def execute(self, job: Job, ctx: Context) -> Result:
        # Process job
        if needs_delegation:
            await ctx.delegate_to("specialized_worker", sub_job)
        return Result(...)
```

### Error Handling
- Always use structured error types derived from `TareException`
- Implement exponential backoff for retries
- Log errors with full context including job_id, worker_id, and stack trace
- Failed jobs go to dead letter queue after max retries

### Testing Requirements
- Unit tests for all worker logic (pytest)
- Integration tests for queue-worker flows
- Use Docker containers for test infrastructure
- Mock external services, never call production APIs in tests

## Project Structure

```
tare/
├── python_modules/
│   ├── libraries/               # Shared libraries
│   ├── tare/                    # Core framework library
│   │   ├── worker/              # Worker base classes and decorators
│   │   ├── queue/               # Queue abstractions and implementations
│   │   ├── executor/            # Job execution engine
│   │   ├── monitoring/          # Event and metrics collection
│   │   └── workers/             # Built-in worker implementations
│   ├── tare-graphql/            # GraphQL API server
│   │   ├── schema/              # GraphQL schema definitions
│   │   ├── resolvers/           # Query and mutation handlers
│   │   └── subscriptions/       # Real-time event streams
│   └── tare-webserver/          # Web server for UI and API
│
├── js_modules/
│   └── tare-ui/                 # React monitoring dashboard
│       ├── components/          # Reusable UI components
│       ├── pages/               # Route-based page components
│       └── graphql/             # Generated GraphQL client code
│
├── helm/
│   └── tare/                   # Kubernetes deployment charts
│
└── docs/
    ├── architecture.md         # System design documentation
    └── dagster_research.md     # Comparative analysis notes
```

## Development Workflow

### Setting Up Development Environment
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup repository
git clone <repository>
cd tare
uv sync

# Start development services
docker-compose up -d redis postgres
uv run --package tare-graphql uvicorn tare_graphql.main:app --reload
npm install --prefix js_modules/tare-ui
npm run dev --prefix js_modules/tare-ui
```

### Creating a New Worker
1. Define worker class in `python_modules/tare/workers/`
2. Implement `execute()` method with job processing logic
3. Add unit tests in `tests/workers/`
4. Register worker in configuration
5. Document worker capabilities and requirements

### Testing Strategy
- **Unit Tests (70%)**: Test worker logic in isolation
- **Integration Tests (25%)**: Test queue-worker interactions
- **E2E Tests (5%)**: Test complete job workflows
- Run tests: `uv run pytest python_modules/*/tests/`

## API Patterns

### Job Submission
```graphql
mutation SubmitJob($input: JobInput!) {
  submitJob(input: $input) {
    id
    status
    worker
    queuedAt
  }
}
```

### Job Delegation (Worker-to-Worker)
```python
# Inside worker execution
result = await ctx.delegate_to(
    worker="downstream_processor",
    job=Job(data=transformed_data),
    wait=True,  # Block until completion
    timeout=300  # 5 minute timeout
)
```

### Monitoring Subscription
```graphql
subscription JobEvents($jobId: ID!) {
  jobEvents(jobId: $jobId) {
    eventType
    timestamp
    worker
    message
    metadata
  }
}
```

## Configuration Management

### Environment Variables
- `TARE_REDIS_URL` - Redis connection string
- `TARE_DATABASE_URL` - PostgreSQL connection string
- `TARE_GRPC_PORT` - gRPC server port (default: 50051)
- `TARE_WORKER_CONCURRENCY` - Max concurrent jobs per worker
- `TARE_QUEUE_POLL_INTERVAL` - Queue polling interval in seconds

### Worker Configuration
```yaml
# config/workers.yaml
workers:
  data_processor:
    concurrency: 4
    timeout: 300
    retries: 3
    retry_backoff: exponential

  specialized_worker:
    concurrency: 1
    memory_limit: "4Gi"
    requires_gpu: true
```

## Error Handling and Recovery

### Retry Mechanism
- Exponential backoff: 1s, 2s, 4s, 8s, 16s
- Max retries configurable per worker type
- Failed jobs stored in dead letter queue
- Manual retry available via GraphQL mutation

### Monitoring and Alerting
- Structured logging with correlation IDs
- Metrics exported to Prometheus format
- Worker health checks via gRPC
- Queue depth monitoring
- Job duration tracking

## Security Considerations

- All worker processes run in isolated environments
- gRPC communication uses TLS in production
- GraphQL API requires authentication tokens
- Job data encrypted at rest in Redis
- Audit logs for all job submissions and completions

## Performance Optimization

### Queue Management
- Use Redis Streams consumer groups for load balancing
- Implement queue priorities for critical jobs
- Batch processing for high-volume workflows
- Connection pooling for database and Redis

### Worker Scaling
- Horizontal scaling via Kubernetes HPA
- Vertical scaling based on job complexity
- Worker pools for different job types
- Resource limits to prevent memory leaks

## Troubleshooting Guide

### Common Issues
1. **Jobs stuck in queue**: Check worker health and Redis connectivity
2. **Worker crashes**: Review logs for OOM errors or unhandled exceptions
3. **Slow job processing**: Profile worker code, check for blocking I/O
4. **Queue overflow**: Scale workers or increase processing capacity

### Debug Commands
```bash
# Check worker status
uv run tare worker status

# Inspect queue depth
uv run tare queue stats

# Replay failed jobs
uv run tare jobs replay --from-dlq

# Export job traces
uv run tare trace export --job-id <id>
```

## Contributing Guidelines

### Code Review Checklist
- [ ] Type hints added for new functions
- [ ] Unit tests cover edge cases
- [ ] Documentation updated
- [ ] No hardcoded credentials
- [ ] Error handling implemented
- [ ] Performance impact considered

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Update relevant documentation
4. Run full test suite
5. Submit PR with clear description
6. Address review feedback
7. Squash and merge after approval

## Related Resources

- [Dagster Architecture](https://docs.dagster.io/concepts) - Inspiration for execution model
- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/) - Queue implementation details
- [gRPC Python Guide](https://grpc.io/docs/languages/python/) - IPC implementation
- [Strawberry GraphQL](https://strawberry.rocks/) - GraphQL schema reference

## Version Information

- Framework Version: 0.1.0
- Python Required: >=3.12
- API Version: v1
- Last Updated: 2024-01
