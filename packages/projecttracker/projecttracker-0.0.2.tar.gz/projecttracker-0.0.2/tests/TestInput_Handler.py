import unittest
from unittest.mock import patch
from projecttracker.utils.input_handler import (
    get_user_choice,
    get_project_input,
    get_task_input,
    get_projectID_input,
    get_priority_input,
    get_duration_input,
    get_comments_input,
    get_assigned_input,
    get_start_date_input,
    get_deadline_input,
    get_owner_input,
    get_project_task_id,
    any_key_continue,
    get_file_path,
)

class TestInput_Handler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up class...")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down class...")

    def setUp(self):
        print("Setting up test...")

    def tearDown(self):
        print("Tearing down test...")

    def test_get_user_choice_valid_input(self):
        with patch("builtins.input", return_value="1"):
            user_choice = get_user_choice()
            self.assertEqual(user_choice, 1)
            self.assertIsInstance(user_choice, int)
            self.assertGreaterEqual(user_choice, 0)
            self.assertLessEqual(user_choice, 9)
    
    def test_get_project_input(self):
        with patch("builtins.input", return_value="ProjectX"):
            project_name = get_project_input()
            self.assertEqual(project_name, "ProjectX")
            self.assertIsInstance(project_name, str)
            self.assertNotEqual(project_name, "")
            self.assertRegex(project_name, r"\w+")

        with patch("builtins.input", return_value=""):
            project_name = get_project_input()
            self.assertEqual(project_name, "")
            self.assertIsInstance(project_name, str)
            self.assertEqual(project_name, "")
            self.assertNotRegex(project_name, r"\w+")
    
    def test_get_task_input(self):
        with patch("builtins.input", return_value="TaskY"):
            task_name = get_task_input()
            self.assertEqual(task_name, "TaskY")
            self.assertIsInstance(task_name, str)
            self.assertNotEqual(task_name, "")
            self.assertRegex(task_name, r"\w+")

        with patch("builtins.input", return_value=""):
            task_name = get_task_input()
            self.assertEqual(task_name, "")
            self.assertIsInstance(task_name, str)
            self.assertEqual(task_name, "")
            self.assertNotRegex(task_name, r"\w+")
    
    def test_get_projectID_input(self):
        with patch("builtins.input", return_value="P123"):
            project_id = get_projectID_input()
            self.assertEqual(project_id, "P123")
            self.assertIsInstance(project_id, str)
            self.assertNotEqual(project_id, "")
            self.assertRegex(project_id, r"\w+")
    
    def test_get_priority_input_valid_input(self):
        with patch("builtins.input", return_value="low"):
            priority = get_priority_input()
            self.assertEqual(priority, "low")
            self.assertIsInstance(priority, str)
            self.assertIn(priority, ["low", "medium", "high"])
            self.assertRegex(priority, r"\w+")
    
    def test_get_duration_input(self):
        with patch("builtins.input", return_value="3"):
            duration = get_duration_input()
            self.assertEqual(duration, "3")
            self.assertIsInstance(duration, str)
            self.assertNotEqual(duration, "")
            self.assertRegex(duration, r"\d+")
    
    def test_get_comments_input(self):
        with patch("builtins.input", return_value="Important task"):
            comments = get_comments_input()
            self.assertEqual(comments, "Important task")
            self.assertIsInstance(comments, str)
            self.assertNotEqual(comments, "")
            self.assertRegex(comments, r"\w+")
    
    def test_get_assigned_input(self):
        with patch("builtins.input", return_value="John Doe"):
            assigned_to = get_assigned_input()
            self.assertEqual(assigned_to, "John Doe")
            self.assertIsInstance(assigned_to, str)
            self.assertNotEqual(assigned_to, "")
            self.assertRegex(assigned_to, r"\w+")
    
    def test_get_start_date_input(self):
        with patch("builtins.input", return_value="2023-01-15"):
            start_date = get_start_date_input()
            self.assertEqual(start_date, "2023-01-15")
            self.assertIsInstance(start_date, str)
            self.assertNotEqual(start_date, "")
            self.assertRegex(start_date, r"\d{4}-\d{2}-\d{2}")
    
    def test_get_deadline_input(self):
        with patch("builtins.input", return_value="2023-02-28"):
            deadline = get_deadline_input()
            self.assertEqual(deadline, "2023-02-28")
            self.assertIsInstance(deadline, str)
            self.assertNotEqual(deadline, "")
            self.assertRegex(deadline, r"\d{4}-\d{2}-\d{2}")
    
    def test_get_owner_input(self):
        with patch("builtins.input", return_value="Jane Smith"):
            owner_name = get_owner_input()
            self.assertEqual(owner_name, "Jane Smith")
            self.assertIsInstance(owner_name, str)
            self.assertNotEqual(owner_name, "")
            self.assertRegex(owner_name, r"\w+")
    
    def test_get_project_task_id(self):
        with patch("builtins.input", return_value="P456"):
            project_task_id = get_project_task_id()
            self.assertEqual(project_task_id, "P456")
            self.assertIsInstance(project_task_id, str)
            self.assertNotEqual(project_task_id, "")
            self.assertRegex(project_task_id, r"\w+")
    
    def test_any_key_continue(self):
        with patch("builtins.input", return_value=""):
            user_input = any_key_continue()
            self.assertEqual(user_input, "")
            self.assertIsInstance(user_input, str)
            self.assertEqual(user_input, "")
            self.assertNotRegex(user_input, r"\w+")
    
    def test_get_file_path(self):
        with patch("builtins.input", return_value="/path/to/file.txt"):
            file_path = get_file_path()
            self.assertEqual(file_path, "/path/to/file.txt")
            self.assertIsInstance(file_path, str)
            self.assertNotEqual(file_path, "")
            self.assertRegex(file_path, r"\w+")

        with patch("builtins.input", return_value=""):
            file_path = get_file_path()
            self.assertEqual(file_path, "")
            self.assertIsInstance(file_path, str)
            self.assertEqual(file_path, "")
            self.assertNotRegex(file_path, r"\w+")