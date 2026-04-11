/*
  NEUROLEARN ASSIST - Braille Arduino Interface
  Receives UTF-8 braille text over serial and maps to a 6-pin braille cell driver.
  Replace pin mapping and pulse timing to match your solenoid driver hardware.
*/

const int DOT_PINS[6] = {2, 3, 4, 5, 6, 7};
const int CELL_DELAY_MS = 120;

String incoming = "";

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 6; i++) {
    pinMode(DOT_PINS[i], OUTPUT);
    digitalWrite(DOT_PINS[i], LOW);
  }
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      processLine(incoming);
      incoming = "";
    } else {
      incoming += c;
    }
  }
}

void processLine(const String &text) {
  // UTF-8 braille can be multi-byte, so production hardware should decode bytes properly.
  // This minimal firmware expects pre-converted simple symbols and triggers a demo pulse.
  for (int i = 0; i < text.length(); i++) {
    char ch = text.charAt(i);
    activatePatternForAscii(ch);
    delay(CELL_DELAY_MS);
    clearPins();
  }
}

void activatePatternForAscii(char ch) {
  // Simple placeholder mapping for ASCII letters (a-z) to braille dots.
  // Replace with full mapping logic for your mechanical cell layout.
  switch (tolower(ch)) {
    case 'a': setDots(1, 0, 0, 0, 0, 0); break;
    case 'b': setDots(1, 1, 0, 0, 0, 0); break;
    case 'c': setDots(1, 0, 0, 1, 0, 0); break;
    case 'd': setDots(1, 0, 0, 1, 1, 0); break;
    case 'e': setDots(1, 0, 0, 0, 1, 0); break;
    default: clearPins(); break;
  }
}

void setDots(int d1, int d2, int d3, int d4, int d5, int d6) {
  digitalWrite(DOT_PINS[0], d1 ? HIGH : LOW);
  digitalWrite(DOT_PINS[1], d2 ? HIGH : LOW);
  digitalWrite(DOT_PINS[2], d3 ? HIGH : LOW);
  digitalWrite(DOT_PINS[3], d4 ? HIGH : LOW);
  digitalWrite(DOT_PINS[4], d5 ? HIGH : LOW);
  digitalWrite(DOT_PINS[5], d6 ? HIGH : LOW);
}

void clearPins() {
  for (int i = 0; i < 6; i++) {
    digitalWrite(DOT_PINS[i], LOW);
  }
}
