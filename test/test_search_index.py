import asyncio
import os
import unittest
from unittest.mock import AsyncMock, patch

os.environ["PROFILE_INDEX_NAME"] = "dev-profiles"

from src.domain.search.service.search_service import SearchService


class SearchIndexRoutingTest(unittest.TestCase):
    def setUp(self):
        self.opensearch = AsyncMock()
        self.opensearch.post.return_value.res_json = {"hits": {"hits": []}}
        self.opensearch.get.return_value.res_json = {"_source": {}}
        self.opensearch.delete.return_value.res_json = {"result": "deleted"}
        self.service = SearchService(opensearch=self.opensearch)

    def test_search_uses_configured_index(self):
        asyncio.run(self.service.get_mentor_list({}))
        self.opensearch.post.assert_awaited_once()
        self.assertEqual(
            self.opensearch.post.await_args.args[0],
            "/dev-profiles/_search",
        )

    def test_get_uses_configured_index(self):
        asyncio.run(self.service.get_mentor(123))
        self.opensearch.get.assert_awaited_once()
        self.assertEqual(
            self.opensearch.get.await_args.args[0],
            "/dev-profiles/_doc/123",
        )

    def test_delete_uses_configured_index(self):
        asyncio.run(self.service.delete_mentor(123))
        self.opensearch.delete.assert_awaited_once()
        self.assertEqual(
            self.opensearch.delete.await_args.args[0],
            "/dev-profiles/_doc/123",
        )


if __name__ == "__main__":
    unittest.main()
