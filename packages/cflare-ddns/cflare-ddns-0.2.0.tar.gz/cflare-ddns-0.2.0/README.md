# cflare-ddns

This is yet another Cloudflare Dynamic DNS application.

## Usage

```shell
usage: cflare-ddns [-h] [-c CONFIG_FILE] [-i INTERVAL]

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        Path to your configuration file
  -i INTERVAL, --interval INTERVAL
                        Number of seconds between each sync. This will make the program run forever.
```

## Configuration file example

```json
{
  "api_key": "xxxx",
  "email": "xxxx@gmail.com",
  "records": [
    {
      "zone_id": "xxxx",
      "domain": "xxx.xyz",
      "record_name": "xxx"
    }
  ]
}
```
