import smbus
import time

def getOzone():
    bus = smbus.SMBus(1)
    data = bus.read_i2c_block_data(0x50, 0x00, 2)
    raw_adc = (data[0] & 0x0F) * 256 + data[1]
    ppm = (1.99 * raw_adc) / 4096.0 + 0.01
    return str(int(ppm));

def getLight():
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x60, 0x13, 0x29)
    bus.write_byte_data(0x60, 0x14, 0x89)
    bus.write_byte_data(0x60, 0x15, 0x02)
    bus.write_byte_data(0x60, 0x16, 0x00)
    bus.write_byte_data(0x60, 0x17, 0xF0)
    bus.write_byte_data(0x60, 0x18, (0x01 | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x03, 0x01)
    bus.write_byte_data(0x60, 0x04, 0x01)
    bus.write_byte_data(0x60, 0x07, 0x17)
    bus.write_byte_data(0x60, 0x17, 0x00)
    bus.write_byte_data(0x60, 0x18, (0x0E | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x17, 0x00)
    bus.write_byte_data(0x60, 0x18, (0x1E | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x17, 0x70)
    bus.write_byte_data(0x60, 0x18, (0x1D | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x17, 0x00)
    bus.write_byte_data(0x60, 0x18, (0x11 | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x17, 0x20)
    bus.write_byte_data(0x60, 0x18, (0x1F | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x17, 0x70)
    bus.write_byte_data(0x60, 0x18, (0x10 | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x17, 0x20)
    bus.write_byte_data(0x60, 0x18, (0x12 | 0xA0))
    time.sleep(0.01)
    response = bus.read_byte_data(0x60, 0x2E)
    bus.write_byte_data(0x60, 0x18, 0x0E)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x60, 0x22, 4)
    visible = data[1] * 256 + data[0]
    ir = data[3] * 256 + data[2]
    data = bus.read_i2c_block_data(0x60, 0x2C, 2)
    uv = data[1] * 256 + data[0]
    return (str(int(visible)), str(int(ir)), str(int(uv)));

def getTemp():
    bus = smbus.SMBus(1)
    bus.write_byte(0x76, 0x1E)
    time.sleep(0.5)
    data1 = bus.read_i2c_block_data(0x76, 0xA2, 2)
    data2 = bus.read_i2c_block_data(0x76, 0xA4, 2)
    data3 = bus.read_i2c_block_data(0x76, 0xA6, 2)
    data4 = bus.read_i2c_block_data(0x76, 0xA8, 2)
    data5 = bus.read_i2c_block_data(0x76, 0xAA, 2)
    data6 = bus.read_i2c_block_data(0x76, 0xAC, 2)
    c1 = data1[0] * 256 + data1[1]
    c2 = data2[0] * 256 + data2[1]
    c3 = data3[0] * 256 + data3[1]
    c4 = data4[0] * 256 + data4[1]
    c5 = data5[0] * 256 + data5[1]
    c6 = data6[0] * 256 + data6[1]
    bus.write_byte(0x76, 0x40)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x76, 0x00, 3)
    D1 = data[0] * 65536 + data[1] * 256 + data[2]
    bus.write_byte(0x76, 0x50)
    time.sleep(0.5)
    data0 = bus.read_i2c_block_data(0x76, 0x00, 3)
    D2 = data0[0] * 65536 + data0[1] * 256 + data0[2]
    dT = D2 - c5 * 256
    Temp = 2000 + dT * c6 / 8388608
    OFF = c2 * 131072 + (c4 * dT) / 64
    SENS = c1 * 65536 + (c3 * dT ) / 128

    if Temp >= 2000 :
        Ti = 5 * (dT * dT) / 274877906944
        OFFi = 0
        SENSi= 0
    elif Temp < 2000 :
        Ti = 3 * (dT * dT) / 8589934592
        OFFi= 61 * ((Temp - 2000) * (Temp - 2000)) / 16
        SENSi= 29 * ((Temp - 2000) * (Temp - 2000)) / 16
        if Temp < -1500:
            OFFi = OFFi + 17 * ((Temp + 1500) * (Temp + 1500))
            SENSi = SENSi + 9 * ((Temp + 1500) * (Temp +1500))

    OFF2 = OFF - OFFi
    SENS2= SENS - SENSi
    cTemp = (Temp - Ti) / 100.0
    fTemp =  cTemp * 1.8 + 32
    pressure = ((((D1 * SENS2) / 2097152) - OFF2) / 32768.0) / 100.0
    bus.write_byte(0x40, 0xFE)
    time.sleep(0.3)
    bus.write_byte(0x40, 0xF5)
    time.sleep(0.5)
    data0 = bus.read_byte(0x40)
    data1 = 0
    D3 = data0 * 256 + data1
    humidity = (-6.0 + (125.0 * (D3 / 65536.0)))
    return (str(int(humidity)), str(int(pressure)), str(round(cTemp,1)));
