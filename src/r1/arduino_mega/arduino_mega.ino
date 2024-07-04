#include "sbus.h"
#include <ArduinoJson.h>
#include <AccelStepper.h> 

#define serialM Serial1
#define debug Serial
#define grip1 7  // grip1
#define plant 6  // plant
#define grap 3   // grap ball
#define grip2 2  // grip2
#define gas 5    // gas station

// take ball in r1
#define relay 4

//stepper
#define DIRx 13
#define STEPx 12
#define EN 38 
AccelStepper gun(1,STEPx,DIRx); 
 

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

float lx = 225;
float ly = 179.55;
float r = 63.5;

int gun_ang = 0;
bool buttonA, buttonB, buttonC, buttonD;
bool isMidG = false;

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
  digitalWrite(gas, 1);
  gun.setMaxSpeed(1000);
  gun.setSpeed(1000);
  
}

void loop() {
  readSbus();
  readSerial();
  gun.move(1000);
  gun.run();
  // Switch G
  if (data.ch[10] > 0 && data.ch[10] < 1700) {
    manualMode();
  } else if(data.ch[10] < 0 && data.ch[10] > -1700) {
    pos_run(vx, vy, w);
  } else {
    if (isMidG == false) {
      isMidG = true;
      remoteControl(0, 0, 0);
    }
  }
}
//=============================================================================================

void manualMode(){
  // Joystick X1 Y1 X2
  remoteControl(data.ch[1], data.ch[0], data.ch[2]);
  // remoteControl(data.ch[0], -data.ch[1], data.ch[2]);

  // // Button A
  // if (data.ch[4] > 0 && data.ch[4] < 1700 && !buttonA) {
  //   debug.println("Button A on");
  //   digitalWrite(grip1, 1);
  //   digitalWrite(grip2, 1);
  //   delay(500);
  //   digitalWrite(plant, 1);
  //   buttonA = true;
  // } else if (data.ch[4] < 0 && data.ch[4] > -1700) {
  //   buttonA = false;
  // }

  // // Button B
  // if (data.ch[5] > 0 && data.ch[5] < 1700 && !buttonB) {
  //   debug.println("down");
  //   digitalWrite(plant, 0);
  //   delay(500);
  //   digitalWrite(grip1, 0);
  //   delay(1000);
  //   digitalWrite(plant, 1);
  //   debug.println("up");
  //   buttonB = true;
  //   debug.println("Button B on");
  // } else if (data.ch[5] < 0 && data.ch[5] > -1700) {
  //   buttonB = false;
  //   // debug.println("Button B off");
  // }

  // // Button C
  // if (data.ch[6] > 0 && data.ch[6] < 1700 && !buttonC) {
  //   debug.println("Button C on");
  //   digitalWrite(plant, 0);
  //   delay(50);
  //   digitalWrite(grip2, 0);

  //   buttonC = true;
  // } else if (data.ch[6] < 0 && data.ch[6] > -1700) {
  //   buttonC = false;
  // }

  // // Button D
  // // if (data.ch[7] > 0 && data.ch[7] < 1700) {
  // //   debug.println("Button D on");
  // //   digitalWrite(grap, 1);
  // // } else if({
  // //   digitalWrite(grap, 0);
  // // }

  // // Switch H
  // if (data.ch[11] > 0 && data.ch[11] < 1700) {
  //   digitalWrite(relay, HIGH);
  //   shotBall(true, data.ch[8]);
  // } else if (data.ch[11] == 0) {
  //   digitalWrite(relay, LOW);
  //   shotBall(false, 0);
  // }
}