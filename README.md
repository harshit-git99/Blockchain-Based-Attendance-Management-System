# Blockchain-Based Attendance Management System (Python)

This project is a **console-based Blockchain Attendance Management System** implemented in pure Python (standard library only). It uses blockchain concepts such as hashing, block linking, and immutability to securely store attendance records.

---

## 🚀 Features

- Blockchain implementation with SHA-256 hashing
- Immutable attendance records (per run)
- Add new attendance entries
- View all attendance records
- Verify blockchain integrity
- Console-based menu system

---

## 🛠 Technologies Used

- Python 3.x
- Standard Python Libraries:
  - `hashlib`
  - `json`
  - `time`

---

## 📁 Project Structure

```
attendance_blockchain.py
README.md
requirements.txt
```

---

## ▶ How to Run (Console)

1. Make sure Python 3 is installed.
2. Navigate to the project directory.
3. Run the program:

```bash
python attendance_blockchain.py
```

---

## ▶ How to Run (Web UI)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
python server.py
```

3. Open in browser:

- http://127.0.0.1:5000


---

## 📜 Menu Options

```
1. Mark Attendance
2. View Attendance Records
3. Verify Blockchain
4. Exit
```

---

## 🔐 Blockchain Security

Each attendance entry is stored in a block that contains:
- Index
- Timestamp
- Attendance Data
- Current Hash
- Previous Hash

Blocks are cryptographically linked; verification recalculates each hash and checks the chain linkage.

---

## 🧠 Future Enhancements

- Persist data to a file/database
- Web Interface (Flask/Django)
- QR Code Attendance
- Face Recognition
- Admin & Student Login
- Export to Excel
- Real Mining (Proof of Work)

---

## 📄 Dependencies

- Console version uses **Python standard library only**.
- Flask web UI uses **Flask** (see `requirements.txt`).

---
