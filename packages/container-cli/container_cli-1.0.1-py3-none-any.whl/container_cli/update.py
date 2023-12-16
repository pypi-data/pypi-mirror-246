import requests
def get_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    return None
# 调用示例
package_name = "numpy"
latest_version = get_latest_version(package_name)
if latest_version:
    print(f"最新版本的 {package_name} 是 {latest_version}")
else:
    print(f"无法获取 {package_name} 的最新版本信息")






import pkg_resources

def get_package_version(package_name):
    try:
        version = pkg_resources.get_distribution(package_name).version
        return version
    except pkg_resources.DistributionNotFound:
        return None

# 调用示例
package_name = "numpy"
current_version = get_package_version(package_name)
if current_version:
    print(f"{package_name} 的当前版本号是 {current_version}")
else:
    print(f"无法获取 {package_name} 的版本号")