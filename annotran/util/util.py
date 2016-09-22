import re
import urllib


def strip_logout(url):
    """
    Removes the in-built hypothes.is-appended &__formid__=logout from a URL
    :param url: the URL
    :return: a clean URL
    """
    try:
        url = re.sub('&__formid__=logout$', '', url).split("#")[0]
    except IndexError:
        url = ''
    return url


def get_url_from_request(request):
    """
    Extracts a URL from a request and removes the in-built hypothes.is-appended &__formid__=login
    :param request: the request
    :return: a clean URL
    """
    try:
        url = urllib.unquote(
            urllib.unquote(request.url.split('?')[1].replace('url=', '')).split('?')[1].replace('url=', ''))
        url = re.sub('&__formid__=login$', '', url).split("#")[0]
    except IndexError:
        url = ''
    return url
