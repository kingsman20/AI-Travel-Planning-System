import ipaddress

import requests


def _is_public_ip(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_global
    except ValueError:
        return False


def city_from_ip(ip: str | None) -> str:
    if not ip or not _is_public_ip(ip):
        return ""
    try:
        response = requests.get(
            f"http://ip-api.com/json/{ip}",
            params={"fields": "status,city,country"},
            timeout=3,
        )
        data = response.json()
    except (requests.RequestException, ValueError):
        return ""
    if data.get("status") != "success" or not data.get("city"):
        return ""
    if data.get("country"):
        return f"{data['city']}, {data['country']}"
    return data["city"]


def city_from_timezone(timezone_name: str | None) -> str:
    if not timezone_name or "/" not in timezone_name:
        return ""
    return timezone_name.split("/")[-1].replace("_", " ")


def detect_starting_city(ip: str | None = None, timezone_name: str | None = None):
    """Return (city_label, source_label). source_label is empty if undetected."""
    city = city_from_ip(ip)
    if city:
        return city, "Detected from your connection"
    city = city_from_timezone(timezone_name)
    if city:
        return city, "Guessed from your timezone"
    return "", ""
