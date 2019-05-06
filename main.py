import time

import MySQLdb
import RPi.GPIO as GPIO

# Pins
MOTION_SENSOR_PIN = 16
LED_PIN = 11

GPIO.setmode(GPIO.BOARD)

# LED
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)

# Motion sensor
GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

# Database
db = MySQLdb.connect(host="localhost",
                     user="mySQL",
                     passwd="password",
                     db="testDB")
cursor = db.cursor()

# initiation
Read = 0
State = 0


# LED blinks according to parameters value. Default is 3.
def blink_led(times=3):
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)


# writes the log into the DB when the state of the alarm-system changes
def insert_time(is_active):
    try:
        cursor.execute("INSERT INTO alarm_system (is_active) VALUES(1);") if is_active else \
            cursor.execute("INSERT INTO alarm_system (is_active) VALUES(0)")
        db.commit()
    except cursor.MySQLError:
        print(cursor.MySQLError)


try:
    print("Waiting, until PIR is in sleep mode...")

    # Waiting until there is no more motion in front of the motion sensor.
    while GPIO.input(MOTION_SENSOR_PIN) != 0:
        time.sleep(0.5)

    print("Start monitoring...")

    # Main continuous loop
    while True:
        Read = GPIO.input(MOTION_SENSOR_PIN)

        # If alarm switches from 'active' to 'not active'
        if State == 1 and Read == 0:
            State = 0
            print("Switching alarm off...")
            insert_time(0)
            time.sleep(0.5)

        # If alarm switches from 'not active' to 'active'
        elif Read == 1:
            State = 1
            print("Motion recognized, starting alarm...")
            insert_time(1)
            blink_led()

# User can interrupt the loop with pressing ctrl + 'c'
except KeyboardInterrupt:
    print("Stopping...")
    GPIO.cleanup()
    db.close()
