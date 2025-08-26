from django.apps import apps


def get_geolocation(ip_address):
    """
    Get the geolocation (country and city) for a given IP address
    """

    ClickifyConfig = apps.get_app_config('clickify')

    if not ClickifyConfig.geoip_reader or not ip_address:
        return None, None

    try:
        response = ClickifyConfig.geoip_reader.city(ip_address)
        return response.country.name, response.city.name
    except Exception:
        return None, None
