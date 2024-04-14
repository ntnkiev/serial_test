import serial
import serial.tools.list_ports
# import rfranco
from serial.serialutil import SerialException


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = {str(index + 1): port.device for index, port in enumerate(ports)}
    return available_ports


def main():
    with open('data.bin', 'rb') as file:  # Замініть 'file.bin' на шлях до вашого bin-файлу
        data_bin = file.read()
    while True:
        ports = list_serial_ports()
        if ports:
            print("Available serial ports:")
            for index, port in ports.items():
                print(f"{index}: {port}")
        else:
            print("Serial port not found.")

        user_input = input("Enter port number or press 'r' to refresh or 'q' to exit: ")
        if user_input == "r":
            pass
        elif user_input == "q":
            exit()
        else:
            port = ports.get(user_input)
            if port:
                with serial.Serial(port, 9600, timeout=.1) as ser:
                    print(f"Port {port} open.")
                    while True:
                        data = ser.readline()
                        if data == b'\x16\x05':
                            ser.write(b'\x11\x1B\x53\x1A\x03\x36\x0A')
                        elif data == b'\x16\x1B\x53\x30\x31\x30\x31\x30\x31\x30\x31\x6C\x47\x53\x20\x20\x20\x20\x20\x0A':
                            ser.write(data_bin)
                        else:
                            pass
                        # rfranco.rf_poll(ser)
                        # ser.close()
            else:
                print("Illegal port number.")
        # data = ser.readline()


if __name__ == '__main__':
    main()
