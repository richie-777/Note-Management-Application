from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notes', lazy=True))

class NoteVersion(db.Model):
    version_id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create all database tables
with app.app_context():
    db.create_all()

# User registration endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if username or email already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    # Create a new user
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    # Check if username or email exists
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user or user.password != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

# Create a new note endpoint
@app.route('/notes/create', methods=['POST'])
def create_note():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Create a new note
    new_note = Note(title=title, content=content, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()

    # Insert initial version of the note
    new_note_version = NoteVersion(note_id=new_note.id, content=content, timestamp=datetime.now(), user_id=user_id)
    db.session.add(new_note_version)
    db.session.commit()

    return jsonify({'message': 'Note created successfully'}), 201

# Update an existing note endpoint
@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.json
    content = data.get('content')

    note = Note.query.get(id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Update the note content
    note.content = content
    db.session.commit()

    # Insert new version of the note
    new_note_version = NoteVersion(note_id=id, content=content, timestamp=datetime.now(), user_id=note.user_id)
    db.session.add(new_note_version)
    db.session.commit()
    
    return jsonify({'message': 'Note updated successfully'}), 200

# Retrieve a specific note endpoint
@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Check if the user has access to the note
    # You need to implement the logic for user access based on authentication
    # For simplicity, let's assume the user has access to all notes
    return jsonify({'title': note.title, 'content': note.content}), 200

# Share a note with other users endpoint
@app.route('/notes/share', methods=['POST'])
def share_note():
    data = request.json
    note_id = data.get('note_id')
    user_ids = data.get('user_ids')  # List of user IDs to share the note with

    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Share the note with the specified users
    for user_id in user_ids:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404

        # Update the user_id field of the note
        note.user_id = user_id

    db.session.commit()
    return jsonify({'message': 'Note shared successfully'}), 200

# Get the version history of a note endpoint
@app.route('/notes/version-history/<int:id>', methods=['GET'])
def get_note_version_history(id):
    note_versions = NoteVersion.query.filter_by(note_id=id).order_by(NoteVersion.timestamp.desc()).all()
    if not note_versions:
        return jsonify({'error': 'Version history not found for this note'}), 404

    version_history = []
    for version in note_versions:
        version_info = {
            'version_id': version.version_id,
            'content': version.content,
            'timestamp': version.timestamp,
            'user_id': version.user_id
        }
        version_history.append(version_info)

    return jsonify({'version_history': version_history}), 200

# Delete a note endpoint
@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
