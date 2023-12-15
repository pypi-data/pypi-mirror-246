import requests

from axya_whisper.constants import AXYA_API_TOKEN, AXYA_API_URL, VERIFY_SSL
from axya_whisper.models import GeniusERPConfigurationResponse


def get_axya_config() -> GeniusERPConfigurationResponse: 
    headers = {
        "Authorization": f"Token {AXYA_API_TOKEN}",
    }
    
    response = requests.get(f"{AXYA_API_URL}/genius/configuration", headers=headers, verify=VERIFY_SSL)

    if response.status_code == 200:
        return GeniusERPConfigurationResponse(response.json())
    else:
        # Notify AXYA
        pass