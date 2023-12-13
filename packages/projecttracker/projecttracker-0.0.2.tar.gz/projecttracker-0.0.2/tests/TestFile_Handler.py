import unittest
import os
import json
import pandas as pd
from projecttracker.utils.file_handler import write_to_json, read_from_json, delete_all_objects, write_to_json_dict, download_csv
from projecttracker.management.operations import Operations

class TestFile_Handler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = Operations() 
        cls.obj.add_proj(**{
            'Name': 'Test Project 1',
            'Priority': 'High',
            'Duration': '4',
            'Comments': 'Created for unit testing',
            'assignedTo': 'Team Lead 1',
            'startDate': '2023-11-11',
            'Deadline': '2023-11-30',
            'Owner': 'Project Owner 1',
        })
        cls.file_name = "project.json"
        cls.dict_obj = {"name": "Alice", "age": 30}
        cls.dict_file_name = "test_dict_file.json"
        cls.delete_file_name = "test_delete.json"
        cls.data = pd.DataFrame({"name": ["Bob", "Charlie"], "age": [22, 35]})
        current_directory = os.getcwd()
        cls.csv_file_path = current_directory[2:]

    def setUp(self):
        self.test_data = {
            'projectID': 'P0001',
            'projectName': 'Test Project 1',
            'projectPriority': 'High',
            'projectDuration': '4',
            'projectComments': 'Created for unit testing',
            'assignedToProjectTL': 'Team Lead 1',
            'projectStartDate': '2023-11-11',
            'projectDeadline': '2023-11-30',
            'projectOwner': 'Project Owner 1',
            'projectStatus': 'Not Started'
        }

    def tearDown(self):
        print("Tear Down")

    def test_read_from_json(self):
        data = read_from_json(self.file_name)
        self.assertEqual(data[0]['projectID'], self.test_data['projectID'])
        self.assertEqual(data[0]['projectPriority'], self.test_data['projectPriority'])
        self.assertEqual(data[0]['projectStatus'], self.test_data['projectStatus'])
        self.assertEqual(data[0]['projectDuration'], self.test_data['projectDuration'])
    
    def test_write_to_json(self):
        write_to_json(self.obj, self.file_name)
        result = read_from_json(self.file_name)
        self.assertEqual(result[0], self.test_data)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("projectID", result[0])

    def test_delete_all_objects(self):
        with open(self.delete_file_name, 'w') as test_file:
            test_file.write("Test content")

        delete_all_objects(self.delete_file_name)

        with open(self.delete_file_name, 'r') as test_file:
            file_content = test_file.read()
            self.assertEqual(file_content, "")
        self.assertTrue(os.path.exists(self.delete_file_name))
        self.assertEqual(os.path.getsize(self.delete_file_name), 0)
        self.assertIsNone(delete_all_objects("non_existent_file.json"))

    def test_write_to_json_dict_write(self):
        write_to_json_dict(self.dict_obj, self.dict_file_name, method='w')
        result = read_from_json(self.dict_file_name)
        self.assertEqual(result, [self.dict_obj])
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("name", result[0])

    def test_download_csv_file_created(self):
        download_csv(self.data, self.csv_file_path)
        file_path = f"{self.csv_file_path}/project_details.csv"
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))
        self.assertGreater(os.path.getsize(file_path), 0)
        self.assertTrue(file_path.endswith(".csv"))

    def test_download_csv(self):
        download_csv(self.data, self.csv_file_path)
        file_path = f"{self.csv_file_path}/project_details.csv"
        result_data = pd.read_csv(file_path)
        pd.testing.assert_frame_equal(result_data, self.data)
        self.assertIsInstance(result_data, pd.DataFrame)
        self.assertEqual(result_data.shape, self.data.shape)
        self.assertListEqual(list(result_data.columns), list(self.data.columns))

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.file_name)
            os.remove(cls.dict_file_name)
            os.remove(cls.delete_file_name)
        except FileNotFoundError:
            pass
