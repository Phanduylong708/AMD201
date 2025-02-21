# Cài venv và cài thư viện trong requirements.txt

# Tạo database mới

1. Mở DBeaver và kết nối tới server database của bạn (ví dụ: localhost).
2. Nhấp chuột phải vào kết nối đó và chọn "Create New Database".
3. Nhập tên database `rideshare` (cho nhất quán) sau đó nhấn OK
4. Refresh (F5) lại 

# Kết nối database

1. Vào file services\user\src\data\init.py
2. Đổi username và password (kiếm file init.py trong folder trên lớp copy qua cũng được). Nhớ để database = "rideshare"
3. Mở file .env (cái này để chạy token)
4. Đổi DATABASE_URL theo đúng thông tin kết nối của bạn, SECRET_KEY là dãy bất kỳ (ví dụ: 123)
   Giả sử thông tin kết nối là:
    - User: postgres
    - Password: 123
    - Host: localhost
    - Port: 5432
    - Database: rideshare
    Thì nhập .env là:
    DATABASE_URL=postgresql://postgres:123@localhost:5432/rideshare
    SECRET_KEY=123 
5. Cd đến thư mục services\user và chạy python main.py. Mở localhost:8001/docs rồi test

# Test ?
1. Create User
2. Post Token nhập tk mk vừa tạo vào, xong copy token (trong giấu "")
3. Bấm nút Authorize rồi nhập token 
4. Test Auth Status thành công thì test các tính năng còn lại
5. Mở DBeaver coi có data chưa, có thì xong

# Lỗi ?
1. Làm hết rồi mà không thấy database trong DBeaver ?
    - Bấm New Database Connection góc trái màn hình
    - Chọn PostgreSQL
    - Ô database nhập rideshare
    - Username, password thì như cũ
    - Test Connection ok thì finish
    - Bấm database -> rideshare -> tables -> public -> users