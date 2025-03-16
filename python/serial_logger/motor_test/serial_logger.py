import serial
import csv
import time

SERIAL_PORT = "/dev/cu.usbserial-21230"  # Change to match your device, e.g., "COM3" for Windows
BAUD_RATE = 115200  # Set the same baud rate as your robot
OUTPUT_CSV = "motor_ramp_test.csv"
RAMP_CSV = "motor_ramp_test.csv"
STEP_CSV = "motor_step_test.csv"

def send_signal(ser, mode):
    """ Sends start signal ('1' for ramp test, '2' for step test) to Arduino. """
    print(f"Sending test mode '{mode}' to Arduino...")
    ser.write(mode.encode())  # Send '1' or '2'
    time.sleep(1)  # Wait for Arduino response
    while ser.in_waiting:
        print(ser.readline().decode().strip())  # Print Arduino response


def log_data(ser, filename, log_frequency_ms):
    """ Logs serial data into CSV with the given logging frequency. """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time (ms)", "PWM", "Motor Speed (RPM)"])

        start_time = time.time()
        while True:
            line = ser.readline().decode().strip()
            if line:
                try:
                    pwm, speed_rpm = map(float, line.split(","))
                    elapsed_time = round((time.time() - start_time) * 1000, 2)  # Time in ms
                    print(f"{elapsed_time} ms | PWM: {pwm} | Speed: {speed_rpm} RPM")
                    writer.writerow([elapsed_time, pwm, speed_rpm])

                    if (mode == '1' and pwm >= 255) or (mode == '2' and elapsed_time >= 5000):
                        print("Test completed.")
                        break

                except ValueError:
                    print(f"Skipping malformed line: {line}")
            
            # time.sleep(log_frequency_ms / 1000.0)  # Control logging frequency



if __name__ == "__main__":
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allow time for Arduino reset

        mode = input("Enter test mode ('1' for ramp test, '2' for step test): ").strip()
        if mode not in ['1', '2']:
            print("Invalid input! Exiting.")
            exit()

        send_signal(ser, mode)  # 🚀 Send mode to Arduino

        if mode == '1':
            log_data(ser, RAMP_CSV, log_frequency_ms=100)  # Ramp test: log at 100ms
        elif mode == '2':
            log_data(ser, STEP_CSV, log_frequency_ms=5)  # Step test: log at 10ms

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        if 'ser' in locals():
            ser.close()