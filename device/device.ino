/* 
 * Bookbox notification device code
 * Created 2018-04-17
 * For deepsleep to work properly we need to connect gpio16 to rst
 */

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#define USE_SERIAL Serial

ESP8266WiFiMulti WiFiMulti;

void setup() {
    USE_SERIAL.begin(115200);

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();

    for(uint8_t t = 4; t > 0; t--) {
        USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
        USE_SERIAL.flush();
        delay(1000);
    }

    WiFi.mode(WIFI_STA);
    WiFiMulti.addAP("JOKERNET", "password");

}

void loop() {
    // wait for WiFi connection
    while(WiFiMulti.run() != WL_CONNECTED) {
      delay(2);
    }

    HTTPClient http;

    USE_SERIAL.print("[HTTP] begin...\n");
    http.begin("http://192.168.0.100ä:5000/"); //Server address
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpCode = http.POST("level=40"); //TODO: Add actual value here

    // httpCode will be negative on error
    if(httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        USE_SERIAL.printf("[HTTP] POST... code: %d\n", httpCode);

        // file found at server
        if(httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            USE_SERIAL.println(payload);
        }
    } else {
        USE_SERIAL.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
    USE_SERIAL.println("going into hibernation");
    ESP.deepSleep(1000*1000*5); //sleep for 5 seconds TODO: Change this to 1 hour when deploying
}

