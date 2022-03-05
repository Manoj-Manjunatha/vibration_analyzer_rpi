"""
Read the accelerometer and gyro of MPU6050 from RaspberryPi and display the values.
"""

import smbus
from time import sleep
from datetime import datetime, timedelta

# MPU6050 Registers and their Addresses
# Config registers.
PWR_MGMT_1 = 0x6B
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C

# Sensor registers.
ACCEL_X_OUT_H = 0x3B
ACCEL_Y_OUT_H = 0x3D
ACCEL_Z_OUT_H = 0x3F
GYRO_X_OUT_H = 0x43
GYRO_Y_OUT_H = 0x45
GYRO_Z_OUT_H = 0x47

# SMPLRT_DIV = 0x19
# CONFIG = 0x1A
# INT_ENABLE = 0x38


def mpu_init(bus, device_address):
    """Initialize the MPU to read data."""

    # Writing 0 to power management will set the device to use internal 8Mhz oscilator.
    bus.write_byte_data(device_address, PWR_MGMT_1, 0)  # [0000 0000]

    # Writing 0 to gyroscope config will set the gyroscope mode to full scale +/- 250 deg/s. 
    bus.write_byte_data(device_address, GYRO_CONFIG, 0) # [0000 0000]

    # Writing 0 to accelerometer config will set the accelerometer mode to full scale +/- 2g. 
    bus.write_byte_data(device_address, ACCEL_CONFIG, 0) # [0000 0000]


    # # Write a sample-rate-register.
    # bus.write_byte_data(device_address, SMPLRT_DIV, 7)


    # Write to configuration-register.
    # bus.write_byte_data(device_address, CONFIG, 0)


    # Write to interrupt-enable-register.
    # bus.write_byte_data(device_address, INT_ENABLE, 1)

    sleep(0.5)


def read_raw_data(bus, device_address, sensor_address):
    """Get the raw data from the MPU and return it."""

    # Accelerometer and Gyro values are received in 16-bit.
    """
    Eg- 0x3B register receives first 8 bit data,
        and then 0x3C register receives next 8 bit data.
        Hence high, low variables are defined.
    """ 
    high = bus.read_byte_data(device_address, sensor_address)
    low = bus.read_byte_data(device_address, sensor_address + 1)

    """
    The 16bit data received in the form of chunks are stored in 'high', 'low' variables.
    It'll be in 2's compliment form. Inorder to store the 2 8bit data into 1 variable,
    we would do a left shift and then use a bitwise or to concatenate the next value.
    Eg- high = 0001 0010, low = 1001 0101
            -> (left shift 8 bits) 0001 0010 0000 0000.
            -> (OR with 'low' data) 0001 0010 0000 0000 | 1001 0101
            -> o/p = 0001 0010 1001 0101 = 4757(Decimal)
    """
    value = ((high << 8) | low)

    """
    The value returned will be in the range of 0 to 65535.
    Inorder to get -ve values, we'll subtract the values by 65535,
    which are greater than half of 65535. 
    """
    if value > (65535 / 2):
        value = value - 65535

    return value


def convert_accel_to_g(raw_data):
    """
    Since we had selected +/- 2g as range, we need divide the raw data by 16384 LSB/g,
    inorder to get the values in g(gravity).
    """
    return raw_data / 16384.0


def get_accelerometer_data(bus, device_address):

    # Accelerometer values.
    acc_x = read_raw_data(bus, device_address, ACCEL_X_OUT_H)
    acc_y = read_raw_data(bus, device_address, ACCEL_Y_OUT_H)
    acc_z = read_raw_data(bus, device_address, ACCEL_Z_OUT_H)

    # print('---------------- x={}, y={}, z={} -----------'.format(acc_x, acc_y, acc_z))

    acc_x_g = convert_accel_to_g(acc_x)
    acc_y_g = convert_accel_to_g(acc_y)
    acc_z_g = convert_accel_to_g(acc_z)

    return acc_x_g, acc_y_g, acc_z_g


def print_data(bus, device_address):
    """Read the data from MPU and print it."""
    print(get_accelerometer_data(bus, device_address))
    print('\n')


def main():

    # Call the init function to initialze.
    device_name = input('Enter device name \n')
    time_to_record = 10         # time to record data in seconds
    bus = smbus.SMBus(1)
    device_address = 0x68       # This is the I2C address [0110 1000]
    print("Initializing MPU6050. \n")
    mpu_init(bus, device_address)

    print("Reading data from Gyro and Accelerometer - ")
    end_datetime = datetime.now() + timedelta(seconds=time_to_record)
    filename = 'accelerometer_data_{}s_{}.txt'.format(time_to_record, end_datetime.timestamp())
    if device_name:
        filename = '{}_{}'.format(device_name, filename)
    print("Data logging started - ", datetime.now())

    with open(filename, 'w+') as f:
        while datetime.now() < end_datetime:
            f.write('{} -- {} \n'.format(datetime.now(), get_accelerometer_data(bus, device_address)))

    print("Data logging complete - ", datetime.now())
    print("File saved as - ", filename)


if __name__ == "__main__":
    main()
