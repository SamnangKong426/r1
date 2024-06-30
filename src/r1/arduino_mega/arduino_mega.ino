#include "sbus.h"
#include <ArduinoJson.h>
#include <Servo.h>
#include <AccelStepper.h>

#define serialM Serial1
#define debug Serial
#define grip 7    // grip
#define arm 6     // arm
#define grap 3    // grap ball
#define rotate 2  //

// take ball in r1
#define relay 4
// Servo
#define servo1 35  //55_close, 100 open conveyor right
#define servo2 34  //150_close, 85 open conveyor left

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

AccelStepper stepperRight(1, 12, 13);  // conveyor right
AccelStepper stepperLeft(1, 10, 11);   // conveyor left

Servo ss1, ss2;
JsonDocument doc;


const int min_val = 1050;
const int mid_val = 1500;
const int max_val = 1950;

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
  run_angle(5, 0, 90);
}

void loop() {
  // realSerial();
  readSbus();
  if (data.ch[10] > 0 && data.ch[10] < 1700) {
    remoteControl(data.ch[1], data.ch[0], data.ch[2]);
  } else {
    remoteControl(0, 0, 0);
  }
  rotate_gun(data.ch[3]);

  // if (data.ch[5] > 0 && data.ch[5] < 1700) {
  //   digitalWrite(grap, HIGH);
  // } else if (data.ch[5] < 0 && data.ch[5] > -1700) {
  //   digitalWrite(grap, LOW);
  // }

  // if (data.ch[4] > 0 && data.ch[4] < 1700) {
  //   blackMotor(true);
  // } else if (data.ch[4] < 0 && data.ch[4] > -1700) {
  //   blackMotor(false);
  // }

  // if (data.ch[6] > 0 && data.ch[6] < 1700) {
  //   shotBall(true, data.ch[8]);
  // } else if (data.ch[6] < 0 && data.ch[6] > -1700) {
  //   shotBall(false, 0);
  // }


  // // if (sensor2 == 1){
  // //   debug.println("seedling left");
  // // }

  // // if (sensor4 == 1){
  // //   debug.println("seedling right");
  // // }
  // if (data.ch[9] > 0 && data.ch[9] < 1700) {
  //   while (1) {
  //     if (digitalRead(sensor2) == 0 && digitalRead(sensor4) == 0) {
  //       remoteControl(0, 100, 0);
  //     } else if (digitalRead(sensor2) == 1 && digitalRead(sensor4) == 1) {
  //       remoteControl(0, 0, 0);
  //       digitalWrite(arm, HIGH);
  //       delay(1000);
  //       digitalWrite(grip, HIGH);
  //       delay(1000);
  //       digitalWrite(rotate, HIGH);
  //       delay(1000);
  //       digitalWrite(grip, LOW);
  //       delay(1000);
  //       digitalWrite(arm, LOW);
  //       delay(1000);
  //       digitalWrite(grip, HIGH);
  //       delay(1000);
  //       digitalWrite(rotate, LOW);
  //       delay(1000);
  //       digitalWrite(grip, LOW);
  //       break;
  //     }
  //   }
  // } else if (data.ch[9] < 0 && data.ch[9] > -1700) {
  // } else {
  //   remoteControl(0, 0, 0);
  // }


  // serialization();
}

//=============================================================================================

void initSerial() {
  /* Serial to display data */
  debug.begin(115200);
  debug.setTimeout(10);
  serialM.begin(115200);
  serialM.setTimeout(100);
  sbus_rx.Begin();
  delay(1000);
  debug.println("Done Setup!");
}

void init_hardware() {
  pinMode(grip, OUTPUT);
  pinMode(arm, OUTPUT);
  pinMode(grap, OUTPUT);
  pinMode(rotate, OUTPUT);

  pinMode(relay, OUTPUT);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(sensor3, INPUT);
  pinMode(sensor4, INPUT);

  ss1.attach(servo1, 800, 2200);
  ss2.attach(servo2, 800, 2200);

  // ss1_close(true);
  // ss2_close(true);
  blackMotor(false);

  //Shot ball Motor
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  digitalWrite(R_EN, LOW);  //Low for close
  digitalWrite(L_EN, LOW);  //Low for close
}

void ss1_close(bool status) {
  if (status) {
    ss1.write(55);
  } else {
    ss1.write(100);
  }
}

void ss2_close(bool status) {
  if (status) {
    ss2.write(150);
  } else {
    ss2.write(85);
  }
}

void shotBall(bool status, int speed) {
  int pwm = map(speed, -1666, 1666, 0, 255);
  analogWrite(RPWM, LOW);  //HIGH or LOW
  if (status) {
    digitalWrite(R_EN, HIGH);  //Low for close
    digitalWrite(L_EN, HIGH);  //Low for close
  } else {
    digitalWrite(R_EN, LOW);  //Low for close
    digitalWrite(L_EN, LOW);  //Low for close
  }
  analogWrite(LPWM, pwm);  //0-255
}

void blackMotor(bool status) {
  if (status) {
    digitalWrite(relay, HIGH);
  } else {
    digitalWrite(relay, LOW);
  }
}

void rotate_gun(int angle) {
  int ang = map(angle, -1666, 1666, -5, 5);
  gun_ang += ang;
  if (gun_ang > 80) {
    gun_ang = 80;
  } else if (gun_ang < -80) {
    gun_ang = -80;
  }
  run_angle(5, gun_ang, 90);
}

//==============================================================================================


void readSbus() {
  if (sbus_rx.Read()) {
    /* Grab the received data */
    data = sbus_rx.data();
    /* Display the received data */
    for (int8_t i = 0; i < data.NUM_CH; i++) {
      data.ch[i] = map(data.ch[i], 282, 1722, -1500, 1500);
      debug.print(data.ch[i]);
      debug.print("\t");
    }
    debug.println();
    // remoteControl();
    // movement();
    // switchE();
    // buttonA1click();
    // buttonB1clickHolding();
    /* Set the SBUS TX data to the received data */
  }
}

//void switchE() {
//    // control switch
//  if (data.ch[4] > mid_val) {
//    Serial.println("Switch E is max");
//  } else if (data.ch[4] < mid_val) {
//    Serial.println("Switch E is min");
//  } else {
//    Serial.println("Switch E is mid");
//  }
//}
//
//void buttonA1click() {
//  // control Button A not holding
//  if (data.ch[8] > mid_val &&  buttonA == false) {
//    Serial.println("Button A is pressed");
//    buttonA = true;
//  } else if (data.ch[8] < mid_val && buttonA == true) {
//    Serial.println("Button A is pressed");
//    buttonA = false;
//  } else {
//    Serial.println("Button A is not pressed");
//  }
//}
//
//void buttonB1clickHolding() {
//    // control Button B holding
//  if (data.ch[9] > mid_val) {
//    Serial.println("Button B is pressed");
//  } else {
//    Serial.println("Button B is not pressed");
//  }
//}