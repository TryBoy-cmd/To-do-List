from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    done       = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

# ──────────────────────────────────────────────
# ROUTES  (CRUD)
# ──────────────────────────────────────────────

@app.route('/')
def index():
    filter_by = request.args.get('filter', 'all')   # all | active | done
    if filter_by == 'active':
        tasks = Task.query.filter_by(done=False).order_by(Task.created_at.desc()).all()
    elif filter_by == 'done':
        tasks = Task.query.filter_by(done=True).order_by(Task.created_at.desc()).all()
    else:
        tasks = Task.query.order_by(Task.created_at.desc()).all()

    total  = Task.query.count()
    active = Task.query.filter_by(done=False).count()
    done   = Task.query.filter_by(done=True).count()

    return render_template('index.html',
                           tasks=tasks,
                           filter_by=filter_by,
                           total=total,
                           active=active,
                           done=done,
                           now=datetime.now())


# CREATE
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if not title:
        flash('Judul tugas tidak boleh kosong!', 'error')
        return redirect(url_for('index'))

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    flash(f'Tugas "{title}" berhasil ditambahkan!', 'success')
    return redirect(url_for('index'))


# UPDATE — toggle selesai/belum
@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
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

        task.title = title
        task.description = description
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


# DELETE ALL done tasks
@app.route('/clear-done', methods=['POST'])
def clear_done():
    count = Task.query.filter_by(done=True).delete()
    db.session.commit()
    flash(f'{count} tugas selesai berhasil dihapus.', 'success')
    return redirect(url_for('index'))


# ──────────────────────────────────────────────
# INIT DB & RUN
# ──────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)