from common.util import get_blocked_urls, update_hosts

def block_url(url : str):
    urls = get_blocked_urls()
    urls += [url, "www." + url]

    update_hosts(urls)

def unblock_url(url : str):
    urls = get_blocked_urls()
    urls.remove(url)
    urls.remove("www." + url)

    update_hosts(urls)
