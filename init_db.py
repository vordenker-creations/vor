import sqlite3
import os

def init_db():
    db_name = 'vku_portal.db'
    
    # Bước 1: Cố gắng xóa hẳn file vật lý
    try:
        if os.path.exists(db_name):
            os.remove(db_name)
            print("Đã xóa file DB cũ...")
    except Exception as e:
        print(f"⚠️ Cảnh báo: Không thể xóa file do Server đang chạy. Hệ thống sẽ cưỡng chế làm sạch dữ liệu bên trong...")

    # Bước 2: Kết nối và cưỡng chế xóa sạch các bảng cũ (Nếu Bước 1 thất bại)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS jobs')
    cursor.execute('DROP TABLE IF EXISTS candidates')
    cursor.execute('DROP TABLE IF EXISTS users')

    # Bước 3: Tạo lại cấu trúc mới nhất
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            fullname TEXT,
            position TEXT,
            company TEXT,
            phone TEXT,
            address TEXT,
            bio TEXT,
            preferred_industry TEXT,
            preferred_level TEXT,
            preferred_english TEXT,
            avatar TEXT,
            last_username_change TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT,
            class_name TEXT,
            is_featured INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            requirements TEXT,
            description TEXT,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')

    # Nạp dữ liệu mẫu ứng viên
    sample_candidates = [
        ('Nguyễn Văn A', 'Java Swing, SQL Server', '25GAI', 1),
        ('Trần Thị B', 'Python, AI, Data Analysis', '25GAI', 1),
        ('Henry247', 'Python, Flask, AI Major', '25GAI', 1),
        ('Lê Văn C', 'Web Design, Bootstrap', '25GAI', 0),
        ('Phạm Thị D', 'Machine Learning, Deep Learning', '25GAI', 0),
        ('Nguyễn Hoàng Nam', 'C++, Embedded Systems', '25GAI', 0)
    ]
    cursor.executemany('INSERT INTO candidates (name, skills, class_name, is_featured) VALUES (?, ?, ?, ?)', sample_candidates)

    conn.commit()
    conn.close()
    print("✅ Đã khởi tạo và làm sạch Database thành công!")

if __name__ == '__main__':
    init_db()