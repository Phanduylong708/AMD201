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

2. **Cài đặt Visual Studio Code**:
   - Truy cập [https://code.visualstudio.com/](https://code.visualstudio.com/)
   - Tải VS Code phiên bản phù hợp với máy của bạn
   - Cài đặt và khởi động VS Code

3. **Cài đặt Python**:
   - Truy cập [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Tải Python phiên bản mới nhất (chọn Windows installer 64-bit)
   - Khi cài đặt, **nhớ tích vào ô "Add Python to PATH"**
   - Click Install Now

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

### Quy trình làm việc hàng ngày

1. **Bắt đầu ngày làm việc**:
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

### Các thao tác Git khác trong VS Code

1. **Xem lịch sử commit**:
   - Click vào dấu ⋯ → "View History"
   - Hoặc cài extension "Git History" để xem trực quan hơn

2. **Hoàn tác thay đổi**:
   - Click phải vào file → "Discard Changes"
   - Hoặc click vào dấu ↺ bên cạnh file

3. **So sánh thay đổi**:
   - Click phải vào file → "Compare with Saved"
   - Hoặc click đúp vào file trong Source Control

### Lưu ý quan trọng khi làm việc

- LUÔN pull code mới nhất trước khi bắt đầu làm việc
- LUÔN pull lại trước khi push để tránh conflict
- Thêm tên bạn vào commit message để dễ theo dõi
- Commit thường xuyên và với message rõ ràng
- Nếu không chắc chắn về thay đổi nào, hãy thảo luận với team
- Thông báo cho team khi bạn đang thay đổi một file quan trọng
- Backup code locally trước khi thực hiện các thay đổi lớn

## Development Team

- [Team Member 1]
- [Team Member 2]
- [Team Member 3]

## Documentation

Detailed documentation including API specifications and architecture diagrams can be found in the `/docs` directory. 