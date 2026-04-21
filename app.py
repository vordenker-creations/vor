from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'vku_ai_25gai_secret_key'

def get_db_connection():
    conn = sqlite3.connect('vku_portal.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    user_id = session.get('user_id')
    search_query = request.args.get('q', '')
    conn = get_db_connection()
    
    user_info = None
    if user_id:
        user_info = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if search_query:
        query = f'%{search_query}%'
        featured = conn.execute('SELECT * FROM candidates WHERE is_featured = 1 AND (name LIKE ? OR skills LIKE ?)', (query, query)).fetchall()
        regular = conn.execute('SELECT * FROM candidates WHERE is_featured = 0 AND (name LIKE ? OR skills LIKE ?)', (query, query)).fetchall()
    else:
        featured = conn.execute('SELECT * FROM candidates WHERE is_featured = 1').fetchall()
        regular = conn.execute('SELECT * FROM candidates WHERE is_featured = 0').fetchall()
    
    history_chats = [
        {'name': 'Nguyễn Văn A', 'time': '20:30', 'last_msg': 'Em chào anh ạ'},
        {'name': 'Trần Thị B', 'time': 'Hôm qua', 'last_msg': 'Dạ em cảm ơn'}
    ]
    conn.close()
    return render_template('index.html', user_info=user_info, featured=featured, regular=regular, search_query=search_query, recent_chats=history_chats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            if not user['preferred_industry']:
                return redirect(url_for('onboarding'))
            return redirect(url_for('index'))
            
        
        flash('Sai tài khoản hoặc mật khẩu!', 'danger')
    return render_template('login.html')

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        industry = request.form.get('industry')
        level = request.form.get('level')
        english = request.form.get('english')
        conn = get_db_connection()
        conn.execute('UPDATE users SET preferred_industry = ?, preferred_level = ?, preferred_english = ? WHERE id = ?', 
                     (industry, level, english, session['user_id']))
        conn.commit()
        conn.close()
        
        
        flash('Cảm ơn bạn đã hoàn thành khảo sát!', 'success')
        return redirect(url_for('index'))
    return render_template('onboarding.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fullname = request.form['fullname']
        position = request.form['position']
        company = request.form['company']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        
        
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        
        if existing_user:
            conn.close()
            if existing_user['username'] == username:
                flash('Lỗi: Tên đăng nhập này đã có người sử dụng!', 'danger')
            else:
                flash('Lỗi: Email này đã được đăng ký cho tài khoản khác!', 'danger')
            return redirect(url_for('register'))
            
        try:
            conn.execute('INSERT INTO users (username, password, email, fullname, position, company, phone, address) VALUES (?,?,?,?,?,?,?,?)', 
                         (username, password, email, fullname, position, company, phone, address))
            conn.commit()
            flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Lỗi hệ thống: {str(e)}', 'danger')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    if request.method == 'POST':
        conn.execute('UPDATE users SET bio = ? WHERE id = ?', (request.form.get('bio'), session['user_id']))
        conn.commit()
        flash('Đã lưu mô tả thành công!', 'success')
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', profile_data=user_data)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('INSERT INTO jobs (title, requirements, description, author_id) VALUES (?,?,?,?)',
                     (request.form['job_title'], request.form['job_requirements'], request.form['job_description'], session['user_id']))
        conn.commit()
        conn.close()
        flash('Đã đăng tin tuyển dụng thành công!', 'success')
        return redirect(url_for('index'))
    return render_template('post_job.html', username=session.get('username'))
app.run(debug=True)