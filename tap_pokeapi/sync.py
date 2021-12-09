import requests
import singer

LOGGER = singer.get_logger()


def sync_pokemons(client, pokemon_qty=10):
    method = 'GET'

    pokemons = []

    for pokemon_id in range(1, pokemon_qty + 1):
        path = f'pokemon/{pokemon_id}'
        response = client.request(method, path=path)

        pokemons.append(response)

    return pokemons


def sync(client, config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.streams:
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        bookmark_column = stream.replication_key
        is_sorted = False

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        max_bookmark = None
        for row in sync_pokemons(client, pokemon_qty=10):

            # write one or more rows to the stream:
            singer.write_records(stream.tap_stream_id, [row])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state(
                        {stream.tap_stream_id: row[bookmark_column]})
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, row[bookmark_column])
        if bookmark_column and not is_sorted:
            singer.write_state({stream.tap_stream_id: max_bookmark})
    return
