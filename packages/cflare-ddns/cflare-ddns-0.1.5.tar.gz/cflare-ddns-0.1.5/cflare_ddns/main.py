import sys
import time
from cflare_ddns import args
from cflare_ddns import config
from cflare_ddns.ddns import ddns


def main():
    try:
        while 1:
            args_parse = args.init()
            ap = args_parse.parse_args()
            if ap.config_file is None:
                print("Please specify config file")
            conf = config.parse(ap.config_file)
            for rec in conf["records"]:
                ddns(
                    email=conf["email"],
                    api_key=conf["api_key"],
                    zone_id=rec["zone_id"],
                    domain=rec["domain"],
                    record_name=rec["record_name"],
                )
            if ap.interval is None:
                sys.exit(0)
            print(f"Sleeping for {ap.interval} seconds")
            time.sleep(ap.interval)
    except Exception as err:
        print(err)
        sys.exit(1)
