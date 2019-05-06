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

# Bewegungsmelder
GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

# Datenbank
db = MySQLdb.connect(host="localhost",
                     user="mySQL",
                     passwd="password",
                     db="testDB")
cursor = db.cursor()

# Initialisierung
Read = 0
State = 0


def blink_led(times=3):
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)


# JUST FOR TESTING REASONS:
# -----------------------------------------------------------------
# you must create a Cursor object. It will let
# you execute all the queries you need
cursor = db.cursor()

# Use all the SQL you like
cursor.execute("SELECT * FROM testTable;")

# print all the first cell of all the rows
# for row in cursor.fetchall():
#     print row[0]

# db.close()

# -----------------------------------------------------------------

try:
    print("Waiting, until PIR is in sleep mode ...")

    # Warten, bis Bewegungsmelder keine Bewegung erkennt, bevor die Endlosschleife gestartet wird
    while GPIO.input(MOTION_SENSOR_PIN) != 0:
        time.sleep(0.5)
    print("Start monitoring...")

    while True:  # TODO: Blinks twice 3 times, don't know why...
        Read = GPIO.input(MOTION_SENSOR_PIN)
        if State == 1 and Read == 0:
            State = 0
            print("Switching alarm off...")
            # cursor.execute ("")
            time.sleep(0.5)
        elif Read == 1:
            State = 1
            print("Motion recognized, starting alarm...")
            blink_led()

except KeyboardInterrupt:
    print("Stopping...")
    # db.close
    GPIO.cleanup()
