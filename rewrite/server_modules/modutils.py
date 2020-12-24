from http.client import HTTPSConnection


def obtain_reachable_ip_address(iprtvers):
    urlh = "api64.ipify.org"
    if iprtvers == 4:
        urlh = "api.ipify.org"
    elif iprtvers == 6:
        urlh = "api6.ipify.org"
    try:
        connobjc = HTTPSConnection(urlh)
        connobjc.request("GET", "/")
        response = connobjc.getresponse()
        return response.read().decode("UTF-8")
    except:
        return "Error getting IP address."
