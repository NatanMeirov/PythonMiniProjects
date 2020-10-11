# Imports
import sys
import hashlib
try:
    import requests
except ImportError:
    print("Please make sure to install requests library first: use 'pip install requests' command")
    sys.exit()


# Consts
API_URL = "https://api.pwnedpasswords.com/range/"


# Functions
def get_hashed_password_header_and_trailer(password):
    hashed_password = hashlib.sha1(password.encode("UTF-8")).hexdigest().upper()
    header, trailer = hashed_password[:5], hashed_password[5:]
    return header, trailer


def request_api_data(hashed_query_characters):
    url = API_URL  + hashed_query_characters
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Runtime Error has occurred - Wrong Status Code: {response.status_code}")
    return response


def get_password_leaks_count(all_hashes, hash_to_check):
    hashes = [tuple(line.split(":")) for line in all_hashes.splitlines()]
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


# Main
def secured_password_checker_engine():
    # Validations
    try:
        if len(sys.argv) < 2:
            raise IOError(f"Arguments Error - not enough arguments:\n{sys.argv[0]} [Password 1 to check] ... (More are optional)")

    except IOError as e:
        print(e)
        sys.exit()


    # Processing
    passwords_to_check = sys.argv[1:]

    for password in passwords_to_check:
        hashed_password_header, hashed_password_trailer = get_hashed_password_header_and_trailer(password)
        api_response = request_api_data(hashed_password_header) # The returned api_response.text would be a list of all trailers of hashed password (for security reasons)
        times_leaked = get_password_leaks_count(api_response.text, hashed_password_trailer)
        if times_leaked:
            print(f"[-] {password} was leaked {times_leaked} times...")
        else:
            print(f"[+] {password} is secured and did not leaked!")


if __name__ == "__main__":
    secured_password_checker_engine()