# compile, upload and monitor
arduino-cli compile --fqbn arduino:avr:mega arduino_mega/
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:mega  arduino_mega/
arduino-cli monitor -p /dev/ttyUSB0 --fqbn arduino:avr:mega --config baudrate=115200

