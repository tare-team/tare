"""GraphQL schema definitions."""

import strawberry

@strawberry.type
class Query:
    """Root GraphQL query."""

    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL"

schema = strawberry.Schema(query=Query)
