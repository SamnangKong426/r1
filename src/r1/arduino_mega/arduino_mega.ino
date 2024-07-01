#include "sbus.h"
#include <ArduinoJson.h>

#define serialM Serial1
#define debug Serial
#define grip1 7  // grip1
#define plant 6  // plant
#define grap 3   // grap ball
#define grip2 2  // grip2
#define gas 5   // gas station

// take ball in r1
#define relay 4

//Sensor
#define sensor1 36
#define sensor2 37  // front left
#define sensor3 40
#define sensor4 41  //front right

//Shot ball Motor
#define R_EN 44
#define L_EN 43
#define LPWM 8
#define RPWM 9
JsonDocument doc;

float lx = 250;
float ly = 250;
float r = 63.5;

int gun_ang = 0;

float M[4] = { 0, 0, 0, 0 };

double vx, vy, w;

/* SBUS object, reading SBUS */
bfs::SbusRx sbus_rx(&Serial2);
/* SBUS data */
bfs::SbusData data;

void setup() {
  initSerial();
  init_hardware();
  delay(500);
  debug.println("Start");
}

void loop() {
  readSbus();
  // Switch G
  if (data.ch[10] > 0 && data.ch[10] < 1700) {
    // Joystick X1 Y1 X2
    remoteControl(data.ch[1], data.ch[0], data.ch[2]);

    // Button A
    if (data.ch[4] > 0 && data.ch[4] < 1700) {
      digitalWrite(grip1, 1);
      digitalWrite(grip2, 1);
      delay(50);
      digitalWrite(plant, 0);
    }
    
    // Button B
    if (data.ch[5] >= 1) {
      digitalWrite(plant, 1);
      delay(50);
      digitalWrite(grip1, 0);
      delay(250);
    } else if (data.ch[5] <= -1) {
      digitalWrite(plant, 0);
    }

    // Button C
    if (data.ch[6] > 0 && data.ch[6] < 1700) {
      digitalWrite(plant, 1);
      delay(50);
      digitalWrite(grip2, 0);
    }

    // Button D
    if (data.ch[7] > 0 && data.ch[7] < 1700) {
      digitalWrite(grap, 1);
    } else {
      digitalWrite(grap, 0);
    }

    // Switch H
    if (data.ch[11] > 0 && data.ch[11] < 1700) {
      digitalWrite(relay, HIGH);
      shotBall(true, data.ch[8]);
    } else {
      digitalWrite(relay, LOW);
      shotBall(false, 0);
    }


  } else {
    remoteControl(0, 0, 0);
  }
}

//=============================================================================================

