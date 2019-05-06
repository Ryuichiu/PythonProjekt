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

# Initialisierung
Read = 0
State = 0

# Curser Initialisierung
cursor = db.cursor()


def blink_led(times=3):
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)


def insert_time(active):
    try:
        #sql = "insert into alarm_system (is_active) values(%s);"
        cursor.execute("insert into alarm_system (is_active) values(1);") if active else\
            cursor.execute("insert into alarm_system (is_active) values (0)")
        db.commit()
    except cursor.MySQLError:
        print(cursor.MySQLError)


try:
    print("Waiting, until PIR is in sleep mode ...")

    # Warten, bis Bewegungsmelder keine Bewegung erkennt, bevor die Endlosschleife gestartet wird
    while GPIO.input(MOTION_SENSOR_PIN) != 0:
        time.sleep(0.5)
    print("Start monitoring...")
    insert_time(0)
    insert_time(1)

    while True:
        Read = GPIO.input(MOTION_SENSOR_PIN)
        if State == 1 and Read == 0:
            State = 0
            print("Switching alarm off...")
            insert_time(0)
            time.sleep(0.5)
        elif Read == 1:
            State = 1
            print("Motion recognized, starting alarm...")
            insert_time(1)
            blink_led()

except KeyboardInterrupt:
    print("Stopping...")
    # db.close
    GPIO.cleanup()
    db.close()
