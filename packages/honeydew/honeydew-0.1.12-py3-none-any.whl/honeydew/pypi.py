import requests
import json

# Get the latest version of pypi package from pypi.org
def get_latest_pypi_version(package_name):
    import requests
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.status_code == 200:
        return response.json()['info']['version']
    else:
        return None