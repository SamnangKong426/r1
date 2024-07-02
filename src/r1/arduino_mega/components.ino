void initSerial() {
  /* Serial to display data */
  debug.begin(115200);
  debug.setTimeout(100);
  serialM.begin(115200);
  serialM.setTimeout(100);
  sbus_rx.Begin();
  Serial2.setTimeout(100);
}

void init_hardware() {
  pinMode(grip1, OUTPUT);
  pinMode(plant, OUTPUT);
  pinMode(grap, OUTPUT);
  pinMode(grip2, OUTPUT);

  digitalWrite(grip1, 0);
  digitalWrite(plant, 0);
  digitalWrite(grap, 0);
  digitalWrite(grip2, 0);
  digitalWrite(gas, 0);

  digitalWrite(relay, LOW);

  pinMode(relay, OUTPUT);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(sensor3, INPUT);
  pinMode(sensor4, INPUT);

  //Shot ball Motor
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  digitalWrite(R_EN, LOW);  //Low for close
  digitalWrite(L_EN, LOW);  //Low for close
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

//==============================================================================================


void readSbus() {
  if (sbus_rx.Read()) {
    /* Grab the received data */
    data = sbus_rx.data();
    /* Display the received data */
    for (int8_t i = 0; i < data.NUM_CH; i++) {
      data.ch[i] = map(data.ch[i], 282, 1722, -1500, 1500);
      // debug.print(data.ch[i]);
      // debug.print("\t");
    }
    // debug.println();
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