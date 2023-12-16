import sys
import time
from cflare_ddns import config
from cflare_ddns.ddns import ddns
from cflare_ddns import ip


def main(args):
    try:
        while 1:
            conf = config.parse(args.config_file)
            new_ip = ip.get_public()
            print(f"Your public ip: {new_ip}")
            for rec in conf["records"]:
                ddns(
                    email=conf["email"],
                    api_key=conf["api_key"],
                    zone_id=rec["zone_id"],
                    domain=rec["domain"],
                    record_name=rec["record_name"],
                    new_ip=new_ip,
                )
            if args.interval is None:
                sys.exit(0)
            print(f"Sleeping for {args.interval} seconds")
            time.sleep(args.interval)
    except Exception as err:
        print(err)
        sys.exit(1)
