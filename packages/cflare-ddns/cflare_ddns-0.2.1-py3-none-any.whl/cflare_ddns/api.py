import requests
from cflare_ddns import exceptions as ex

BASE_URL = "https://api.cloudflare.com/client/v4/zones"


def headers(
    email: str,
    api_key: str,
):
    """
    This will construct the header dict. It will get the
    variables from the config file.

    Args:
        email (str): Cloudflare email account
        api_key (str): Cloudflare api_key

    Returns:
        dict: Header dict
    """
    return {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json",
    }


def set_ip(
    email: str,
    api_key: str,
    zone_id: str,
    domain: str,
    record_name: str,
    record_id: str,
    new_ip: str,
) -> None:
    """
    This will set a new ip

    Args:
        email (str): Cloudflare email account
        api_key (str): Cloudflare api_key
        zone_id (str): Zone id from cloudflare
        domain (str): Your domain name
        record_name (str): Your subdomain name
        record_id (str): Record id
        new_ip (str): New ip to set

    Returns:
        None
    """
    url = f"{BASE_URL}/{zone_id}/dns_records/{record_id}"
    data = {
        "type": "A",
        "name": f"{record_name}.{domain}",
        "content": new_ip,
    }

    response = requests.put(
        url,
        headers=headers(email, api_key),
        json=data,
    )
    result = response.json()

    if response.status_code == 200 and result["success"]:
        print(f"A record updated successfully. New IP: {new_ip}")
    else:
        msg = f'Failed to update A record. Error: {result["errors"]}'
        raise ex.RecordUpdateError(msg)


def get_ip(
    email: str,
    api_key: str,
    zone_id: str,
    domain: str,
    record_name: str,
) -> (str, str):
    """
    This will get the current ip and record_id

    Args:
        email (str): Cloudflare email account
        api_key (str): Cloudflare api_key
        zone_id (str): Zone id from cloudflare
        domain (str): Your domain name
        record_name (str): Your subdomain name

    Returns:
        tuple
            - str: current ip
            - str: current record id
    """

    # Get the current A record details
    url = f"{BASE_URL}/{zone_id}/dns_records"
    url += f"?type=A&name={record_name}.{domain}"

    response = requests.get(
        url,
        headers=headers(email, api_key),
    )
    data = response.json()

    if response.status_code == 200 and data["success"]:
        # Extract the current A record ID and IP address
        current_record_id = data["result"][0]["id"]
        current_ip = data["result"][0]["content"]
        return current_ip, current_record_id
    else:
        msg = f'Failed to fetch A record details. Error: {data["errors"]}'
        raise ex.RecordNotFound(msg)
