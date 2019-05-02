import RPi.GPIO as GPIO
import time
import threading


class Alarm:
    # variables

    MOTION_SENSOR_PIN = 16
    LED_PIN = 11

    alarmIsOn = False

    GPIO.setmode(GPIO.BOARD)

    # led
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, GPIO.LOW)

    # motion sensor
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

    def start_alarm():
        def start_loop():
            Alarm.alarmIsOn = True
            sleeper = 0.5
            while():
                GPIO.output(Alarm.LED_PIN, GPIO.HIGH)
                time.sleep(sleeper)
                GPIO.output(Alarm.LED_PIN, GPIO.LOW)
                time.sleep(sleeper)

        threading.Thread(target=start_loop).start()

    def stop_alarm():
        Alarm.alarmIsOn = False

    start_alarm()
    time.sleep(10)
    stop_alarm()

    print("Stopped, waiting 3 Secs...")
    time.sleep(3)
    print("Starting Alarm now.")
    start_alarm()
    print("Started, waiting 10 Secs and stop program")
    time.sleep(10)

    GPIO.cleanup()