from dotenv import load_dotenv
import os

import RPi.GPIO as GPIO
import time
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart




load_dotenv()


print("hello world")

EMAIL_SEND = os.getenv('EMAIL_SEND')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_RECIV = os.getenv('EMAIL_RECIV')


def send_emain_jpg(fotka):
	# Dane do logowania
	nadawca_email = EMAIL_SEND
	haslo = EMAIL_PASS
	odbiorca_email = EMAIL_RECIV

	# Tworzenie wiadomości
	wiadomosc = MIMEMultipart()
	wiadomosc['From'] = nadawca_email
	wiadomosc['To'] = odbiorca_email
	wiadomosc['Subject'] = "Test email ze zdjęciem"

	# Dodanie tekstu
	tekst = MIMEText("Oto wiadomość ze zdjęciem")
	wiadomosc.attach(tekst)

	# Dodanie zdjęcia
	with open(f'{fotka}.jpg', 'rb') as f:
		img_data = f.read()
		image = MIMEImage(img_data, name=f'photos/{fotka}.jpg')
		wiadomosc.attach(image)

	# Inicjalizacja zmiennej serwer
	serwer = None

	try:
		serwer = smtplib.SMTP('smtp.gmail.com', 587)
		serwer.starttls()
		serwer.login(nadawca_email, haslo)

		# Wysłanie emaila
		serwer.send_message(wiadomosc)
		print("Email ze zdjęciem został wysłany!")

	except Exception as e:
		print(f"Wystąpił błąd: {e}")

	finally:
		if serwer:
			serwer.quit()
			

def main_loop():
   	print("PROGRAM START")

    while True:
        time.sleep(1)
        input_state =  GPIO.input(4)

        

        # jeżeli ruch to zrób fotke i wyslij 
        if input_state == GPIO.HIGH:
            print("WYKRYTO RUCH")
            print("ROBIE FOTKE")
            datatime_now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            cmd = f"libcamera-jpeg -o photos\{datatime_now}.jpg"
            os.system(cmd)
			
            send_emain_jpg(datatime_now)


        # jeżeli brak ruchu to nic nie rób

        else:
            print("NOTHING HEPPENDS")