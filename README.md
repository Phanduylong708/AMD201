# Ride Sharing System

A FastAPI-based microservices system for ride sharing, developed as part of the AMD201 Advanced Microservice Development and Deployment coursework.

## Project Structure

```
ride-sharing/
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

2. **Kiểm tra Git**:
   ```bash
   git --version
   ```

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

### Cách sài

1. **Lấy code mới nhất**:
   - Terminal:
     ```bash
     # Luôn cập nhật code mới nhất trước khi bắt đầu
     git pull origin main
     ```
   - VS Code GUI:
     1. Click vào biểu tượng Source Control (Ctrl+Shift+G)
     2. Click vào dấu ⋯ (3 chấm)
     3. Chọn "Pull"

2. **Trong quá trình làm việc**:

   a. **Kiểm tra thay đổi**:
   - Terminal: `git status`
   - VS Code GUI:
     1. Click vào Source Control
     2. Xem danh sách file thay đổi ở mục "Changes"

   b. **Xem chi tiết thay đổi**:
   - Terminal: `git diff`
   - VS Code GUI:
     1. Click vào file trong mục "Changes"
     2. VS Code sẽ hiển thị những thay đổi với màu sắc trực quan

   c. **Thêm file đã thay đổi để commit**:
   - Terminal: `git add .`
   - VS Code GUI:
     1. Click dấu + bên cạnh mỗi file để stage từng file
     2. Hoặc click dấu + bên cạnh mục "Changes" để stage tất cả

   d. **Commit thay đổi với mô tả rõ ràng**:
   - Terminal: `git commit -m "[Tên bạn] - Mô tả những gì bạn đã làm"`
   - VS Code GUI:
     1. Nhập mô tả commit vào ô "Message"
     2. Nhấn Ctrl+Enter hoặc click dấu ✓ để commit

   e. **Tải code mới về (phòng trường hợp có người khác đã push code lên)**:
   - Terminal: `git pull origin main`
   - VS Code GUI:
     1. Click vào dấu ⋯ (3 chấm)
     2. Chọn "Pull"

   f. **Đẩy code lên**:
   - Terminal: `git push origin main`
   - VS Code GUI:
     1. Click vào dấu ⋯ (3 chấm)
     2. Chọn "Push"
     3. Hoặc click vào biểu tượng "Sync Changes" (hai mũi tên tròn) để pull và push cùng lúc

### Xử lý khi có conflict

1. **Khi có conflict, VS Code sẽ hiển thị trực quan**:
   - File có conflict sẽ được đánh dấu (C)
   - Mở file, các đoạn conflict sẽ được highlight
   - VS Code hiển thị các lựa chọn ngay trên code:
     * "Accept Current Change" (giữ code của bạn)
     * "Accept Incoming Change" (lấy code mới về)
     * "Accept Both Changes" (giữ cả hai)
     * "Compare Changes" (so sánh các thay đổi)

2. **Sau khi giải quyết conflict**:
   - Terminal:
     ```bash
     git add .
     git commit -m "[Tên bạn] - Resolve conflict"
     git push origin main
     ```
   - VS Code GUI:
     1. Các file đã resolve sẽ tự động được stage
     2. Nhập message "Resolve conflict"
     3. Click dấu ✓ để commit
     4. Click "Sync Changes" để push

3. **.gitignore**:
   - File này chứa các file và thư mục mà Git sẽ không theo dõi
   - Các file này sẽ không được commit lên
   - Để thêm file vào .gitignore, chỉ cần thêm tên file (vd: howtorun.md, docs/)

## Development Team

- [Team Member 1]
- [Team Member 2]
- [Team Member 3]
