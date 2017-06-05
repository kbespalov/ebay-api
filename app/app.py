import argparse
import prettytable
import yaml
import logging
import sys
import api

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
LOG = logging.getLogger(__name__)


def print_dump(items):
    """Print result of api.dump as table"""
    columns = ['item_id', 'title', 'quantity', 'price', 'url']
    table = prettytable.PrettyTable(columns)
    for item in items:
        table.add_row([item.ItemID,
                       item.Title,
                       item.QuantityAvailable,
                       item.BuyItNowPrice.value,
                       item.ListingDetails.ViewItemURL])
    print table


def store_dump(items, file_path):
    """Store result of api.dump as yaml file"""
    formatted = {}
    for item in items:
        formatted[int(item.ItemID)] = {
            'Title': item.Title,
            'QuantityAvailable': int(item.QuantityAvailable),
            'BuyItNowPrice': {
                'value': float(item.BuyItNowPrice.value),
                '_currencyID': item.BuyItNowPrice._currencyID
            },
            'ListingDetails': {
                'ViewItemURL': item.ListingDetails.ViewItemURL
            }
        }
    with open(file_path, 'w') as f:
        yaml.dump(formatted, f, default_flow_style=False)


def load_dump(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f)


def dump(config):
    """Retrieve, print and store active items"""
    items = api.dump(config)
    print_dump(items)
    store_dump(items, config.file)


def update(config):
    """Load dumped items from yaml file and applies changes"""

    stored_items = load_dump(config.file)
    current_items = api.dump(config)
    require_update = []

    for item in current_items:
        if int(item.ItemID) in stored_items:
            stored_item = stored_items[int(item.ItemID)]
            diff = {}
            msg = '%s is changed from: %s to: %s'

            quantity = int(stored_item['QuantityAvailable'])
            if quantity != int(item.QuantityAvailable):
                diff['QuantityAvailable'] = quantity
                LOG.info(msg % ('QuantityAvailable', item.QuantityAvailable,
                                quantity))

            title = stored_item['Title']
            if title != item.Title:
                LOG.info(msg % ('Title', item.Title, title))
                diff['Title'] = title

            price = stored_item['BuyItNowPrice']
            if price['value'] != float(item.BuyItNowPrice.value):
                diff['BuyItNowPrice'] = price
                LOG.info(msg % ('BuyItNowPrice', item.BuyItNowPrice.value,
                                price['value']))

            if diff:
                diff['ItemID'] = item.ItemID
                require_update.append({'Item': diff})

    if require_update:
        api.update(config, require_update)
    else:
        LOG.info('Nothing has changed.')


def get_parser():
    """Build a parser of command line interface"""

    description = 'eBay API command line interface'
    base = argparse.ArgumentParser(description=description, add_help=False)

    subparsers = base.add_subparsers(help='list of commands')

    cmd = 'dump'
    dump_parser = subparsers.add_parser(cmd, help='dump a list of items')
    dump_parser.set_defaults(cmd=dump)

    cmd = 'update'
    update_parser = subparsers.add_parser(cmd, help='update a list of items')
    update_parser.set_defaults(cmd=update)

    # adding of common arguments
    for p in [dump_parser, update_parser]:
        p.add_argument('-c', '--config', dest='config_file',
                       default='./etc/ebay.yml',
                       help='a configuration file in yaml format')
        p.add_argument('-d', '--domain', dest='domain',
                       default='api.sandbox.ebay.com',
                       help='default ebay api domain')
        p.add_argument('-f', '--file', dest='file',
                       default='./out/items.yml',
                       help='use given file for dumping or loading')

    return base


def start():
    parser = get_parser()
    namespace = parser.parse_args(sys.argv[1:])
    namespace.cmd(namespace)
