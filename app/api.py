import itertools
import logging
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping

LOG = logging.getLogger(__name__)


def get_items(config, items):
    # todo: use GetMultipleItems instead of GetMyeBaySelling

    def chunks(l, n=20):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    raise NotImplemented()
    #
    # api = Shopping(domain=config.domain, config_file=config.config_file)
    # for ids in chunks(items.keys()):
    #     response = api.execute('GetMultipleItems', {
    #         'ItemID': ids,
    #         'IncludeSelector': 'ItemSpecifics',
    #     })
    #     print response
    #
    # return []


def dump(config):
    api = Trading(domain=config.domain, config_file=config.config_file)
    result = []

    def get_page(page_num):
        return api.execute('GetMyeBaySelling', {
            'ActiveList': {
                'Include': True,
                'Pagination': {
                    'PageNumber': page_num
                }
            },
            'OutputSelector': [
                'ActiveList.PaginationResult',
                'ActiveList.ItemArray.Item.Title',
                'ActiveList.ItemArray.Item.ItemID',
                'ActiveList.ItemArray.Item.BuyItNowPrice',
                'ActiveList.ItemArray.Item.ListingDetails.ViewItemURL',
                'ActiveList.ItemArray.Item.QuantityAvailable'
            ]
        })

    LOG.debug('dumping a list of selling items ...')
    for page_num in itertools.count(1):
        LOG.debug('items page: %d ' % page_num)
        response = get_page(page_num)
        active = response.reply.ActiveList
        page_count = int(active.PaginationResult.TotalNumberOfPages)
        result.extend(active.ItemArray.Item)
        if page_count == page_num:
            return result


def update(config, changes):
    api = Trading(domain=config.domain, config_file=config.config_file)
    for change in changes:
        try:
            api.execute('ReviseFixedPriceItem', change)
            LOG.info('%s is successfully changed. ' % change['Item']['ItemID'])
        except ConnectionError as error:
            LOG.error(error)
