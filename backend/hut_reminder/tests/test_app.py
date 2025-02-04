import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test method."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_app(self):
        """Test app creation and configuration."""
        self.assertIsInstance(self.app, Flask)
        self.assertEqual(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        self.assertTrue('sqlite' in self.app.config['SQLALCHEMY_DATABASE_URI'])


    def test_home_route(self):
        """Test the home route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Hello, Flask!")

    def test_error_handling(self):
        """Test 404 error handling."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    @patch('app.db.create_all')
    def test_db_creation_error(self, mock_create_all):
        """Test database creation error handling."""
        mock_create_all.side_effect = Exception("Database error")
        
        with self.assertRaises(Exception):
            create_app()

    def test_config_values(self):
        """Test configuration values."""
        test_app = create_app()
        self.assertEqual(test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        self.assertTrue(test_app.config['SQLALCHEMY_DATABASE_URI'].endswith('hut_reminder.db'))
