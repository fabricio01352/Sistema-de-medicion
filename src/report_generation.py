import sqlite3
import pandas as pd
from datetime import date
from github import Github, Auth
import datetime
import schedule
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os

def subir_a_github_api(file_path, repo_full_name, branch="main"):
    token = os.getenv("GITHUB_TOKEN")
    g = Github(auth=Auth.Token(token))
    repo = g.get_repo(repo_full_name)
    
    with open(file_path, "rb") as file:
        content = file.read()
        
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Reporte generado {fecha}"
    file_name = file_path.split("/")[-1]
    
    try:
        try:
            existing_file = repo.get_contents(file_name, ref=branch)
            repo.update_file(existing_file.path, message, content, existing_file.sha, branch=branch)
            print(" Reporte actualizado en GitHub")
        except:
            repo.create_file(file_name, message, content, branch=branch)
            print(" Reporte creado en GitHub")
    except Exception as e:
        print(f" Error al subir con API: {e}")

def generar_y_subir_reporte():
    conn = sqlite3.connect('car_location_db.db')

    today = date.today()
    query = f"""
    SELECT COUNT(*) AS "total de carros"
    FROM lecturas
    WHERE DATE(timestamp) = '{today}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    file_name = f"reporte_{today}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica",14)
    c.drawString(100,750, f"Reporte diario - {today}")
    
    total = df.iloc[0,0]
    c.setFont("Helvetica",12)
    c.drawString(100,700, f"Total de carros: {total}")
    
    c.save()
    
    # file_name = f"reporte_{today}.xlsx"
    # df.to_excel(file_name, index=False)
    # print(f" Reporte generado: {file_name}")

    subir_a_github_api(file_name, os.getenv("REPO_NAME"))

schedule.every().day.at("21:50").do(generar_y_subir_reporte)
print(" Scheduler iniciado, el reporte se enviará a las 18:00 todos los días.")

while True:
    schedule.run_pending()
    time.sleep(30) 
