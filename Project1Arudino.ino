

// Define the pin connected to the LED
int ledPin = 13;

void setup() {
  // Start the serial communication
  Serial.begin(9600);
  
  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Check if data is available to read from serial
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming byte
    
    if (command == '2') {  // If signal is '2' (Glasses ON)
      blinkLED(2);  // Blink LED twice
    }
    else if (command == '3') {  // If signal is '3' (Glasses OFF)
      blinkLED(3);  // Blink LED three times
    }
  }
}

// Function to blink the LED a certain number of times
void blinkLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);  // Turn on the LED
    delay(500);  // Wait for 500ms
    digitalWrite(ledPin, LOW);   // Turn off the LED
    delay(500);  // Wait for 500ms
  }
}



