from cflare_ddns.main import main
from cflare_ddns.args import init


if __name__ == "__main__":
    args_parse = init()
    args = args_parse.parse_args()
    main(args)
