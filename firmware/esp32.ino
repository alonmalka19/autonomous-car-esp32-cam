#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Limor1";
const char* password = "0508851790";

const int gpLb = 2;   // \u05e9\u05de\u05d0\u05dc \u05d0\u05d7\u05d5\u05e8\u05d4
const int gpLf = 14;  // \u05e9\u05de\u05d0\u05dc \u05e7\u05d3\u05d9\u05de\u05d4
const int gpRb = 15;  // \u05d9\u05de\u05d9\u05df \u05d0\u05d7\u05d5\u05e8\u05d4
const int gpRf = 13;  // \u05d9\u05de\u05d9\u05df \u05e7\u05d3\u05d9\u05de\u05d4

WebServer server(80);
String lastDistance = "0";

void stopMotors() {
  digitalWrite(gpLf, LOW);
  digitalWrite(gpLb, LOW);
  digitalWrite(gpRf, LOW);
  digitalWrite(gpRb, LOW);
}

void handleForward() {
  stopMotors();
  digitalWrite(gpLf, HIGH);
  digitalWrite(gpRf, HIGH);
  server.send(200, "text/plain", "Moving forward");
}

void handleBackward() {
  stopMotors();
  digitalWrite(gpLb, HIGH);
  digitalWrite(gpRb, HIGH);
  server.send(200, "text/plain", "Moving backward");
}

void handleLeft() {
  stopMotors();
  digitalWrite(gpRf, HIGH);  // \u05d9\u05de\u05d9\u05df \u05e7\u05d3\u05d9\u05de\u05d4
  server.send(200, "text/plain", "Turning left");
}

void handleRight() {
  stopMotors();
  digitalWrite(gpLf, HIGH);  // \u05e9\u05de\u05d0\u05dc \u05e7\u05d3\u05d9\u05de\u05d4
  server.send(200, "text/plain", "Turning right");
}

void handleSpinLeft() {
  stopMotors();
  digitalWrite(gpLb, HIGH);  // \u05e9\u05de\u05d0\u05dc \u05d0\u05d7\u05d5\u05e8\u05d4
  digitalWrite(gpRf, HIGH);  // \u05d9\u05de\u05d9\u05df \u05e7\u05d3\u05d9\u05de\u05d4
  server.send(200, "text/plain", "Spinning left");
}

void handleSpinRight() {
  stopMotors();
  digitalWrite(gpLf, HIGH);  // \u05e9\u05de\u05d0\u05dc \u05e7\u05d3\u05d9\u05de\u05d4
  digitalWrite(gpRb, HIGH);  // \u05d9\u05de\u05d9\u05df \u05d0\u05d7\u05d5\u05e8\u05d4
  server.send(200, "text/plain", "Spinning right");
}

void handleStop() {
  stopMotors();
  server.send(200, "text/plain", "Stopping");
}

void handleDistance() {
  server.send(200, "text/plain", lastDistance);
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 16, 17);  // RX = GPIO16, TX = GPIO17

  pinMode(gpLb, OUTPUT);
  pinMode(gpLf, OUTPUT);
  pinMode(gpRb, OUTPUT);
  pinMode(gpRf, OUTPUT);
  stopMotors();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected. IP: ");
  Serial.println(WiFi.localIP());

  // \u05e4\u05e7\u05d5\u05d3\u05d5\u05ea \u05ea\u05e0\u05d5\u05e2\u05d4 \u05e8\u05d2\u05d9\u05dc\u05d5\u05ea
  server.on("/forward", handleForward);
  server.on("/backward", handleBackward);
  server.on("/left", handleLeft);
  server.on("/right", handleRight);
  server.on("/stop", handleStop);
  server.on("/distance", handleDistance);

  // \u05e4\u05e7\u05d5\u05d3\u05d5\u05ea \u05e1\u05d9\u05d1\u05d5\u05d1 \u05d7\u05d6\u05e7\u05d5\u05ea
  server.on("/spin_left", handleSpinLeft);
  server.on("/spin_right", handleSpinRight);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();

  // \u05e7\u05e8\u05d9\u05d0\u05d4 \u05e1\u05d3\u05d9\u05e8\u05d4 \u05de\u05d4-Arduino
  while (Serial2.available()) {
    String reading = Serial2.readStringUntil('\n');
    reading.trim();
    if (reading.length() > 0) {
      lastDistance = reading;
      Serial.println("Distance: " + lastDistance);
    }
  }
}

#define IR_LEFT 16
#define IR_RIGHT 

void setup() {
  Serial.begin(115200);
  pinMode(IR_LEFT, INPUT);
  pinMode(IR_RIGHT, INPUT);
}

void loop() {
  int left = digitalRead(IR_LEFT);
  int right = digitalRead(IR_RIGHT);

  if (left == LOW && right == LOW)
    Serial.println("\uD83D\uDEA7 \u05de\u05db\u05e9\u05d5\u05dc \u05de\u05e9\u05e0\u05d9 \u05d4\u05e6\u05d3\u05d9\u05dd");
  else if (left == LOW)
    Serial.println("\u21A9\uFE0F \u05de\u05db\u05e9\u05d5\u05dc \u05de\u05e9\u05de\u05d0\u05dc");
  else if (right == LOW)
    Serial.println("\u21AA\uFE0F \u05de\u05db\u05e9\u05d5\u05dc \u05de\u05d9\u05de\u05d9\u05df");
  else
    Serial.println("\u2714\uFE0F \u05d0\u05d9\u05df \u05de\u05db\u05e9\u05d5\u05dc\u05d9\u05dd");

  delay(300);
}
