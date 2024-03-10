import requests

def send_http_request(url, verify=False, timeout=5, headers=None, proxy=None):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, verify=verify, timeout=timeout, proxies=proxies)
        return response
    except requests.exceptions.Timeout:
        return -1
    except requests.exceptions.RequestException:
        return None

