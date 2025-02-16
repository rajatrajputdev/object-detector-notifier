#define TRIG_PIN 7
#define ECHO_PIN 6
#define ALARM_PIN 13
#define CLEAR 4

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(ALARM_PIN, OUTPUT);
  pinMode(CLEAR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  long duration;
  float distance;

  // Send a 10us pulse to trigger pin
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read the echo pin
  duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calculate distance in cm
  distance = duration * 0.034 / 2;

  // Check distance and activate alarm if needed
  if (distance < 10 && distance > 0) {
    digitalWrite(ALARM_PIN, HIGH);
    digitalWrite(CLEAR, LOW);
    Serial.print(distance);
    Serial.print(" cm, ");

  } else {
    digitalWrite(ALARM_PIN, LOW);
    digitalWrite(CLEAR, HIGH);

  }

  delay(500);
}
