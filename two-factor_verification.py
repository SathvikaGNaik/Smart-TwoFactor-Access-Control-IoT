from machine import I2C, Pin, ADC, PWM
import time
import network
import urequests
from mfrc522 import MFRC522
from pico_i2c_lcd import I2cLcd

# ---------------- WIFI ----------------
SSID = "OPPO A52"
PASSWORD = "01234567"
API_KEY = "1AJ7GNVPX1JSHYX7"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting WiFi...")
while not wifi.isconnected():
    time.sleep(1)
print("WiFi Connected")

# ---------------- LCD ----------------
i2c = I2C(1, sda=Pin(18), scl=Pin(19))
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)

def display(msg):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(msg[:16])

# ---------------- RFID ----------------
rfid = MFRC522(spi_id=0, sck=2, miso=4, mosi=7, cs=5, rst=9)
AUTHORIZED_CARD = 1545502562

# ---------------- KEYPAD ----------------
rows = [Pin(10, Pin.OUT), Pin(11, Pin.OUT),
        Pin(12, Pin.OUT), Pin(13, Pin.OUT)]

cols = [Pin(14, Pin.IN, Pin.PULL_DOWN),
        Pin(20, Pin.IN, Pin.PULL_DOWN),
        Pin(16, Pin.IN, Pin.PULL_DOWN),
        Pin(17, Pin.IN, Pin.PULL_DOWN)]

keys = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']
]

# ---------------- ACCELEROMETER ----------------
accel = ADC(26)

# ---------------- OUTPUTS ----------------
buzzer = Pin(21, Pin.OUT)
relay = Pin(22, Pin.OUT)

# ---------------- SERVO ----------------
servo = PWM(Pin(15))
servo.freq(50)

def set_angle(angle):
    duty = int(1638 + (angle / 180) * 8192)
    servo.duty_u16(duty)

set_angle(0)

# ---------------- GLOBAL ----------------
PASSWORD_CORRECT = "1346"
entered = ""
wrong_attempts = 0
lockdown = False
last_cloud_time = 0

# ---------------- CLOUD FUNCTION ----------------

def send_event(event, severity):
    global last_cloud_time

    # Respect ThingSpeak 15 sec rule
    if time.time() - last_cloud_time < 15:
        return

    try:
        url = "https://api.thingspeak.com/update"
        payload = "api_key={}&field1={}&field2={}".format(API_KEY, event, severity)

        response = urequests.post(url, data=payload)

        if response.status_code == 200:
            print("Cloud:", event, severity)
            last_cloud_time = time.time()
        else:
            print("HTTP Error:", response.status_code)

        response.close()

    except Exception as e:
        print("Cloud Error:", e)

# ---------------- FUNCTIONS ----------------

def servo_unlock():
    display("Unlocking...")
    set_angle(90)
    time.sleep(2)
    set_angle(0)
    display("Locked")

def buzzer_pattern(mode):
    if mode == "success":
        buzzer.high(); time.sleep(0.2); buzzer.low()

    elif mode == "error":
        for _ in range(3):
            buzzer.high(); time.sleep(0.2)
            buzzer.low(); time.sleep(0.2)

    elif mode == "alarm":
        for _ in range(10):
            buzzer.high(); time.sleep(0.1)
            buzzer.low(); time.sleep(0.1)

def read_rfid():
    rfid.init()
    (status, _) = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        (status, uid) = rfid.SelectTagSN()
        if status == rfid.OK:
            return int.from_bytes(bytes(uid), "little")
    return None

def read_keypad():
    global entered
    for i in range(4):
        for r in rows:
            r.low()
        rows[i].high()

        for j in range(4):
            if cols[j].value():
                key = keys[i][j]
                time.sleep(0.25)

                if key.isdigit():
                    entered += key
                    display("*" * len(entered))

                elif key == '#':
                    temp = entered
                    entered = ""
                    return temp

                elif key == '*':
                    entered = ""
                    display("Cleared")
    return None

def detect_intrusion():
    global lockdown
    display("Monitoring...")

    for _ in range(30):
        val = accel.read_u16()
        print("Accel:", val)

        if val > 60000 or val < 10000:
            display("BREAK-IN ALERT")
            send_event(5, 5)

            relay.high()
            buzzer_pattern("alarm")

            lockdown = True
            time.sleep(10)

            relay.low()
            return

        time.sleep(0.2)

def reset_system():
    global wrong_attempts, lockdown
    wrong_attempts = 0
    lockdown = False

# ---------------- START ----------------
display("Scan RFID")

# ---------------- MAIN LOOP ----------------

while True:

    if lockdown:
        display("SYSTEM LOCKED")
        time.sleep(5)
        continue

    card = read_rfid()

    if card:

        if card == AUTHORIZED_CARD:
            display("RFID OK")
            send_event(1, 1)

            time.sleep(1)
            display("Enter Password")

            while True:
                pwd = read_keypad()

                if pwd:
                    print("Entered:", pwd)

                    if pwd == PASSWORD_CORRECT:
                        display("ACCESS GRANTED")
                        send_event(2, 1)

                        buzzer_pattern("success")
                        servo_unlock()
                        reset_system()

                        display("Scan RFID")
                        break

                    else:
                        display("WRONG PASSWORD")
                        send_event(3, 2)

                        buzzer_pattern("error")
                        wrong_attempts += 1

                        if wrong_attempts >= 3:
                            detect_intrusion()
                            break

        else:
            display("UNAUTHORIZED")
            send_event(4, 3)

            buzzer_pattern("error")

    time.sleep(1)