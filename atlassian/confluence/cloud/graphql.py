"""Confluence Cloud GraphQL Gateway operations."""

from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit

from ...confluence_base import ConfluenceBase


class GraphQLOperations(ConfluenceBase):
    """Operations for the evolving Atlassian GraphQL Gateway schema."""

    _ADVANCED_SEARCH_QUERY = """
    query AdvancedAGGSearchQuery(
      $experience: String!,
      $query: String!,
      $first: Int,
      $filters: SearchFilterInput!
    ) {
      search {
        search(
          experience: $experience,
          query: $query,
          first: $first,
          filters: $filters
        ) {
          edges {
            node {
              id
              title
              type
              url
              ... on SearchConfluencePageBlogAttachment {
                excerpt
              }
            }
          }
          totalCount
        }
      }
    }
    """

    def _graphql_url(self) -> str:
        """Return the GraphQL gateway URL for the configured Cloud site."""
        parsed = urlsplit(self.url)
        if parsed.hostname == "api.atlassian.com":
            return "https://api.atlassian.com/graphql"
        return f"{parsed.scheme}://{parsed.netloc}/gateway/api/graphql"

    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute an Atlassian GraphQL Gateway query or mutation.

        GraphQL schema fields may be added, deprecated, or removed independently
        of this package. The raw GraphQL response is therefore returned so that
        callers can inspect both ``data`` and GraphQL ``errors``.
        """
        response = self.post(
            self._graphql_url(),
            json={"query": query, "variables": variables or {}},
            absolute=True,
        )
        return response or {}

    def search_graphql(
        self,
        query: str,
        cloud_id: str,
        first: int = 25,
        entities: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Search Confluence content through the experimental GraphQL search API.

        ``cloud_id`` is the Confluence site cloud ID. The raw GraphQL response
        is returned; successful results are at
        ``data.search.search`` and contain ``edges`` and ``totalCount``. The
        GraphQL schema is not versioned, so callers should inspect its
        ``errors`` field before consuming data.
        """
        if not query:
            raise ValueError("query must not be empty")
        if not 1 <= first <= 100:
            raise ValueError("first must be between 1 and 100")

        variables = {
            "experience": "confluence.advancedSearch",
            "query": query,
            "first": first,
            "filters": {
                "entities": entities
                or [
                    "ati:cloud:confluence:page",
                    "ati:cloud:confluence:attachment",
                    "ati:cloud:confluence:blogpost",
                    "ati:cloud:confluence:space",
                ],
                "locations": [f"ari:cloud:confluence::site/{cloud_id}"],
            },
        }
        return self.graphql(self._ADVANCED_SEARCH_QUERY, variables)
