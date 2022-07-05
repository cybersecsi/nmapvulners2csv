#!/usr/bin/env python3

import traceback
import csv
import fire
import requests
from xml.etree import ElementTree
from time import sleep
from bs4 import BeautifulSoup
from os import path, makedirs

VERSION = '1.0.1'
OUTPUT_DIR = "nmapvulners2csv_output" # Default value, can be changed with the '--dir' optional flag
CSV_HEADERS = ['host', 'port', 'protocol', 'service', 'version','cpe', 'id_vuln', 'cvss', 'type', 'exploit', 'url', 'description']
VULNERS_URL= "https://vulners.com/"

vulners_base = lambda t: "{}{}".format(VULNERS_URL, t)
vulners_endpoint = lambda t,id: "{}/{}".format(vulners_base(t), id)

def banner():
  print(
      '''
        ███████╗███████╗ ██████╗███████╗██╗
        ██╔════╝██╔════╝██╔════╝██╔════╝██║
        ███████╗█████╗  ██║     ███████╗██║
        ╚════██║██╔══╝  ██║     ╚════██║██║
        ███████║███████╗╚██████╗███████║██║
        ╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝

        https://wwww.secsi.io - https://github.com/cybersecsi/nmapvulners2csv
      ''')  

def info(msg):
    print("[+] {}".format(msg))

def err(msg):
    traceback.print_exc()
    print("[-] ERR:{}".format(msg))

def download_descr(type, id):
    ve = vulners_endpoint(type, id)
    ret = requests.get(ve)
    return ret.text

def obtain_descr(text):
    html = "".join(text)
    soup = BeautifulSoup(html, 'html.parser')
    meta_descr = soup.select('meta[property="og:description"]')[0]
    return meta_descr['content']

def is_open(p):
    state = p.find("state")
    return state.attrib['state'] == "open"

def get_cpe(p):
    return p.find("service").find("cpe").text if p.find("service") is not None and p.find("service").find("cpe") is not None else ""

def get_vulns(p):
    script = p.find("script[@id='vulners']")
    if script is None:
        return []
    else:
        t = script.find("table")
        vulns = []
        tables = t.findall('table')
        for t in tables:
            vuln = { 'id': t.find("elem[@key='id']").text,
                'cvss': t.find("elem[@key='cvss']").text,
                'exploit': t.find("elem[@key='is_exploit']").text,
                'type': t.find("elem[@key='type']").text,
            }
            vuln['url'] = vulners_endpoint(vuln['type'], vuln['id'])
            vulns.append(vuln)
        return vulns

def check_or_create_dir(dir_path):
    exists = path.exists(dir_path)

    if not exists:
        # Create a new directory because it does not exist 
        makedirs(dir_path)
        info(f"Directory {dir_path} created")

def get(host, descr=False):
    ports = host.findall('ports//port')

    open_ports = [p for p in ports if is_open(p)]
    evidences = []

    for p in open_ports:
        vulns = get_vulns(p)
        cpe = get_cpe(p)

        try:
            service = p.find("service").attrib['name']
        except Exception as e:
            service = ""

        try:
            product = p.find("service").attrib['product']
        except Exception as e:
            product = ""

        try:
            version = p.find("service").attrib['version']
        except Exception as e:
            version = ""

        #CSV_HEADERS = ['host', 'port', 'service','cpe', 'cvss', 'id_vuln', 'type', 'exploit']
        if not vulns:
            evidence = {
                'host': host.find("address").attrib['addr'],
                'port': p.attrib['portid'],
                'protocol': p.attrib['protocol'],
                'service': service,
                'version': product + version,
                'cpe': "",
                'id_vuln':  "",
                'cvss' : "",
                'type' : "",
                'exploit' : "",
                'url':  "",
                'description': ""
            }
            evidences.append(evidence)
        for v in vulns:
            # To avoid Vulners block
            # TODO: resend logic
            if descr:
                sleep(0.2)

            #CSV_HEADERS = ['host', 'port', 'service','cpe', 'cvss', 'id_vuln', 'type', 'exploit']
            info("get {}".format(v['id']))
            evidence = {
                'host': host.find("address").attrib['addr'],
                'port': p.attrib['portid'],
                'protocol': p.attrib['protocol'],
                'service': service,
                'version': product + " " + version,
                'cpe': cpe,
                'id_vuln':  v['id'],
                'cvss' : v['cvss'],
                'type' : v['type'],
                'exploit' : v['exploit'],
                'url':  v['url'],
                'description': obtain_descr(download_descr(v['type'], v['id'])) if descr else ""
            }
            evidences.append(evidence)
    return evidences, open_ports

def process(nmap_xml_file, output_dir = OUTPUT_DIR, output = 'output.csv', descr = False):
    """
    Convert a xml nmap output file in csv file
    Example usage:
    --get_descr
    """
    if descr:
        info("Description enabled: send requests to obtain vunerability descriptoins")
    
    info(f"Opening XML file {nmap_xml_file}")
    document = ElementTree.parse(nmap_xml_file)
    info("Obtaining hosts...")
    hosts = document.findall('host')
    info("Found hosts: {}".format(len(hosts)))

    all_evidences = []

    for sh in hosts:
        evidences, all_ports = get(sh, descr)
        all_evidences = all_evidences + evidences

    check_or_create_dir(output_dir)

    with open(path.join(output_dir, output),  'w', encoding='utf-8', newline='') as csvfile:
        info(f"Store evidences in {path.join(output_dir, output)}")
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(all_evidences)
    pass

def main():
    try:
        banner()
        fire.Fire(process)
    except Exception as e:
        err(str(e))

if __name__ == '__main__':
    main()