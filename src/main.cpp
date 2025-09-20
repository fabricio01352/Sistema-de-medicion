#include <WiFi.h>
#include <PubSubClient.h>
#include "secrets.h"



const char* ssid = WIFI_SSID;         
const char* password = WIFI_PW; 
const char* mqtt_server = MQTT_SV;

WiFiClient espClient;
PubSubClient client(espClient);

const int TRIG_PIN = 5;      
const int ECHO_PIN = 18;     
const int UMBRAL_CARRO = 50; 

unsigned long lastTime = 0;
const unsigned long interval = 1800000; 

void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  Serial.println("WiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) { break; }
    delay(5000);
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

long medirDistancia() {
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracion = pulseIn(ECHO_PIN, HIGH);
  return duracion * 0.034 / 2;
}

void loop() {
  if (!client.connected()) { reconnect(); }
  client.loop();

  unsigned long currentTime = millis();
  if (currentTime - lastTime >= interval) {
    lastTime = currentTime;

    long distancia = medirDistancia();
    bool hayCarro = distancia < UMBRAL_CARRO;

    if(hayCarro){
      char msg[10];
      sprintf(msg, "%d", hayCarro);
      client.publish("sensores/hayCarro", msg);
      Serial.print("Publicado -> Hay carro: ");
      Serial.println(hayCarro);
    }

    Serial.print("Distancia: ");
    Serial.print(distancia);
    Serial.print(" cm -> Hay carro: ");
    Serial.println(hayCarro);
  }
}
