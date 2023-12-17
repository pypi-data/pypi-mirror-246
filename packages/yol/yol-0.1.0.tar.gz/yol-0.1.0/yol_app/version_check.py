import requests
import pkg_resources
from datetime import datetime

def get_current_version():
    package_name = __package__
    try:
        current_version = pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        current_version = None  # Handle the case where package is not found

    # Assuming you have a way to store or retrieve the release date
    current_version_date = datetime(2023, 1, 1)  # Replace with actual logic to get release date

    return package_name, current_version, current_version_date

def get_latest_version_from_pypi(package_name):
    try:
        response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
        if response.status_code == 200:
            data = response.json()
            return data['info']['version']
    except requests.RequestException:
        return None

def check_for_update():
    package_name, current_version, current_version_date = get_current_version()
    if not current_version:
        return "Unable to determine current version"

    latest_version = get_latest_version_from_pypi(package_name)
    if latest_version and latest_version != current_version:
        return latest_version
    else:
        if datetime.now() > current_version_date.replace(year=current_version_date.year + 1):
            return 'version check failed, consider updating'
    return None

# Use this function to trigger the version check
update_version = check_for_update()
