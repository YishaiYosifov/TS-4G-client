import socket
import json
import os
import re

HOSTS_FILE = "C:\Windows\System32\drivers\etc\hosts"
GET_HOST_URL_REGEX = re.compile(r"\n# TS-4G-START\n([\S\s]*)\n# TS-4G-END")

with open("config.json", "r") as f: CONFIG = json.load(f)

def send(s : socket.socket, data : dict): s.send(json.dumps(data).encode("utf-8"))

def get_blocked_urls(remove : bool = False) -> list:
    with open(HOSTS_FILE, "r") as f: hosts = f.read()

    hostsBlocks = re.search(GET_HOST_URL_REGEX, hosts)
    if not hostsBlocks:
        if not remove:
            hosts += "\n# TS-4G-START\n\n# TS-4G-END"
            with open(HOSTS_FILE, "w") as f: f.write(hosts)

        return []
    hostsBlocks = hostsBlocks.group(1)

    if remove:
        hosts = re.sub(GET_HOST_URL_REGEX, "", hosts)
        with open(HOSTS_FILE, "w") as f: f.write(hosts)

    blockedURLs = []
    for block in hostsBlocks.split("\n"):
        urls = block.split()
        if len(urls) > 1: blockedURLs.append(urls[1])
    return blockedURLs

def update_hosts(urls : list):
    with open(HOSTS_FILE, "r") as f: hosts = f.read()
    hosts = re.sub(GET_HOST_URL_REGEX, "", hosts)
    
    urls = "\n".join([f"0.0.0.0 {url}" for url in urls])
    hosts += f"\n# TS-4G-START\n{urls}\n# TS-4G-END"
    with open(HOSTS_FILE, "w") as f: f.write(hosts)

    os.system("ipconfig /flushdns")
