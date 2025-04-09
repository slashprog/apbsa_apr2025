from gevent import monkey; monkey.patch_all()

from time import sleep, time
from concurrent.futures import ThreadPoolExecutor as Executor

def fetch_web_page(url):
    from urllib.request import urlopen
    try:
        print(f"Fetching {url}...")
        response = urlopen(url)
        print(f"Fetched {url}.")
    except HTTPError as e:
        return str(e)
    else:
        return str(response.code)
 

urls = [
    "http://www.chandrashekar.info/",
    "http://cisco.com/",
    "http://www.python.org/",
    "https://www.dhrona.net/",
    "http://www.kernel.org/",
    "http://www.debian.org/",
    "https://www.moonranger.net/"
]

if __name__ == '__main__':
    start = time()
    #result = [ fetch_web_page(x) for x in urls ]
    result = list(map(fetch_web_page, urls))
    duration = time() - start
    print(f"duration = {duration}")
    print(f"result = {result}")
    print("-" * 40)

    start = time()
    with Executor(max_workers=10) as workers:
        result = list(workers.map(fetch_web_page, urls))
    duration = time() - start
    print(f"duration = {duration}")
    print(f"result = {result}")
