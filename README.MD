# Smart Object Detector & Notifier

An Arduino-based object detection and notification system, integrated with Python for storing data in Azure SQL.
## Demo
![https://github.com/rajatrajputdev/object-detector-notifier/blob/main/demonstration/demonst3.gif?raw=true](https://github.com/rajatrajputdev/object-detector-notifier/blob/main/demonstration/demonst3.gif?raw=true)
## Applications
- Can be used in vehicles as rear wall detector.
- Can be used in water tanks / aquariums with some modification to detect water levels.
- Can be used in door locks.

### Prequisites
- Arduino UNO
- C
- Python
- Azure SQL

### Features  
- Detects any disturbance within a 10-centimeter range.  
- LED indicators show **DANGER** or **CLEAR** status.  
- Data is continuously stored in an SQL database with dynamic distance ranges.

## Arduino Setup
[object-notifier.ino](https://github.com/rajatrajputdev/object-detector-notifier/blob/main/arduino-code/object-notifier/object-notifier.ino)
```c
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
```
### Arduino Circuit Setup
![https://raw.githubusercontent.com/rajatrajputdev/object-detector-notifier/refs/heads/main/demonstration/circuit.png](https://raw.githubusercontent.com/rajatrajputdev/object-detector-notifier/refs/heads/main/demonstration/circuit.png)
![https://raw.githubusercontent.com/rajatrajputdev/object-detector-notifier/refs/heads/main/demonstration/demonst1.jpg](https://raw.githubusercontent.com/rajatrajputdev/object-detector-notifier/refs/heads/main/demonstration/demonst1.jpg)

## Python & Azure SQL Setup
SQL Display in Azure Data Studio
![https://raw.githubusercontent.com/rajatrajputdev/object-detector-notifier/refs/heads/main/demonstration/sql-demo.png](https://raw.githubusercontent.com/rajatrajputdev/object-detector-notifier/refs/heads/main/demonstration/sql-demo.png)
[app.py](https://github.com/rajatrajputdev/object-detector-notifier/blob/main/python-code/app.py)
```python
import pyodbc
import serial
import time

DB_CONFIG = {
    "server": "",
    "database": "",  
    "username": "",  
    "password": "",  
    "driver": ""  # Ensure this driver is installed
}

# Function to establish database connection
def connect_to_db():
    try:
        conn = pyodbc.connect(
            f'DRIVER={DB_CONFIG["driver"]};SERVER={DB_CONFIG["server"]};PORT=1433;DATABASE={DB_CONFIG["database"]};UID={DB_CONFIG["username"]};PWD={DB_CONFIG["password"]}',
            timeout=30
        )
        print("Connected to database")
        return conn
    except pyodbc.Error as e:
        print("Database connection error:", e)
        return None

# Function to read data from Arduino and store it in the database
def read_from_arduino():
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)  # Adjust COM port as needed
        time.sleep(2) 
        print("Connected to Arduino")

        conn = connect_to_db()
        if conn is None:
            return
        
        cursor = conn.cursor()
        
        while True:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                detection_time = time.strftime('%H:%M:%S %Y-%m-%d')  # Get current timestamp
                print(f"Received data: {data} at {detection_time}")
                data = f'Object detected at [ ' + data + ' ]'
                cursor.execute("INSERT INTO ObjectDetected (DetectionTime, DetectedText) VALUES (?, ?)", detection_time, data)
                conn.commit()
                print("Data inserted into database")

    except serial.SerialException as e:
        print("Serial connection error:", e)
    except pyodbc.Error as e:
        print("Database error:", e)
    except Exception as e:
        print("General error:", e)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")
        if 'arduino' in locals() and arduino:
            arduino.close()
            print("Arduino connection closed.")

if __name__ == "__main__":
    read_from_arduino()
```



## License

MIT

**Free and Open Source Software with Open Source Hardware, Hell Yeah!**