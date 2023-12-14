from flask import request, jsonify, render_template
from notlar import app, db
from notlar.models import User, Note
from datetime import datetime
from flask import redirect, url_for
from . import login_manager, current_user
from sqlalchemy import desc


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(500)
@app.errorhandler(400)
def internal_server_error(error):
    return render_template('error.html'), error.code


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), error.code


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_notes_management'))
    return render_template('index.html')


@app.route('/dashboard_notes_management', methods=['GET'])
def dashboard_notes_management():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    current_date_time = datetime.now()
    today_formatted_date = current_date_time.strftime('%d/%m/%Y')
    return render_template(
        'dashboard_notes_management.html',
        user_email=current_user.email,
        user_name=current_user.name,
        todays_date=today_formatted_date
    ), 200


@app.route('/dashboard_all_notes', methods=['GET'])
def dashboard_all_notes():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    return render_template(
        'dashboard_all_notes.html',
        user_email=current_user.email,
        user_name=current_user.name
    ), 200


@app.route('/dashboard_home', methods=['GET'])
def dashboard_home():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    return render_template(
        'dashboard_home.html',
        user_email=current_user.email,
        user_name=current_user.name
    ), 200


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/kanban', methods=['GET'])
def kanban():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    return render_template(
        'kanban.html'
    ), 200


@app.route('/settings', methods=['GET'])
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    return render_template('settings.html'), 200


@app.route('/get_notes', methods=['GET'])
def get_notes():
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    date_str = request.args.get('date')
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    notes = Note.query.filter_by(user_id=current_user.id, created_at=selected_date).all()

    notes_data = [
        {
            "date": note.created_at.strftime('%Y-%m-%d'),
            "content": note.text,
            "number": note.id,
            "color": note.color
        } for note in notes]
    return jsonify(notes_data), 200


@app.route('/all_notes', methods=['GET'])
def list_notes_by_date_range():
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    query = Note.query.filter_by(user_id=current_user.id)

    if start_date and end_date:
        query = query.filter(Note.created_at >= start_date, Note.created_at <= end_date)
    elif start_date:
        query = query.filter(Note.created_at >= start_date)
    elif end_date:
        query = query.filter(Note.created_at <= end_date)

    query = query.order_by(desc(Note.created_at))

    notes = query.all()

    notes_data = [
        {
            "date": note.created_at.strftime('%Y-%m-%d'),
            "content": note.text,
            "number": note.id,
            "color": note.color
        } for note in notes]

    return jsonify(notes_data), 200


@app.route('/create_note', methods=['POST'])
def create_note():
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    data = request.json
    title = data.get('title', '')
    text = data.get('text', '')

    # Let's keep like this since we don't handle colors yet
    color = data.get('color', '#FFFFFF')

    created_at = datetime.strptime(data.get('created_at'), '%Y-%m-%d').date()

    new_note = Note(title=title, text=text, color=color, user=current_user, created_at=created_at)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({"message": "Note created successfully"}), 201


@app.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note deleted successfully"}), 200
    else:
        return jsonify({"error": "Note not found or unauthorized"}), 404
