Secure File Sharing System (AES Encryption)

This project is developed as part of Cyber Security Internship - Task 3.
It allows users to securely upload, encrypt, store, and download files using AES-256 encryption.

 Features

 Upload and encrypt any file using AES-256
 Stores encrypted files securely
 Download encrypted files with on-the-fly decryption
 User-friendly interface (Flask + HTML)
 No plaintext stored — full security

 Tech Stack
Component	Technology
Backend	Python Flask
Encryption	AES (Cryptography library)
Frontend	HTML + Bootstrap
Storage	Local file system
 Folder Structure
SecureFileShare_Task3
│── app.py
│── requirements.txt
│── README.md
│
├── templates
│   └── index.html
│
└── files
    └── (encrypted files)

 How to Run
pip install -r requirements.txt
python app.py


Open browser:

 http://127.0.0.1:5000


Encryption Details

Algorithm: AES

Mode: Fernet (AES-256 + HMAC)


Key is securely generated and used for both encryption and decryption.
