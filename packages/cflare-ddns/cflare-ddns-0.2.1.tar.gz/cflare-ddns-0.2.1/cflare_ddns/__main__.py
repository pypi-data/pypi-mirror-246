from cflare_ddns.main import main
from cflare_ddns.args import init


def start():
    args_parse = init()
    args = args_parse.parse_args()
    main(args)


if __name__ == "__main__":
    start()
