USB-ISS module
-------------
![USB-ISS module](https://github.com/xinghuang077/ET2_test/blob/main/I2C_Config_test/IMGs/usb-iss%20module.png)
  - The USB-ISS  Multifunction USB Communications Module provides a complete interface between your PC and the **I2C bus**, SPI bus, a Serial port and general purpose Analogue Input or Digital I/O. The module is powered from the USB. Operating voltage is selectable between 3.3v and 5v.
  - USB-ISS document: https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm
  - USB-ISS Python library: https://usb-iss.readthedocs.io
  - USB-ISS Python souce code: https://github.com/sneakypete81/usb_iss/tree/master/src/usb_iss
  - Since the operating voltage of USB-ISS module is higher than the power of ET2_test chip (1.2 V), a level translator is needed on the test PCB board to lower the logic high voltages of SDA and SCL to 1.2 V.

Usage Example
-------------
```

    from usb_iss import UsbIss, defs

    # Configure I2C mode

    iss = UsbIss()
    iss.open("COM3")
    iss.setup_i2c()

    # Write and read back some data
    # NOTE: I2C methods use 7-bit device addresses (0x00 - 0x7F)

    iss.i2c.write(0x62, 0, [0, 1, 2]);
    data = iss.i2c.read(0x62, 0, 3)

    print(data)
    # [0, 1, 2]
```

Installing
----------
```
    pip install usb-iss

```
