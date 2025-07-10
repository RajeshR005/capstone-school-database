# 🏫 Capstone School Database

![Banner](https://capsule-render.vercel.app/api?type=waving\&color=0db1ff\&height=200\&text=Capstone%20School%20Database\&fontAlignY=35\&fontSize=40\&desc=A%20Full-fledged%20Backend%20for%20School%20Management\&descSize=20)

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-success?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</p>

---

## 🎯 Project Overview

This is a **real-world Capstone Backend Project** for managing school data. It’s built with 🔥 FastAPI, 🚀 SQLAlchemy, and 🧠 Alembic to deliver a professional and scalable REST API solution.

> ✅ Role-based authentication
> ✅ Admin-only master management
> ✅ PDF question upload system
> ✅ Secure and modular design

---

## 📁 Folder Structure

```bash
capstone-school-database/
├── backend/
│   └── app/
│       ├── alembic/                  # DB migrations
│       │   └── versions/
│       ├── app/
│       │   ├── api/
│       │   │   └── endpoints/        # Common endpoints for all users
│       │   ├── core/                 # Config & Security
│       │   ├── crud/                 # Admin-only master CRUDs
│       │   ├── db/                   # DB session, base class
│       │   ├── models/               # SQLAlchemy models
│       │   ├── schemas/              # Pydantic schemas
├── uploads/
│   └── questions/                    # Uploaded PDF question files
├── requirements.txt
└── README.md
```

---

## 🔧 Technology Stack

* 🚀 **FastAPI** — web framework
* 🔄 **SQLAlchemy** — ORM
* 📦 **Alembic** — DB migrations
* 📑 **Pydantic** — data validation
* 🔐 **JWT Auth** — secure login
* 🗃️ **Database** — MySQL 

---

## ⚙️ Installation Guide

```bash
# Clone the repository
git clone https://github.com/RajeshR005/capstone-school-database.git
cd capstone-school-database/backend/app

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install all required packages
pip install -r ../../requirements.txt

# Run Alembic migrations
alembic upgrade head

# Launch the FastAPI server
uvicorn app.app.main:app --reload
```

---

## 🔐 Authentication Endpoints (No Register)

| Endpoint                               | Description     |
| -------------------------------------- | --------------- |
| `POST /Authentication/user_login`      | Login User      |
| `POST /Authentication/user_logout`     | Log Out         |
| `POST /Authentication/change_password` | Change Password |
| `POST /Authentication/forgot_password` | Forgot Password |
| `POST /Authentication/verify_otp`      | Verify OTP      |
| `POST /Authentication/reset-password`  | Reset Password  |
| `POST /Authentication/resend-otp`      | Resend OTP      |
| `POST /Authentication/validate_token`  | Validate Token  |



---

## 🔐 Admin-Only Endpoints (from `crud/` folder)

These files contain master data management, accessible only to **Admin users**:

```python
class_academic_crud.py
classroom_crud.py
exam_alloc_crud.py
exam_crud.py
group_crud.py
section_crud.py
standard_crud.py
student_class_crud.py
subject_alloc_crud.py
subject_crud.py
term_crud.py
```

---

## 👥 Common User Endpoints (from `endpoints/`)

These endpoints are accessible to all user roles (Admin, Staff, Principal, etc.):

```python
attendance.py
event.py
forgot_password.py
leave_crud.py
login.py
mark_crud.py
principal.py
question_crud.py
staff.py
```

---

## 📄 PDF Question Upload System

| Feature          | Description                        |
| ---------------- | ---------------------------------- |
| Upload Endpoint  | `POST /Questions/upload/questions` |
| File Type        | `.pdf` only                        |
| Storage Location | `uploads/questions/`               |

🧪 Sample cURL:

```bash
curl -X POST \
  -F "file=@sample_questions.pdf" \
  http://127.0.0.1:8000/Questions/upload/questions
```

You can also view, edit, download, and toggle status of question files using other `/Questions/` endpoints.

---


![Swagger Demo](https://user-images.githubusercontent.com/99156235/152717720-d3b3db5d-68a9-4207-b27e-d9eac2966011.gif)

---

## 💬 Contributing

🙌 Pull Requests are always welcome!

```bash
# 1. Fork this repo
# 2. Create your feature branch
git checkout -b feature/amazing-feature

# 3. Make changes, commit
git commit -m "Add amazing feature"

# 4. Push to origin
git push origin feature/amazing-feature

# 5. Create a Pull Request
```

---

## 📜 License

This project is released under the **MIT License**.
Feel free to build on top of it with credits 🙏

---

### ✨ Author Info

Made with ❤️ by [Rajesh R](https://www.linkedin.com/in/rajeshradha)
Follow me on GitHub: [RajeshR005](https://github.com/RajeshR005)

---

> ⚡ “Empowering digital classrooms, one API at a time.”
> — Capstone Project by Rajesh R, 2025
