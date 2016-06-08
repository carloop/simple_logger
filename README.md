# Serial and TCP CAN bus logger for [Carloop](https://carloop.io)

Reads CAN messages at 500 kbit and outputs them formatted as JSON to the USB Serial and a network port

To see the USB serial port dump, read the port with cat, screen or PuTTY on Windows.
```
cat /dev/tty.usbmodem1411 (update for your port number)
```

To start the network server, call the function "startServer" on your
device:

```
particle call my_carloop startServer
```

To get the IP address and port of the Carloop:

```
particle get my_carloop ip
particle get my_carloop port
```

You must be on the same WiFi network as the Carloop to be able to
connect to the server. You can use telnet or PuTTY in raw mode to
connect with the IP address and port from above:
```
telnet 192.168.0.127 9000
```

Use tee to save the data dump:
```
cat /dev/tty.usbmodem1411 | tee my_drive.log
telnet 192.168.0.127 9000 | tee my_drive.log
```

## Building

Copy this application to Particle Build and add the [Carloop library](https://build.particle.io/libs/56eebf35e1b20225ce00048d)

## License

Copyright 2016 Julien Vanier

Distributed under the MIT license. See LICENSE.txt for more details.

