import urllib
import re

def get_url_from_request(request):
    try:
        url = urllib.unquote(urllib.unquote(request.url.split('?')[1].replace('url=', '')).split('?')[1].replace('url=', ''))
        url = re.sub('\&__formid__=login$', '', url)
    except:
        url = ''
    return url