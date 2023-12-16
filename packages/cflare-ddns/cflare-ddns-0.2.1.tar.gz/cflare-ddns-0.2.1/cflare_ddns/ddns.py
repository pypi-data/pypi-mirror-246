from cflare_ddns import api


def ddns(
    email: str,
    api_key: str,
    zone_id: str,
    domain: str,
    record_name: str,
    new_ip: str,
) -> None:
    """
    This will get the current ip and record_id

    Args:
        email (str): Cloudflare email account
        api_key (str): Cloudflare api_key
        zone_id (str): Zone id from cloudflare
        domain (str): Your domain name
        record_name (str): Your subdomain name
        new_ip (str): The new public ip

    Returns:
        None
    """
    print(f"Getting current ip for {record_name}.{domain}")
    current_ip, current_record_id = api.get_ip(
        email,
        api_key,
        zone_id,
        domain,
        record_name,
    )
    if new_ip != current_ip:
        print(f"Setting new ip for {record_name}.{domain}")
        api.set_ip(
            email,
            api_key,
            zone_id,
            domain,
            record_name,
            current_record_id,
            new_ip,
        )
        print(f"{record_name}.{domain} ip address set to {new_ip}")
    else:
        print(f"{record_name}.{domain} ip address did not change")
