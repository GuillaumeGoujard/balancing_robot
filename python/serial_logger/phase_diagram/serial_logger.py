import serial
import csv
import time

SERIAL_PORT = "/dev/cu.usbserial-110"  # Change to match your device, e.g., "COM3" for Windows
BAUD_RATE = 19200  # Set the same baud rate as your robot
OUTPUT_CSV = "phase_test.csv"


def log_data(ser, filename, log_frequency_ms):
    """ Logs serial data into CSV with the given logging frequency. """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time (ms)", "PWM",  "Angle (deg.)", "Speed (deg./s)"])

        start_time = time.time()
        while True:
            line = ser.readline().decode().strip()
            if line:
                try:
                    pwm, angle, speed = map(float, line.split(","))
                    elapsed_time = round((time.time() - start_time) * 1000, 2)  # Time in ms
                    print(f"{elapsed_time} ms | PWM: {pwm} | Angle: {angle} deg | Speed: {angle} deg/s")
                    writer.writerow([elapsed_time, pwm, angle, speed])

                    # if (mode == '1' and pwm >= 255) or (mode == '2' and elapsed_time >= 5000):
                    #     print("Test completed.")
                    #     break

                except ValueError:
                    print(f"Skipping malformed line: {line}")
            
            # time.sleep(log_frequency_ms / 1000.0)  # Control logging frequency



if __name__ == "__main__":
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        log_data(ser, OUTPUT_CSV, log_frequency_ms=5)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        if 'ser' in locals():
            ser.close()