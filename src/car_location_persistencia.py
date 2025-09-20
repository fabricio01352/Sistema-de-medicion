import sqlite3
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

conn = sqlite3.connect(os.getenv("DB_NAME"))
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS lecturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        hay_carro INTEGER
        
    )
          
''')

conn.commit()

broker = "broker.hivemq.com"
topic = "sensores/hayCarro"

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con codigo ",rc)
    client.subscribe(topic)
    
def on_message(client,userdata, msg):
    # distancia = int(msg.payload.decode())
    hay_carro = int(msg.payload.decode())
    # print(f"Recibido: {distancia} cm")
    
    # c.execute("INSERT INTO lecturas (distancia_cm) VALUES (?)", (distancia,))
    c.execute("INSERT INTO lecturas (hay_carro) VALUES (?)", (hay_carro,))
    conn.commit()
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_forever()
    