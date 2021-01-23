import requests
import hashlib
import sys  

def request_api_data(query_char):  # First 5 symbols of hashed password , a string
    # k Anonimity is used here no need to give complete password to url
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    resp =  requests.get(url)
    if resp.status_code != 200: 
        raise RuntimeError(f'Error fetching : {resp.status_code}, Check the API and TRY AGAIN!')
    else:
         return resp


def get_password_leak_count(hashes ,hash_of_my_psswd): # Hashes are all the hash forms returned which matched the first 5 symbols
    hashes = (line.split(':') for line in hashes.text.splitlines()) # Use splitlines to convert one single big string of text into list of lines
    for h,number in hashes:
        if h == hash_of_my_psswd:
            return number
        
    
# The below function converts our original password into hashed form using sha1 hash function, by using hashlib module

def pwned_api_check(password): # Give original password
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_symbols , tail = sha1password[:5] , sha1password[5:]
    response = request_api_data(first5_symbols) # the response gives the hashform excluding the first 5 symbols

    return get_password_leak_count(response , tail) 

def main(args):
    for password in args: # we can check any number of passwords together
        count = pwned_api_check(password)
        
        if count: # if count is None , then false so goes to else statement
            print(f'{password} FOUND {count} number of times. You should CHANGE THE PASSWORD FOR SECURITY!')
        else:
            print(f'{password} NOT FOUND. You can continue using same password')
    return ("DONE ! ")
if __name__=='__main__': # Means this file will run if it is the main file being run and not if it is imported
    sys.exit(main(sys.argv[1:]))