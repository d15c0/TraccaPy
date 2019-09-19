# TraccaPy

## Table of contents
* [Getting Started](#getting-started)
* [What is TraccaPy?](#what-is-traccapy)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Configuration](#configuration)
* [Compatibility](#compatibility)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)
* [Notice](#notice)
* [GPSD install](#gpsd-install)

## Getting Started

These instructions will explain to you how to get a copy TraccaPy running on your machine.

### What is TraccaPy?

TraccaPy is a Python script that uploads your location to Traccar.  
This tool uses gpsd to get the current location, speed, bearing, altitude and accuracy.  
I used [tPacketCapture](https://play.google.com/store/apps/details?id=jp.co.taosoftware.android.packetcapture&hl=en) to find out what the endpoint was for updating device location.

### Dependencies

* [Geopy](https://github.com/geopy/geopy)
* [Requests](https://github.com/requests/requests)
* [gpsd-py3](https://github.com/MartijnBraam/gpsd-py3)
* [Python 3](https://www.python.org/downloads/)

### Installation
1. Clone the repository: `git clone https://gitlab.com/LapinoLapidus/traccapy`.
2. Install the dependencies `sudo pip3 install geopy requests gpsd-py3`.
2. Rename `config-sample.json` to `config.json`.
3. Modify the config.json file (see Configuration).
4. Set up [gpsd](https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi/use-gpsd), I used /dev/ttyS0
5. Run the file, `python3 Main.py`.

### Configuration

You should edit the configuration file.  
It contains the following:
* sleep_time(int): time to wait between position checks. Example: `60`
* server(string): location of Traccar server(**include http(s) and port number**). Example: `http://192.168.2.1:8082/`.
* device_id(int): has to correspond with the ID you made in Traccar. Example: `12345`.
* min_distance(int): Minimum distance required to send location, in meters. Set to negative to disable. Example: `10`.
* logging(bool): Set to true if you want to log to stdout on success and error. Example: `true`.

### Compatibility
I've only tested this on a Raspberry Pi 3 running Raspbian using the Adafruit GPS.  
It should work on any device running gpsd but I'm unsure.

### Contributing

Pull requests are welcome and appreciated. For major issues, please open an issue first please.  
Please be sure to test your changes before submitting.

### License

This project is licensed under the MIT License - see the LICENSE.md file for details.

### Acknowledgements

* [Bearing calculation function by jeromer](https://gist.github.com/jeromer/2005586)
* [Traccar](https://traccar.org)

### Notice

I am in no way affiliated with Traccar Ltd, this is a fan-made project.

### GPSD install

sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo dpkg-reconfigure gpsd

***edit /etc/default/gpsd***
sudo nano /etc/default/gpsd
