import unittest
import json
from test import app, db, User, Note, NoteVersion

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        with app.app_context():
            data = {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'password123'
            }
            response = self.app.post('/signup', json=data)
            self.assertEqual(response.status_code, 201)

    def test_login(self):
        with app.app_context():
            user = User(username='test_user', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            data = {
                'username_or_email': 'test@example.com',
                'password': 'password123'
            }
            response = self.app.post('/login', json=data)
            self.assertEqual(response.status_code, 200)

    def test_create_note(self):
        with app.app_context():
            user = User(username='test_user', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            data = {
                'title': 'Test Note',
                'content': 'This is a test note',
                'user_id': user.id
            }
            response = self.app.post('/notes/create', json=data)
            self.assertEqual(response.status_code, 201)

    def test_update_note(self):
        with app.app_context():
            user = User(username='test_user', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            note = Note(title='Test Note', content='This is a test note', user_id=user.id)
            db.session.add(note)
            db.session.commit()

            data = {
                'content': 'Updated test note content'
            }
            response = self.app.put(f'/notes/{note.id}', json=data)
            self.assertEqual(response.status_code, 200)

    def test_get_note(self):
        with app.app_context():
            user = User(username='test_user', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            note = Note(title='Test Note', content='This is a test note', user_id=user.id)
            db.session.add(note)
            db.session.commit()

            response = self.app.get(f'/notes/{note.id}')
            self.assertEqual(response.status_code, 200)

    def test_share_note(self):
        with app.app_context():
            user1 = User(username='user1', email='user1@example.com', password='password123')
            user2 = User(username='user2', email='user2@example.com', password='password456')
            db.session.add_all([user1, user2])
            db.session.commit()

            note = Note(title='Test Note', content='This is a test note', user_id=user1.id)
            db.session.add(note)
            db.session.commit()

            data = {
                'note_id': note.id,
                'user_ids': [user2.id]
            }
            response = self.app.post('/notes/share', json=data)
            self.assertEqual(response.status_code, 200)

    def test_get_note_version_history(self):
        with app.app_context():
            user = User(username='test_user', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            note = Note(title='Test Note', content='This is a test note', user_id=user.id)
            db.session.add(note)
            db.session.commit()

            # Create a note version
            note_version = NoteVersion(note_id=note.id, content='Initial version', user_id=user.id)
            db.session.add(note_version)
            db.session.commit()

            response = self.app.get(f'/notes/version-history/{note.id}')
            self.assertEqual(response.status_code, 200)

    def test_delete_note(self):
        with app.app_context():
            user = User(username='test_user', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()

            note = Note(title='Test Note', content='This is a test note', user_id=user.id)
            db.session.add(note)
            db.session.commit()

            response = self.app.delete(f'/notes/{note.id}')
            self.assertEqual(response.status_code, 200)
        
            # Check if note is actually deleted
            deleted_note = Note.query.get(note.id)
            self.assertIsNone(deleted_note)

if __name__ == '__main__':
    unittest.main()
