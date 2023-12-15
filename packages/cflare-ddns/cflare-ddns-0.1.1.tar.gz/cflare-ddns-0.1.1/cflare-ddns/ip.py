import re
import requests
import exceptions as ex


def get_public():
    try:
        # Use a public IP address retrieval service
        response = requests.get("https://cloudflare.com/cdn-cgi/trace")

        if response.status_code == 200:
            # Parse the JSON response
            public_ip = re.search("ip=(.*)", response.text)
            return public_ip.group(1)
        else:
            msg = "Error retrieving public IP. Status code: "
            msg += response.status_code
            raise ex.PublicIPNotFound(msg)
    except Exception as e:
        msg = f"An error occurred: {e}"
        raise ex.PublicIPNotFound(msg)
