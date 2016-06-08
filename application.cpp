/* Serial and TCP CAN bus logger for Carloop
 *
 * Reads CAN messages at 500 kbit and outputs them formatted as JSON to
 * the USB Serial and a network port
 *
 * To see the USB serial port dump, read the port with cat, screen or
 * PuTTY on Windows.
 * cat /dev/tty.usbmodem1411 (update for your port number)
 *
 * To start the network server, call the function "startServer" on your
 * device:
 * particle call my_carloop startServer
 *
 * To get the IP address and port of the Carloop:
 * particle get my_carloop ip
 * particle get my_carloop port
 *
 * You must be on the same WiFi network as the Carloop to be able to
 * connect to the server. You can use telnet or PuTTY in raw mode to
 * connect with the IP address and port from above:
 * telnet 192.168.0.127 9000
 *
 * Use tee to save the data dump:
 * cat /dev/tty.usbmodem1411 | tee my_drive.log
 * telnet 192.168.0.127 9000 | tee my_drive.log
 *
 * Copyright 2016 Julien Vanier
 *
 * Distributed under the MIT license. See LICENSE.txt for more details.
 */

#include "application.h"
#include "carloop/carloop.h"
#include <memory>

using namespace std;

SYSTEM_MODE(SEMI_AUTOMATIC);
SYSTEM_THREAD(ENABLED);

String dumpMessage(const CANMessage &message);

Carloop<CarloopRevision2> carloop;

String myIp;
const int myPort = 9000;

unique_ptr<TCPServer> server;
TCPClient client;

int startServer(String portStr) {
  client.stop();
  server.reset(new TCPServer(myPort));
  server->begin();
  return myPort;
}

void setup() {
  Serial.begin(9600);
  carloop.begin();

  Particle.variable("ip", myIp);
  Particle.variable("port", myPort);
  Particle.function("startServer", startServer);

  Particle.connect();
}

void loop() {
  myIp = WiFi.localIP();

  String dump;
  CANMessage message;
  while(carloop.can().receive(message)) {
    // If the serial port or TCP server is overwhelmed, limit messages
    // if(message.id >= 0x700)
    dump += dumpMessage(message);
  }

  Serial.write(dump);

  if(server) {
    if(client.connected()) {
      client.write(dump);
    } else {
      client = server->available();
    }
  }
}

String dumpMessage(const CANMessage &message) {
  String str;

  str = String::format("{\"timestamp\":%f,\"bus\":1,\"id\":\"0x%03x\",\"data\":\"", millis() / 1000.0, message.id, message.len);
  for(int i = 0; i < message.len; i++) {
    if(i == 0) {
      str += "0x";
    }
    str += String::format("%02x", message.data[i]);
  }
  str += "\"}\n";
  return str;
}

