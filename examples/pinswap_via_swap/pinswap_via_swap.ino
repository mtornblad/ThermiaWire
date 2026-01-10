// ThermiaWire pinswapping via ThermiaWire.pins()
// Copy of ThermiaWire Master Reader
// except for the ThermiaWire.pins() call.
// This is mostly here to make sure it gets tested by CI.


#include <ThermiaWire.h>

void setup() {
  ThermiaWire.swap(2);        // Choose pin swapping level 2 (PC2/PC3 master/slave)
  ThermiaWire.begin();        // join i2c bus (address optional for master)
  Serial.begin(115200);  // start serial for output
}

void loop() {
  ThermiaWire.requestFrom(8, 6);    // request 6 bytes from slave device #8

  while (ThermiaWire.available()) { // slave may send less than requested
    char c = ThermiaWire.read(); // receive a byte as character
    Serial.print(c);         // print the character
  }

  delay(500);
}
