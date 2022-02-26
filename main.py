"""
Read the accelerometer and gyro of MPU6050 from RaspberryPi and display the values.
"""

import smbus
from time import sleep

# MPU6050 Registers and their Addresses
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_X_OUT_H = 0x3B
ACCEL_Y_OUT_H = 0x3D
ACCEL_Z_OUT_H = 0x3F
GYRO_X_OUT_H = 0x43
GYRO_Y_OUT_H = 0x45
GYRO_Z_OUT_H = 0x47


def mpu_init(bus, device_address):
    """Initialize the MPU to read data."""

    # Write a sample-rate-register.
    bus.write_byte_data(device_address, SMPLRT_DIV, 7)

    # Write to power-management-register.
    bus.write_byte_data(device_address, PWR_MGMT_1, 1)

    # Write to configuration-register.
    bus.write_byte_data(device_address, CONFIG, 0)

    # Write to gyro-configuration-register.
    bus.write_byte_data(device_address, GYRO_CONFIG, 24)

    # Write to interrupt-enable-register.
    bus.write_byte_data(device_address, INT_ENABLE, 1)


def read_raw_data(bus, device_address, sensor_address):
    """Get the raw data from the MPU and return it."""

    # Accelerometer and Gyro values are 16-bit.
    high = bus.read_byte_data(device_address, sensor_address)
    low = bus.read_byte_data(device_address, sensor_address + 1)

    # Concatenate high and low value.
    value = ((high << 8) | low)    # high LEFT_SHIFT 8 bits OR with low.

    # Get a signed value from MPU.
    if(value > 32768):
        value = value - 65536

    return value


def print_data(bus, device_address):
    """Read the data from MPU and print it."""

    # Accelerometer values.
    acc_x = read_raw_data(bus, device_address, ACCEL_X_OUT_H)
    acc_y = read_raw_data(bus, device_address, ACCEL_Y_OUT_H)
    acc_z = read_raw_data(bus, device_address, ACCEL_Z_OUT_H)

    print("ACCEL RAW:")
    print("X: {}, Y: {}, Z: {}".format(acc_x, acc_y, acc_z))

    # Full scale range conversion.
    print("\n After conversion:")
    print("X: {}, Y: {}, Z: {}".format((acc_x / 16384.0), (acc_y / 16384.0), (acc_z / 16384.0)))
    print("\n \n")


def main():

    # Call the init function to initialze.
    bus = smbus.SMBus(1)
    device_address = 0x68
    print("Initializing MPU6050.")
    mpu_init(bus, device_address)

    print("Reading data from Gyro and Accelerometer - ")
    while True:
        print_data(bus, device_address)
        sleep(1)


if __name__ == "__main__":
    main()

