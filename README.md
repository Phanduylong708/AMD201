# Ride Sharing System

A FastAPI-based microservices system for ride sharing, developed as part of the AMD201 Advanced Microservice Development and Deployment coursework.

## Project Structure

```
Coursework/
├── api-gateway/          # API Gateway service
├── services/            
│   ├── user/            # User management service
│   ├── rider/           # Rider management service
│   ├── booking/         # Booking management service
│   └── ride-matching/   # Ride matching service
├── docs/                # Documentation and C4 diagrams
└── requirements.txt     # Project dependencies
```

## Services Overview

1. **User Service**: Handles user authentication and profile management
2. **Rider Service**: Manages rider profiles and availability
3. **Booking Service**: Handles ride requests and fare calculation
4. **Ride Matching Service**: Implements rider matching logic
5. **API Gateway**: Central entry point for all client requests

## Git Guide

### Bước 1: Cài đặt các công cụ cần thiết

1. **Cài đặt Git**:
   - Truy cập [https://git-scm.com/downloads](https://git-scm.com/downloads)
   - Tải phiên bản phù hợp với máy của bạn (Windows/Mac/Linux)
   - Chạy file cài đặt, click Next và để các tùy chọn mặc định

2. **Cài đặt Visual Studio Code**:
   - Truy cập [https://code.visualstudio.com/](https://code.visualstudio.com/)
   - Tải VS Code phiên bản phù hợp với máy của bạn
   - Cài đặt và khởi động VS Code


### Bước 2: Cấu hình Git (chỉ làm 1 lần đầu)

1. **Mở Terminal trong VS Code**:
   - Mở VS Code
   - Nhấn `Ctrl + `` (phím nằm dưới Esc)
   - Hoặc vào menu View → Terminal

2. **Cấu hình thông tin Git**:
   ```bash
   git config --global user.name "Tên của bạn"
   git config --global user.email "email@example.com"
   ```

### Bước 3: Tải dự án về máy

1. **Tạo thư mục cho dự án**:
   - Mở File Explorer
   - Tạo một thư mục mới (ví dụ: D:\Projects)
   - Click phải trong thư mục → "Open with Code"

2. **Clone dự án**:
   - Trong VS Code, mở Terminal
   - Chạy lệnh:
     ```bash
     git clone [URL của repository]
     cd ride-sharing
     ```
   - Hoặc dùng VS Code GUI:
     1. Nhấn Ctrl+Shift+P
     2. Gõ "Git: Clone"
     3. Dán URL repository
     4. Chọn thư mục vừa tạo

### Bước 4: Cài đặt môi trường Python

1. **Tạo môi trường ảo**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Cài đặt các thư viện**:
   ```bash
   pip install -r requirements.txt
   ```

### Bước 5: Kiểm tra cài đặt

1. **Kiểm tra Git**:
   ```bash
   git --version
   ```

2. **Kiểm tra Python**:
   ```bash
   python --version
   ```

3. **Kiểm tra pip**:
   ```bash
   pip list
   ```

### Quy trình làm việc đơn giản trên main branch

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Team

- [Team Member 1]
- [Team Member 2]
- [Team Member 3]

## Documentation

Detailed documentation including API specifications and architecture diagrams can be found in the `/docs` directory. 