#include <Arduino.h>

#include <WiFi.h>
#include <HTTPClient.h>

#define DEBUG true

const char *ssid = "tv licensing van #269";
const char *password = "jamesissilly";

const char *serverName = "http://192.168.3.22:6969/";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
// unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;

struct capSensor
{
  int pin;
  unsigned long firstTriggered;
  bool triggered;
};

capSensor capSensors[4] = {
    {32, 0, false},
    {33, 0, false},
    {0, 0, false},
    {2, 0, false}};

void sendPost(int pin)
{
  if (DEBUG)
    Serial.printf("Sending POST request to %d, Current Reading: %d, First Reading: %dms ago\t", pin, touchRead(pin), millis() - capSensors[pin].firstTriggered);
  if (WiFi.status() == WL_CONNECTED)
  {
    WiFiClient client;
    HTTPClient http;
    http.begin(client, serverName);
    // http.addHeader("Content-Type", "application/json");
    String payload;
    switch (pin)
    {
    case 0:
      payload = "x+"; // right
      break;
    case 33:
      payload = "x-"; // left
      break;
    case 2:
      payload = "y+"; // up
      break;
    case 32:
      payload = "y-"; // down
      break;
    default:
      if (DEBUG)
        Serial.printf("Pin %d not found\t", pin);
      break;
    }
    int httpResponseCode = http.POST(payload);
    if (DEBUG)
      Serial.printf("HTTP Response code: %d\n", httpResponseCode);
    http.end();
  }
  else
  {
    if (DEBUG)
      Serial.println("WiFi Disconnected :(");
  }
}

void setup()
{
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop()
{
  for (int i = 0; i < 4; i++)
  {
    if (touchRead(capSensors[i].pin) < 30)
    {
      if (!capSensors[i].triggered)
      {
        capSensors[i].triggered = true;
        capSensors[i].firstTriggered = millis();
      }
    }
    else
    {
      capSensors[i].triggered = false;
      capSensors[i].firstTriggered = 0;
    }
  }

  capSensor lastTriggered = capSensors[0];

  for (int i = 0; i < 4; i++)
  {
    if (capSensors[i].triggered)
    {
      if (lastTriggered.firstTriggered < capSensors[i].firstTriggered)
      {
        lastTriggered = capSensors[i];
      }
    }
  }

  if (lastTriggered.triggered && millis() - lastTriggered.firstTriggered > 200)
  {
    sendPost(lastTriggered.pin);
  }
}
