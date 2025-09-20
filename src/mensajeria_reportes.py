from twilio.rest import Client
import requests
from github import Github, Auth
import re
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")
client = Client(account_sid, auth_token)

from_whatsapp = os.getenv("NUMBER_FROM")   
to_whatsapp = os.getenv("NUMBER_TO")     


# configuramos gitub api
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("REPO_NAME")
g = Github(auth=Auth.Token(token))
repo = g.get_repo(repo_name)

all_files = repo.get_contents("")
pattern = re.compile(r"reporte_\d{4}-\d{2}-\d{2}\.pdf")

report_files = [f for f in all_files if pattern.match(f.name)]
report_files.sort(key=lambda f: f.name, reverse=True)

if not report_files:
    raise Exception("No se encontraron archivos de reporte en el repositorio")

latest_file = report_files[0]
file_url = latest_file.download_url

print(f"archivo mas reciente: {latest_file.name}")


# file_url = "https://raw.githubusercontent.com/Fabricio1352/pdffile_test/main/report.pdf"

def enviarmensaje():
    
    message = client.messages.create(
        from_=from_whatsapp,
        body="Reporte diario de entradas de carros",
        to=to_whatsapp,
        media_url=[file_url]
    )

print("Mensaje enviado, SID:")



schedule.every().day.at("22:00").do(enviarmensaje)
print(" Scheduler iniciado, el reporte se enviará a 6442590010 las 18:10 todos los días.")

while True:
    schedule.run_pending()
    time.sleep(30) 