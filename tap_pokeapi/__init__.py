#!/usr/bin/env python3
import json
import singer
from singer import utils
import sys
from tap_pokeapi.discover import discover
from tap_pokeapi.sync import sync

REQUIRED_CONFIG_KEYS = []
LOGGER = singer.get_logger()


def do_discover():
    LOGGER.info('Starting discover')
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info('Finished discover')


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        do_discover()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            do_discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
