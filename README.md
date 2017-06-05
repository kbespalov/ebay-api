# Ebay Items Command Line Interface

An example of ebay sandbox api app.

Not for production usage.

## How to use:

- Clone and install the package:
  - `git clone https://github.com/kbespalov/ebay-api`
  - `pip install ./ebay-api`

- Specify required for api acces options like `appid`, `token` and `devid` at  the `./ebay-api/etc/ebay.yml` file:

    ```
    # configuration file of api access to the ebay sandbox

    active_domain: api.sandbox.ebay.com
    items_store: ./out/items.yml

    api.sandbox.ebay.com:
        compatability: 989
        appid: -
        certid: -
        devid: -
        token: -
    ```

- Dump current list of active items:
   `ebaycli dump`
```
+--------------+---------------------+----------+--------+--------------------------------------------------------+
|   item_id    |        title        | quantity | price  |                          url                           |
+--------------+---------------------+----------+--------+--------------------------------------------------------+
| 110201097051 |     Iphone 10S+     |   1000   | 200.0  |  http://cgi.sandbox.ebay.com/Iphone-10S-/110201097051  |
| 110201097088 |        AK-47        |   400    | 1000.0 |    http://cgi.sandbox.ebay.com/AK-47-/110201097088     |
| 110201097746 | How to use ebay api |   1000   | 100.0  | http://cgi.sandbox.ebay.com/use-ebay-api-/110201097746 |
| 110201097992 |       My Book       |   111    |  10.0  |   http://cgi.sandbox.ebay.com/My-Book-/110201097992    |
+--------------+---------------------+----------+--------+--------------------------------------------------------+
```
   an output will be formatted as `yaml` format and stored into `./out/items.yml` file by default.

- Change required for you fields at `./out/items.yml`. Available for change fields:
    - title
    - quantity
    - price.value

- Do update:
  `ebaycli update`
```
Changes:
+--------------+---------+----------+-------+---------------------------------------------------+
|   item_id    |  title  | quantity | price |                        url                        |
+--------------+---------+----------+-------+---------------------------------------------------+
| 110201097992 | My Book | 111 > 11 |  10.0 | http://cgi.sandbox.ebay.com/My-Book-/110201097992 |
+--------------+---------+----------+-------+---------------------------------------------------+
```



Use `-h` to get more details:
```
python cmd.py dump -h
usage: cmd.py dump [-h] [-c CONFIG_FILE] [-d DOMAIN] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        a configuration file in yaml format
  -d DOMAIN, --domain DOMAIN
                        default ebay api domain
  -f FILE, --file FILE  use given file for dumping or loading
```