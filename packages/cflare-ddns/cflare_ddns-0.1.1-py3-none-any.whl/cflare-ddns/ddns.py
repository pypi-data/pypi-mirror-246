import api
import ip


def ddns(
    email: str,
    api_key: str,
    zone_id: str,
    domain: str,
    record_name: str,
):
    new_ip = ip.get_public()
    current_ip, current_record_id = api.get_ip(
        email,
        api_key,
        zone_id,
        domain,
        record_name,
    )
    if new_ip != current_ip:
        api.set_ip(
            email,
            api_key,
            zone_id,
            domain,
            record_name,
            current_record_id,
            new_ip,
        )
    else:
        print("IP address did not change.")
