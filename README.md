# 🛡️ Smart Two-Factor Access Control System (IoT)

An intelligent IoT-based security system that combines RFID authentication and keypad password verification with intrusion detection using an accelerometer. The system enhances traditional locking mechanisms by adding multi-layer security and real-time monitoring.

---

## 🚀 Features

- 🔐 Two-Factor Authentication (RFID + Password)
- 🚨 Intrusion Detection using Accelerometer
- 🔔 Buzzer Alert System
- 🔌 Relay-based Security Trigger
- 🔁 Servo Motor Door Lock
- 📟 LCD Display for User Interaction
- ☁️ Cloud Logging using ThingSpeak (Event + Severity)

---

## 🧠 System Workflow

1. User scans RFID card  
2. If valid → prompts for password  
3. If password correct → door unlocks  
4. If wrong password (3 attempts):  
   - Accelerometer activates intrusion monitoring  
5. If forced entry detected:  
   - Alarm triggered  
   - Event logged to cloud  

---

## 📊 ThingSpeak Fields

| Field | Description |
|------|------------|
| Field 1 | Event Code |
| Field 2 | Severity Level |

---

## 🔧 Hardware Used

- Raspberry Pi Pico / Pico W  
- MFRC522 RFID Module  
- 4x4 Matrix Keypad  
- Accelerometer (Analog)  
- Servo Motor  
- Buzzer  
- Relay Module  
- I2C LCD (16x2)

---

## 💻 Technologies Used

- MicroPython  
- Embedded Systems  
- SPI, I2C, GPIO  
- IoT (ThingSpeak Cloud)

---

## ⚙️ Setup Instructions

1. Upload required libraries:
   - `mfrc522.py`
   - `pico_i2c_lcd.py`
2. Connect hardware as per circuit diagram  
3. Update WiFi credentials and API key  
4. Run the main Python file  

---

## 🧪 Output

- Displays system status on LCD  
- Controls servo for locking/unlocking  
- Sends security events to cloud  
- Triggers alarm on intrusion  

---

## 🧠 Learning Outcomes

- Multi-sensor integration  
- Embedded system design  
- IoT cloud communication  
- Real-time security system implementation  

---

## 📌 Future Improvements

- Mobile app notifications  
- Face recognition integration  
- Battery backup system  

---

## 👩‍💻 Author

**Sathvika Naik**  
Embedded Systems & IoT Enthusiast
