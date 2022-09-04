import requests
import hashlib
import streamlit as st
from load_css import local_css


# ------------------------------- FRONT END USING STREAMLIT -----------------------------

st.set_page_config(page_title='Password Security Checker', page_icon="🔒")

local_css("style.css")

#hiding the hamburger menu and footer
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.title("Password Security Checker")
st.write("### Enter your password to check whether it has been Leaked or Not!")
st.write(" ")
password = st.text_input("PASSWORD :", "")

# ------------------------------------------------------------------------------------------


def request_api_data(query_char):  # First 5 symbols of hashed password , a string
    # k Anonimity is used here no need to give complete password to url
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f'Error fetching : {resp.status_code}, Check the API and TRY AGAIN!')
    else:
        return resp


def get_password_leak_count(hashes, hash_of_my_psswd):  # Hashes are all the hash forms returned which matched the first 5 symbols
    hashes = (line.split(':') for line in hashes.text.splitlines())  # Use splitlines to convert one single big string of text into list of lines
    for h, number in hashes:
        if h == hash_of_my_psswd:
            return number


# The below function converts our original password into hashed form using sha1 hash function, by using hashlib module

def pwned_api_check(password):  # Give original password
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_symbols, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_symbols)  # the response gives the hashform excluding the first 5 symbols

    return get_password_leak_count(response, tail)



def check():
        count = pwned_api_check(password)

        if count:  # if count is None , then false so goes to else statement
            # st.header(f'Your Password FOUND {count} number of times ⚠️')
            # st.write('## You should CHANGE YOUR PASSWORD FOR SECURITY!')
            ans = f"<div>Your Password <span class='highlight red'><span class='bold'> FOUND {count} number of times ⚠️</span> </span><p></p><p>You should CHANGE YOUR PASSWORD FOR SECURITY!</p></div>"
            st.markdown(ans, unsafe_allow_html=True)

        else:
            ans = "<div>Your Password <span class='highlight blue'><span class='bold'>NOT FOUND 😌</span> </span><p></p><p>You can continue using same password.</p></div>"
            st.markdown(ans, unsafe_allow_html=True)










if __name__ == '__main__':
    # Means this file will run if it is the main file being run and not if it is imported
    if st.button("SUBMIT"):
        check()

    css_icon = '''                                                                                                                                                       
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    

    <i class="fa-solid fa-lock"></i>  Entries are 100% secure.                                                                                                                                                                        

    '''

    st.write(" ")
    st.write(" ")
    st.write(css_icon, unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write("### Made by Poulamee Pal with ❤️")
