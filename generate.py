import pickle
from pathlib import path

import streamlit_authenticator as stauth

names = [ "Arrene", "Placement"]
usernames = ["admin","placement"]
password = ["1234", "aaa123"]

hashed_passwords = stauth.Hasher(password).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open ("wb") as file:
    pickle.dump(hashed_passwords, file)