import requests
from django.conf import settings

def get_geolocation(ip_address):
    """
    Get the geolocation (country and city) for a given IP address using an API.
    Geolacation is enabled by default. It can be disabled by setting
    CLICKIFY_GEOLOCATION = False in the project's settings
    """

    # Check if geolocation is enabled in settings
    if not getattr(settings, 'CLICKIFY_GEOLOCATION', True):
        return None, None
    
    if not ip_address:
        return None, None
    
    # Avoid making API calls for local/private IP addresses
    if ip_address == '127.0.0.1' or ip_address.startswith(('10.', '172.', '192.168.')):
        return 'Local', 'Local'
    
    try:
        # The API endpoint. We request only the fields we need
        url = f"http://ip-api.com/json/{ip_address}?fields=status,country,city"
        
        response = requests.get(url, timeout=2)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            return data.get('country'), data.get('city')
        else:
            return None, None
    except (requests.RequestException, ValueError):
        # Catch network errors, timeouts, or JSON decoding errors
        return None, None 