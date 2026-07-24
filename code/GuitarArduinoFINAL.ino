const int numStrings = 5;
const int numFrets = 12;

// Digital pins started from 3 bc 0-2 are special
const int strList[numStrings] = {3, 4, 5, 6, 7}; // MAKE SURE YOU WIRE THE RIGHT PINS OR CHANGE THE LIST
const int fretList[numFrets] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11};

void setup() {
  // Strings to digital output
  for (int str = 0; str < numStrings; str++) {
    pinMode(strList[str], OUTPUT);
  }

  // Frets to analog input
  for (int fret = 0; fret < numFrets; fret++) {
    pinMode(fretList[fret], INPUT);
  }
  Serial.begin(9600);
}

void loop() {
  for (int curStr = 0; curStr < numStrings; curStr++) {
    // Set string high for reading each fret, then low for next string reading
    digitalWrite(strList[curStr], HIGH);

    // Prints to serial monitor in form "strNumber_[Array of fret values]"
    Serial.print(curStr); Serial.print(" ");
    for (int curFret = 0; curFret < numFrets; curFret++) {
      if (curFret < 11) {
        Serial.print(analogRead(fretList[curFret])); Serial.print(",");
      } else {
        Serial.print(analogRead(fretList[curFret]));
      }
    digitalWrite(strList[curStr], LOW);
    }
    Serial.println();

    delay(50);
    }
}
