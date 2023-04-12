// arduino code
// read the string from the serial port and turn on/off the associated pin
#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NUM_LEDS 144
Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);
int x;
String str;

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);   // backward - black
  pinMode(9, OUTPUT);   // forward - red
  pinMode(10, OUTPUT);  // left - orange
  pinMode(11, OUTPUT);  // right - yellow
  strip.begin();
  strip.fill(strip.Color(0,89,86)); //PETRONAS GREEN
  //strip.fill(strip.Color(255,0,4));
  strip.show();
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
  }
}