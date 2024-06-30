void trans(byte data[], int datasize, int datareply, int mid) {
  byte reply[datareply];
  bool success = false;
  int count = 0;
  while (success == false) {
    serialM.write(data, datasize);
    delay(5);
    if (serialM.available() > 0) {
      serialM.readBytes(reply, datareply);
    }

    // for (int i = 0; i < datareply; i++) {
    //   debug.print(reply[i], HEX);
    //   debug.print(" ");
    // }
    // debug.println();

    byte checksum = reply[0] + reply[1] + reply[2] + reply[3];
    if (reply[0] == 0x3e && reply[1] == 0xa2 && reply[2] == mid && reply[3] == 0x07 && reply[4] == checksum) {
      success = true;
    } else {
      success = false;
      count++;
      //      debug.println(count);
    }
    if (count > 10) {
      break;
    }
  }
}
void run_speed(int mid, long velo) {
  byte speed[10] = { 0x3e, 0xa2, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
  long ratio = velo * 100 * 10;
  speed[9] = 0;
  speed[2] = mid;
  speed[4] = speed[0] + speed[1] + speed[2] + speed[3];
  for (int i = 5; i < 9; i++) {
    speed[i] = ratio >> (8 * (i - 5));
    speed[9] += speed[i];
  }
  trans(speed, 10, 13, mid);
}

void run_angle(int mid, long angle, long velo) {
  byte data[18] = { 0x3e, 0xa4, 0x01, 0x0c};
  long ratio_velo = velo * 100 * 3;
  long ratio_ang = angle * 100 * 3;
  data[17] = 0;
  data[2] = mid;
  data[4] = data[0] + data[1] + data[2] + data[3];
  for (int i = 5; i < 13; i++) {
    data[i] = ratio_ang >> (8 * (i - 5));
    data[17] += data[i];
  }
  for (int i = 13; i < 17; i++) {
    data[i] = ratio_velo >> (8 * (i - 13));
    data[17] += data[i];
  }
  trans(data, 18, 8, mid);
}


void remoteControl(int _vx, int _vy, int _w) {
  double w1, w2, w3, w4;
  float vx = _vx;
  float vy = _vy;
  float w = map1(_w, -1666, 1666, 2, -2);

  // debug.print("Vx: ");
  // debug.print(vx);
  // debug.print(", Vy: ");
  // debug.print(vy);
  // debug.print(", omega: ");
  // debug.println(w);

  w1 = degrees(((vx - vy) - (w * (lx + ly))) / r);
  w2 = degrees(((vx + vy) + (w * (lx + ly))) / r);
  w3 = degrees(((vx + vy) - (w * (lx + ly))) / r);
  w4 = degrees(((vx - vy) + (w * (lx + ly))) / r);

  // debug.print("M[0]: ");
  // debug.print(w1);
  // debug.print(", M[1]: ");
  // debug.print(w2);
  // debug.print(", M[2]: ");
  // debug.print(w3);
  // debug.print(", M[3]: ");
  // debug.println(w4);

  run_speed(1, w1);
  run_speed(2, -w2);
  run_speed(3, w3);
  run_speed(4, -w4);
}

void pos_run(double vx, double vy, double w) {
  double w1, w2, w3, w4;

  w1 = degrees(((vx - vy) - (w * (lx + ly))) / r);
  w2 = degrees(((vx + vy) + (w * (lx + ly))) / r);
  w3 = degrees(((vx + vy) - (w * (lx + ly))) / r);
  w4 = degrees(((vx - vy) + (w * (lx + ly))) / r);
  run_speed(1, w1);
  run_speed(2, -w2);
  run_speed(3, w3);
  run_speed(4, -w4);
}

float map1(float Input, float Min_Input , float Max_Input , float Min_Output, float Max_Output) {

  return (float) ((Input - Min_Input) * (Max_Output - Min_Output) / (Max_Input - Min_Input) + Min_Output);
}

