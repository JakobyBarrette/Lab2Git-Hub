#include "esp_camera.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <SD_MMC.h>

// WiFi credentials
const char* ssid = "MSIJakoby";
const char* password = "88888888";

// MQTT Broker details
const char* mqtt_server = "192.168.137.1";
const int mqtt_port = 1883;

// MQTT Topics
const char* command_topic = "esp32/cam/command"; // Topic to listen for capture commands
const char* image_topic = "esp32/cam/image";     // Topic to publish captured images

WiFiClient espClient;
PubSubClient client(espClient);

void setup_camera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1; // -1 = not used
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // Adjust frame size and quality
  config.frame_size = FRAMESIZE_UXGA;
  config.jpeg_quality = 10;
  config.fb_count = 2;

  // Initialize the camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  // Convert payload to string
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Check if this is the command topic and message is "capture"
  if (String(topic) == command_topic && message == "capture") {
    captureAndSendPhoto();
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32CAMClient")) {
      Serial.println("connected");
      // Subscribe to command topic
      client.subscribe(command_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup_sd() {
  Serial.println("Initializing SD card...");
  if (!SD_MMC.begin()) {
    Serial.println("SD Card Mount Failed");
    return;
  }
  uint8_t cardType = SD_MMC.cardType();
  if (cardType == CARD_NONE) {
    Serial.println("No SD Card attached");
    return;
  }
  Serial.println("SD Card initialized.");
}

void captureAndSendPhoto() {
  Serial.println("Capturing photo...");
  
  // Take picture
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  
  // Save to SD card
  String path = "/photo_" + String(millis()) + ".jpg";
  fs::FS &fs = SD_MMC;
  
  File file = fs.open(path.c_str(), FILE_WRITE);
  if(!file){
    Serial.println("Failed to open file in writing mode");
  } else {
    file.write(fb->buf, fb->len);
    Serial.printf("Saved file to path: %s\n", path.c_str());
    file.close();
  }
  
  // Publish to MQTT
  if (fb->len > 0) {
    Serial.print("Publishing image to MQTT, size: ");
    Serial.print(fb->len);
    Serial.println(" bytes");
    
    // Publish in chunks if needed (MQTT has max packet size)
    const int chunkSize = 1024;
    for (size_t i = 0; i < fb->len; i += chunkSize) {
      size_t remaining = fb->len - i;
      size_t toSend = (remaining < chunkSize) ? remaining : chunkSize;
      bool lastChunk = (i + toSend) >= fb->len;
      
      client.beginPublish(image_topic, fb->len, lastChunk);
      client.write(fb->buf + i, toSend);
      client.endPublish();
      
      Serial.printf("Published chunk %d-%d\n", i, i+toSend);
      delay(10); // Small delay between chunks
    }
    Serial.println("Image published successfully");
  } else {
    Serial.println("Empty frame buffer");
  }
  
  // Return the frame buffer back to the driver for reuse
  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);
  
  // Initialize components
  setup_camera();
  setup_wifi();
  setup_sd();
  
  // Setup MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}