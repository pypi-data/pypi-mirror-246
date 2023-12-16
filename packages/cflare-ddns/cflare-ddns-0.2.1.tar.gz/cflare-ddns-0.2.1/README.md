# cflare-ddns

This is yet another Cloudflare Dynamic DNS application.

[![PyPI - Version](https://img.shields.io/pypi/v/cflare-ddns)](https://pypi.org/project/cflare-ddns/) ![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54) ![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?logo=Cloudflare&logoColor=white) [![License](https://img.shields.io/github/license/Ileriayo/markdown-badges)](./LICENSE)

## Installation

```shell
pip install cflare-ddns
```

## Usage

First is you need to create a config file. You can place it in the default location `/etc/cflare-ddns.json` or anywhere in your filesystem that is readable by the script. You'll need to pass that config location in the cli if it's not the default location.

Edit the config file, you'll need to provide the following:

- `api_key` - You can get this in your cloudflare dashboard. Follow this [link](https://developers.cloudflare.com/fundamentals/api/get-started/keys/) to get full instructions.
- `email` - The email account you use in cloudflare.
- `zone_id` - [Zone ID](https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/) of your domain name.
- `domain` - The domain name. Example: `example.com`
- `record_name` - The sub domain you want to update with your public ip. This subdomain should be an `A` record type. Example: `www`

Configuration file example:

```json
{
  "api_key": "xxxx",
  "email": "xxxx@gmail.com",
  "records": [
    {
      "zone_id": "xxxx",
      "domain": "example.xyz",
      "record_name": "vpn"
    },
    {
      "zone_id": "xxxx",
      "domain": "example.sh",
      "record_name": "www"
    }
  ]
}
```

Running the script with config in the default location:

```shell
cflare-ddns
```

Running the script with config in non-default location:

```shell
cflare-ddns -c /opt/somewhere/config.json
```

You can add this to your [cronjobs](https://crontab.guru/) to run periodically.

```shell
* * * * * cflare-ddns
- - - - -
| | | | |
| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
| | | ------- Month (1 - 12)
| | --------- Day of month (1 - 31)
| ----------- Hour (0 - 23)
------------- Minute (0 - 59)
```

To run every 15 minutes:

```cron
*/15 * * * * cflare-ddns
```

### CLI Reference

```shell
usage: cflare-ddns [-h] [-c CONFIG_FILE] [-i INTERVAL] [-v]

options:
  -h, --help            show this help message and exit
  -v, --version         App version
  -c CONFIG_FILE, --config CONFIG_FILE
                        Path to your configuration file.
                        Default paths:
                          /etc/cflare-ddns.json,
                          cflare-ddns.json
  -i INTERVAL, --interval INTERVAL
                        Number of seconds between each sync. This will make the program run
                        forever.Hit Ctrl-C to stop.
```
