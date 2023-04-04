import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['qwerty', 'abcdef']).generate()

print(hashed_passwords)