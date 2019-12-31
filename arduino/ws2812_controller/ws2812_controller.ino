#include <Arduino.h>
#include <ArduinoOTA.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266mDNS.h>
#include <WiFiManager.h>

#define FASTLED_ESP8266_DMA // better control for ESP8266 will output or RX pin requires fork https://github.com/coryking/FastLED
#include "FastLED.h"

const char* sensor_name = "wrl_1";
const char* ota_password = "egziifxn";

//#define STATIC_IP

#ifdef STATIC_IP
IPAddress ip(192, 168, 1, 112);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
#endif //STATIC_IP

const int udp_port = 7778;

/*********************************** FastLED Defintions ********************************/
#define NUM_LEDS      300
#define DATA_PIN      5
//#define CLOCK_PIN   2
#define CHIPSET       WS2812B
#define COLOR_ORDER   GRB

/*********************************** Globals *******************************************/
WiFiUDP port;
CRGB leds[NUM_LEDS];

/********************************** Start Setup ****************************************/
void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println("\nStart!");

  // Setup FastLED
#ifdef CLOCK_PIN
  FastLED.addLeds<CHIPSET, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS);
#else
  FastLED.addLeds<CHIPSET, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);
#endif
  for (int i = 0; i < NUM_LEDS; i += 2) leds[i] = CRGB::Red;
  FastLED.show();

  WiFiManager wm;
  wm.autoConnect(sensor_name);

  uint8_t hue = 0;
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(hue++, 255, 255);
    FastLED.show();
    fadeall();
    delay(1);
  }

  for (int i = 0; i < NUM_LEDS; i++) {
    FastLED.show();
    fadeall();
    delay(1);
  }

  MDNS.begin(sensor_name);

  setup_ota();
  port.begin(udp_port);
}

void setup_ota() {
  ArduinoOTA.setHostname(sensor_name);
  ArduinoOTA.setPassword(ota_password);

  ArduinoOTA.onStart([]() {
    Serial.println("Starting");
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();

  // TODO: Hookup either a more elaborate protocol, or a secondary
  // communication channel (i.e. mqtt) for functional control. This
  // will also give the ability to have some non-reative effects to
  // be driven completely locally making them less glitchy.

  // Handle UDP data
  int packetSize = port.parsePacket();
  if (packetSize == sizeof(leds)) {
    port.read((char*)leds, sizeof(leds));
    FastLED.show();
  } else if (packetSize) {
    Serial.printf("Invalid packet size: %u (expected %u)\n", packetSize, sizeof(leds));
    port.flush();
    return;
  }
}

void fadeall() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i].nscale8(250);
  }
}
