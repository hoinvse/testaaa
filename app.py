from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

tasks = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/view_attachment/<int:task_index>')
def view_attachment(task_index):
    try:
        task = tasks[task_index]
        attachment_path = task['attachment']

        if attachment_path:
            return send_file(attachment_path, as_attachment=True)

        flash('Không tìm thấy tệp đính kèm.', 'warning')
        return redirect(url_for('index'))

    except IndexError:
        flash('Vui lòng chọn công việc để xem tệp đính kèm.', 'warning')
        return redirect(url_for('index'))
    
@app.route('/')
def index():
    # ... (giữ nguyên code hiện tại)
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = {
        'name': request.form['task'],
        'priority': request.form['priority'],
        'due_date': request.form['due_date'],
        'category': request.form['category'],
        'completed': False,
        'attachment': None  # Đường dẫn tới tệp đính kèm
    }

    attachment = request.files['attachment']
    if attachment:
        filename = secure_filename(attachment.filename)
        attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        attachment.save(attachment_path)
        task['attachment'] = attachment_path

    # Thêm công việc vào danh sách
    if task['name']:
        tasks.append(task)
        flash('Công việc được thêm thành công!', 'success')
    else:
        flash('Công việc không thể để trống!', 'warning')

    return redirect(url_for('index'))


@app.route('/delete_task/<int:task_index>')
def delete_task(task_index):
    try:
        del tasks[task_index]
        flash('Công việc được xóa thành công!', 'success')
    except IndexError:
        flash('Vui lòng chọn công việc để xóa.', 'warning')

    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_index>', methods=['GET', 'POST'])
def edit_task(task_index):
    try:
        task = tasks[task_index]

        if request.method == 'POST':
            updated_task = {
                'name': request.form['task'],
                'priority': request.form['priority'],
                'due_date': request.form['due_date'],
                'category': request.form['category'],
                'completed': task['completed']
            }
            
            tasks[task_index] = updated_task
            flash('Công việc được cập nhật thành công!', 'success')
            return redirect(url_for('index'))

        return render_template('edit_task.html', task=task, task_index=task_index)
    except IndexError:
        flash('Vui lòng chọn công việc để chỉnh sửa.', 'warning')
        return redirect(url_for('index'))

def sap_xep_cong_viec_theo_uu_tien():
    return sorted(tasks, key=lambda x: x['priority'])

def loc_cong_viec_theo_danh_muc(danh_muc):
    return [task for task in tasks if task['category'] == danh_muc]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
