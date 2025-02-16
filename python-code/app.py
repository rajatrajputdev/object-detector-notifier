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