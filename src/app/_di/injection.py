from src.infra.resource.manager import ResourceManager
from src.infra.api.opensearch import OpenSearch
from src.infra.opensearch.initializer import IndexInitializer
from src.infra.opensearch.mapping import PROFILES_INDEX_MAPPING
from src.domain.search.service.search_service import SearchService

_resource_manager = ResourceManager({})

opensearch = OpenSearch()
_search_service = SearchService(opensearch=opensearch)
_index_initializer = IndexInitializer(opensearch=opensearch)
