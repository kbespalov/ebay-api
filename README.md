# ebay-api

An example of ebay sandbox api app.

Not for production usage.

How to use:

- Install requirements: `pip install -r requirements.txt`
- Configure API access options like `appid`, `token` and `devid` in `./etc/ebay.yml` file.
- Dump current list of active items:
   `python ./ebay-api/cmd.py dump`
   an output will be stored into `./out/items.yml` file.
- Change reqiured fields at `./out/items.yml`
- Do update:
  `python ./ebay-api/cmd.py update`


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
