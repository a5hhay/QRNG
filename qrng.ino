void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A1);

  // bit extraction
  int bit = (sensorValue > 218) ? 1 : 0;

  Serial.println(bit); 

  delay(5);  
}
