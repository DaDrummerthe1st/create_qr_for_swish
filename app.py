import urllib
import os

import numpy as np
import streamlit as st
import qrcode


#"""Since the qr reader in the swish app is only a text input from a web link custom qr-codes can be built"""

st.header("Skapa QR-kod för Swish")

# initialize input data
receiver = st.text_input('Mottagare', help="Mottagare måste fyllas i") # TODO: connect to contacts locally
message = st.text_input('Meddelande', max_chars=50)
amount = st.number_input('Summa', help="Tomt fält innebär att swish-appen kommer kräva att det fylls i senare") # TODO: calculator

# to add some safety to the app
receiver = urllib.parse.quote(receiver, safe="") # safe is for include the '/' character in quoting
message = urllib.parse.quote(message, safe="")

# TODO: Add a custom picture in the middle inside qr-code

# initialize qrcode
qr = qrcode.QRCode( # TODO: fixed size no matter amount of information.
    version=1, # 1-40, if set to None qr.make(fit=True) autodetermines size
    box_size=10, # px size of each little "square", using a big number - made huge difference when reading qr
    error_correction=qrcode.constants.ERROR_CORRECT_L
)

# empty fields means its possible to fill in own information bedore running swish
# filled fields are locked in the Swish app
qr_string = (f"https://app.swish.nu/1/p/sw/?")
if receiver:
    qr_string += f'sw={receiver}'
if message:
    qr_string += f'&msg={message}'
if amount:
    qr_string += f'&amt={amount}&cur=SEK'
qr_string += "&src=qr"

qr.add_data(qr_string)
qr.make()
phone_qr = qr.make_image(fill_color="white", back_color="black")

phone_qr_as_np = np.array(phone_qr) # because otherwise I'd have to first store it locally
st.image(phone_qr_as_np)
st.write(qr_string)

# TODO: create a download_button w/o having to host-store first
# Perhaps PIL har something that could work?
# Similar to file_not_saved_to_host = PIL.makeImage(phone_qr)

# qr_img = qr.make(qr_string)
# qr_img = qr.make_image()
# phone_qr_as_np = np.array(qr_img)
phone_qr.save("filnamn.png")
with open("filnamn.png", "rb") as f:
    st.download_button("Ladda ner som .png",
                       data=f,
                       file_name=f'{receiver}.png',
                       mime='image/png')

os.remove("filnamn.png")
# Complete string:
#qr_string = "https://app.swish.nu/1/p/sw/?sw=+46023456789&amt=600&cur=SEK&msg=GRATTIS!%20Anv%C3%A4nd%20till%20typ%20massage%20eller%20n%C3%A5tt!&src=qr"
