from singer.catalog import Catalog, CatalogEntry
from tap_pokeapi.schema import load_schemas

STREAMS = {
    'pokemons': {
        'key_properties': ['id']
    }
}

def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        stream_metadata = []
        key_properties = STREAMS[stream_id]['key_properties']

        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)
