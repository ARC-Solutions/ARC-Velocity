// arduino code
// read the string from the serial port and turn on/off the associated pin
#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

#define PIN 6
#define NUM_LEDS 144
#define DELAYVAL 500

Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

uint32_t color1 = strip.Color(100, 100, 100);
uint32_t color2 = strip.Color(0, 63, 61); // PETRONAS GREEN
uint32_t color3 = strip.Color(255, 0, 4);
uint32_t color4 = strip.Color(0,0,0);

int x;
String str;

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);   // backward - black
  pinMode(9, OUTPUT);   // forward - red
  pinMode(10, OUTPUT);  // left - orange
  pinMode(11, OUTPUT);  // right - yellow
  strip.begin();
}

void loop() {
  if (Serial.available() >= 0) {
    str = Serial.readStringUntil('\n');
    if (str.equals("left_on")) {
      digitalWrite(11, LOW);
      digitalWrite(10, HIGH);
    }
    if (str.equals("left_off")) {
      digitalWrite(10, LOW);
    }
    if (str.equals("right_on")) {
      digitalWrite(10, LOW);
      digitalWrite(11, HIGH);
    }
    if (str.equals("right_off")) {
      digitalWrite(11, LOW);
    }
    if (str.equals("backward_on")) {
      digitalWrite(9, LOW);
      digitalWrite(8, HIGH);
    }
    if (str.equals("backward_off")) {
      digitalWrite(8, LOW);
    }
    if (str.equals("forward_on")) {
      digitalWrite(8, LOW);
      digitalWrite(9, HIGH);
    }
    if (str.equals("forward_off")) {
      digitalWrite(9, LOW);
    }
    if(str.equals("home")){
        fadeBetweenColors(strip.getPixelColor(0), color1, 23);
    }
    if(str.equals("petronas")){
      fadeBetweenColors(strip.getPixelColor(0), color2, 23);
    }
    if(str.equals("ineos")){
      fadeBetweenColors(strip.getPixelColor(0), color3, 23);
    }
    if(str.equals("led_off")){
      fadeBetweenColors(strip.getPixelColor(0), color4, 23);
      turnOffAllLEDs();
    }
  }
}

void fadeBetweenColors(uint32_t startColor, uint32_t endColor, int duration) {
  uint8_t startRed = (startColor >> 16) & 0xFF;
  uint8_t startGreen = (startColor >> 8) & 0xFF;
  uint8_t startBlue = startColor & 0xFF;

  uint8_t endRed = (endColor >> 16) & 0xFF;
  uint8_t endGreen = (endColor >> 8) & 0xFF;
  uint8_t endBlue = endColor & 0xFF;

  float redStep = ((float)endRed - (float)startRed) / duration;
  float greenStep = ((float)endGreen - (float)startGreen) / duration;
  float blueStep = ((float)endBlue - (float)startBlue) / duration;

  redStep = redStep < 0 ? min(redStep, -1.0f) : max(redStep, 1.0f);
  greenStep = greenStep < 0 ? min(greenStep, -1.0f) : max(greenStep, 1.0f);
  blueStep = blueStep < 0 ? min(blueStep, -1.0f) : max(blueStep, 1.0f);

  for (int i = 0; i < duration; i++) {
    uint8_t currentRed = startRed + (redStep * i);
    uint8_t currentGreen = startGreen + (greenStep * i);
    uint8_t currentBlue = startBlue + (blueStep * i);

    uint32_t currentColor = strip.Color(currentRed, currentGreen, currentBlue);
    strip.fill(currentColor);
    strip.show();
    delay(10);
  }
  if(endColor == strip.Color(0,0,0)){
    turnOffAllLEDs();
  }
}

void turnOffAllLEDs() {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
}
