#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
	CTFR - 04.03.18.02.10.00 - Sheila A. Berta (UnaPibaGeek)
------------------------------------------------------------------------------
"""

## # LIBRARIES # ##
import re

import requests

## # CONTEXT VARIABLES # ##
version = 1.3


## # MAIN FUNCTIONS # ##

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
    parser.add_argument('-o', '--output', type=str, help="Output file.")
    parser.add_argument('-a', '--active', action="store_true", default=False, help="Exclude expired certs")
    return parser.parse_args()


def banner():
    global version
    b = '''
          ____ _____ _____ ____  
         / ___|_   _|  ___|  _ \ 
        | |     | | | |_  | |_) |
        | |___  | | |  _| |  _ < 
         \____| |_| |_|   |_| \_\\
    
     Version {v} - Hey don't miss AXFR!
    Made by Sheila A. Berta (UnaPibaGeek)
    '''.format(v=version)
    print(b)


def clear_url(target):
    return re.sub(".*www\.", '', target, 1).split('/')[0].strip()


def save_subdomains(subdomain, output_file):
    subdomain = subdomain.replace("\\n", " | ")
    with open(output_file, "a") as f:
        f.write(subdomain + '\n')
        f.close()


def main():
    banner()
    args = parse_args()
    subdomains = []
    targeted = target = clear_url(args.domain)
    output = args.output
    if args.active:
        targeted = target + '&exclude=expired'

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=targeted))

    if req.status_code != 200:
        print("[X] Information not available!")
        exit(1)
    for (key, value) in enumerate(req.json()):
        subdomains.append(value['name_value'].replace("\n", " | "))

    subdomains = sorted(set(subdomains))
    qty = len(subdomains)
    print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))
    print("\n[!] ---- {d} certs found ---- [!] \n".format(d=qty))

    for subdomain in subdomains:
        print("[-]  {s}".format(s=subdomain))
        if output is not None:
            save_subdomains(subdomain, output)

    print("\n\n[!]  Done. Have a nice day! ;).")


main()
