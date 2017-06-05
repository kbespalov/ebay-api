import argparse
import prettytable
import yaml
import logging
import sys
import api

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
LOG = logging.getLogger(__name__)


def print_items(items):
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
            'title': item.Title,
            'quantity': int(item.QuantityAvailable),
            'price': {
                'value': float(item.BuyItNowPrice.value),
                'currency': item.BuyItNowPrice._currencyID
            },
            'url': item.ListingDetails.ViewItemURL
        }

    with open(file_path, 'w') as f:
        yaml.dump(formatted, f, default_flow_style=False)


def load_dump(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f)


def dump(config):
    """Retrieve, print and store active items"""
    items = api.dump(config)
    if items:
        print_items(items)
        store_dump(items, config.file)


def update(config):
    """Load dumped items from yaml file and applies changes"""

    def color(obj):
        return '\033[92m' + str(obj) + '\033[0m'

    stored_items = load_dump(config.file)
    current_items = api.dump(config)

    changes = []
    changed_items = []

    for item in current_items:
        if int(item.ItemID) in stored_items:
            stored_item = stored_items[int(item.ItemID)]
            diff = {}
            stored = int(stored_item['quantity'])
            current = int(item.QuantityAvailable)
            if stored != current:
                item.QuantityAvailable = color('%s > %s' % (current, stored))
                diff['Quantity'] = stored
            stored = stored_item['title']
            current = item.Title
            if stored != current:
                diff['Title'] = stored
                item.QuantityAvailable = color('%s > %s' % (current, stored))

            stored = stored_item['price']
            current = float(item.BuyItNowPrice.value)
            if stored['value'] != current:
                diff['StartPrice'] = {
                    '#text': stored['value'],
                    '@attrs': {'currencyID': stored['currency']}
                }
                item.BuyItNowPrice.value = color('%s > %s' % (current, stored))
            if diff:
                diff['ItemID'] = item.ItemID
                changes.append({'Item': diff})
                changed_items.append(item)

    if changes:
        print 'Changes:'
        print_items(changed_items)
        if raw_input('apply (y/N) ? ') == 'y':
            api.update(config, changes)
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

    for p in [dump_parser, update_parser]:
        p.add_argument('-c', '--config', dest='config_file',
                       default='./etc/ebay.yml',
                       help='a configuration file in yaml format')
        p.add_argument('-d', '--domain', dest='domain',
                       help='default ebay api domain')
        p.add_argument('-f', '--file', dest='file',
                       default='./out/items.yml',
                       help='use given file for dumping or loading')

    return base


def get_config():
    parser = get_parser()
    namespace = parser.parse_args(sys.argv[1:])
    with open(namespace.config_file) as f:
        c = yaml.load(f)
    if not namespace.domain:
        if c.get('active_domain', None):
            namespace.domain = c['active_domain']
        else:
            namespace.domain = 'api.sandbox.ebay.com'
    if not namespace.file:
        if c.get('items_store', None):
            namespace.domain = c['items_store']
        else:
            namespace.file = './out/items.yml'
    return namespace


def start():
    c = get_config()
    if c.cmd:
        c.cmd(c)
