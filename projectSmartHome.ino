#include <WiFi.h>
#include <ESP32Servo.h>
#include <ESPmDNS.h>

const char* ssid = "SHHACC";
const char* password = "1234567890";

WiFiServer server(5000);

Servo servo;

void setup() {

  Serial.begin(115200);

  servo.attach(13);

  Serial.println();
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected!");

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // START MDNS
  if (MDNS.begin("esp32")) {

    Serial.println("mDNS started");
    Serial.println("Hostname: esp32.local");
  }

  server.begin();

  Serial.println("TCP server started");
}

void loop() {

  WiFiClient client = server.available();

  if (client) {

    Serial.println("Client connected");

    while (client.connected()) {

      if (client.available()) {

        String cmd = client.readStringUntil('\n');

        cmd.trim();

        Serial.print("Received: ");
        Serial.println(cmd);

        if (cmd == "ON") {

          servo.write(90);

          Serial.println("Servo ON");

        } else if (cmd == "OFF") {

          servo.write(0);

          Serial.println("Servo OFF");
        }
      }
    }

    client.stop();

    Serial.println("Client disconnected");
  }
}