# compile, 
arduino-cli compile --fqbn arduino:avr:mega src/r1/arduino_mega/

# upload
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:mega  src/r1/arduino_mega/

# monitor
# arduino-cli monitor -p /dev/ttyUSB0 --fqbn arduino:avr:mega --config baudrate=115200

