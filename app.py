from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import text
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ──────────────────────────────────────────────
# MODEL
# ──────────────────────────────────────────────
class Task(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, default='')
    done         = db.Column(db.Boolean, default=False)
    deadline     = db.Column(db.Date, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'


def parse_deadline(value):
    if not value:
        return None
    if isinstance(value, str):
        return datetime.strptime(value, '%Y-%m-%d').date()
    return value


def should_hide_task(task, current_time=None):
    if not task.done or not task.completed_at:
        return False
    current_time = current_time or datetime.utcnow()
    return current_time - task.completed_at > timedelta(days=30)


def get_visible_tasks(tasks, current_time=None):
    current_time = current_time or datetime.utcnow()
    return [task for task in tasks if not should_hide_task(task, current_time)]

# ──────────────────────────────────────────────
# ROUTES  (CRUD)
# ──────────────────────────────────────────────

@app.route('/')
def index():
    filter_by = request.args.get('filter', 'all')   # all | active | done | hidden
    current_time = datetime.utcnow()
    all_tasks = Task.query.order_by(Task.created_at.desc()).all()

    visible_tasks = []
    hidden_tasks = []
    for task in all_tasks:
        if should_hide_task(task, current_time):
            hidden_tasks.append(task)
        else:
            visible_tasks.append(task)

    if filter_by == 'active':
        tasks = [task for task in visible_tasks if not task.done]
    elif filter_by == 'done':
        tasks = [task for task in visible_tasks if task.done]
    elif filter_by == 'hidden':
        tasks = hidden_tasks
    else:
        tasks = visible_tasks

    total = len(tasks)
    active = sum(1 for task in tasks if not task.done)
    done = sum(1 for task in tasks if task.done)
    hidden_count = len(hidden_tasks)

    return render_template('index.html',
                           tasks=tasks,
                           filter_by=filter_by,
                           total=total,
                           active=active,
                           done=done,
                           hidden_count=hidden_count,
                           now=datetime.now())


# CREATE
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if not title:
        flash('Judul tugas tidak boleh kosong!', 'error')
        return redirect(url_for('index'))

    deadline = parse_deadline(request.form.get('deadline', '').strip())
    task = Task(title=title, description=description, deadline=deadline)
    db.session.add(task)
    db.session.commit()
    flash(f'Tugas "{title}" berhasil ditambahkan!', 'success')
    return redirect(url_for('index'))


# UPDATE — toggle selesai/belum
@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    task.completed_at = datetime.utcnow() if task.done else None
    db.session.commit()
    status = 'selesai' if task.done else 'aktif'
    flash(f'Tugas "{task.title}" ditandai sebagai {status}.', 'success')
    return redirect(url_for('index', filter=request.args.get('filter', 'all')))


# UPDATE — edit judul & deskripsi
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            flash('Judul tugas tidak boleh kosong!', 'error')
            return redirect(url_for('edit_task', task_id=task_id))

        deadline = parse_deadline(request.form.get('deadline', '').strip())
        task.title = title
        task.description = description
        task.deadline = deadline
        db.session.commit()
        flash(f'Tugas berhasil diperbarui!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)


# DELETE
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    flash(f'Tugas "{title}" berhasil dihapus.', 'success')
    return redirect(url_for('index', filter=request.args.get('filter', 'all')))


# ──────────────────────────────────────────────
# INIT DB & RUN
# ──────────────────────────────────────────────

with app.app_context():
    db.create_all()
    inspector = db.inspect(db.engine)
    columns = {column['name'] for column in inspector.get_columns('task')}
    with db.engine.connect() as conn:
        if 'deadline' not in columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN deadline DATE"))
        if 'completed_at' not in columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN completed_at DATETIME"))
        conn.commit()

if __name__ == '__main__':
    app.run(debug=True)