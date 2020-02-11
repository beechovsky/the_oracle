void setup() {
  // initialize serial communications at 9600 bps:
  delay(1000); // apparently startup delay is good to keep the arduino from getting confused
  Serial.begin(9600);
}

void loop() {
  // availableForWrite() gets the number of bytes available for writing in the serial buffer without blocking the write operation.
  while(Serial.availableForWrite()) {

    // Docs recommend using print() or println() for chars representing a number
    // https://www.arduino.cc/reference/en/language/functions/communication/serial/write/
    // Same as print(), but with carriage return character (ASCII 13, or '\r') and newline character (ASCII 10, or '\n')  
    Serial.println(analogRead(A0)); 

    // blocking stop so buffer doesn't overflow
    delay(2);
  }
}
