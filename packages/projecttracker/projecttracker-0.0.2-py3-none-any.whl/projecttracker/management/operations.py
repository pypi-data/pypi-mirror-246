import pandas as pd
from IPython.display import clear_output
from projecttracker.utils import file_handler, input_handler

class NoDataError(Exception):
    def __str__(self):
        return 'There is no data available.'
    
class Operations:
    '''Class that manages project and task operations.'''

    def __init__(self):
        '''Initializes Operations class with empty dictionaries to store projects and tasks.'''
        self.projects = {}
        self.tasks = {}
        
    def view(self):
        '''View projects and associated tasks.'''
        try:
            # Read projects and tasks from JSON files
            projects_from_json = file_handler.read_from_json('project.json')
            tasks_from_json = file_handler.read_from_json('task.json')

            # Check if both projects and tasks data are available
            if not projects_from_json:
                raise NoDataError()
            elif not tasks_from_json:
                project_df = pd.DataFrame(projects_from_json)
                return project_df.head(10)
            else:
                # Convert data to pandas DataFrame
                project_df = pd.DataFrame(projects_from_json)
                task_df = pd.DataFrame(tasks_from_json)

                # Merge projects and tasks separately using left merge
                result_df = pd.merge(project_df, task_df, on='projectID', how='left')

                # Display the result
                return result_df
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def add_proj(self, **kwargs):
        '''
        Add a new project to the system.

        Args:
            **kwargs: Variable keyword arguments containing project details.

        Returns:
            Project: The newly created Project object.
        '''
        new_proj = Project(**kwargs)
        print(f"Project '{new_proj.projectID}' added.")
        file_handler.write_to_json(new_proj, 'project.json', 'a')  # Write to JSON file
        return new_proj

    def add_task(self, **kwargs):
        '''
        Add a new task to an existing project in the system.

        Args:
            **kwargs: Variable keyword arguments containing task details.

        Returns:
            Task: The newly created Task object, if added successfully.
            None: If the project for the task does not exist.
        '''
        new_task = Task(**kwargs)
        projects_from_json = file_handler.read_from_json('project.json')
        project_ids = [project['projectID'] for project in projects_from_json]
        
        if new_task.projectID in project_ids:
            file_handler.write_to_json(new_task, 'task.json', 'a')  # Write to JSON file
            print(f"Task '{new_task.taskID}' added.")
            return new_task
        else:
            print(f"Project {new_task.projectID} does not exist.")
            return None
    
    def modify_item(self):
        '''Modify attributes of a project or task.'''
        modify_type = input_handler.get_project_task_id()
        
        while True:
            # Read data from JSON files
            projects_from_json = file_handler.read_from_json('project.json')
            tasks_from_json = file_handler.read_from_json('task.json')

            # Identify the list and ID based on user input
            if modify_type[0] == 'P':
                items_list = projects_from_json
                item_ids = [project['projectID'] for project in projects_from_json]
            elif modify_type[0] == 'T':
                items_list = tasks_from_json
                item_ids = [task['taskID'] for task in tasks_from_json]
            else:
                print("Invalid input. Please enter correct 'project' or 'task' IDs.")
                break  # Exit the loop if the input is invalid

            # Check if the specified ID exists
            if modify_type not in item_ids:
                print(f"{modify_type} not found.")
                break  # Exit the loop if the ID is not found

            # Find the dictionary with the specified ID
            item_index = item_ids.index(modify_type)
            item = items_list[item_index]

            # Display current attributes
            clear_output(wait=True)
            print(f"Current attributes of {modify_type}:")
            for key, value in item.items():
                print(f"{key}: {value}")

            # Get the attribute to modify
            attribute = input("Enter the attribute to modify: ")

            # Check if the attribute exists
            if attribute not in item:
                print(f"Attribute '{attribute}' does not exist in {modify_type}.")
            else:
                # Get the new value for the attribute
                new_value = input(f"Enter new value for '{attribute}': ")

                # Update the attribute in the dictionary
                item[attribute] = new_value

                # Write the modified list of dictionaries back to the JSON file
                if modify_type[0] == 'P':
                    file_handler.delete_all_objects('project.json')
                    for project_item in projects_from_json:
                        file_handler.write_to_json_dict(project_item, 'project.json')
                elif modify_type[0] == 'T':
                    file_handler.delete_all_objects('task.json')
                    for task_item in tasks_from_json:
                        file_handler.write_to_json_dict(task_item, 'task.json')

                print(f"Attribute '{attribute}' updated for '{modify_type}'.")

            if input(f"Do you want to continue updating {modify_type} (Y/N)?").upper() != 'Y':
                break  # Exit the loop if the user does not want to continue
    
    def delete_item(self):
        '''Delete a project or task.'''
        projects_from_json = file_handler.read_from_json('project.json')
        project_ids = [project['projectID'] for project in projects_from_json]
        tasks_from_json = file_handler.read_from_json('task.json')
        task_ids = [task['taskID'] for task in tasks_from_json]
        
        delete_type = input_handler.get_project_task_id()

        confirm_delete = input(f"Are you sure you want to delete {delete_type} Y/N? ").upper()
        
        if confirm_delete != "Y":
            return None # Exit if user does not confirm deletion
        
        # Check if the delete type refers to a project ('P') or a task ('T')
        if delete_type[0] == 'P':

            if delete_type in project_ids:
                 # Create a list excluding the project to be deleted
                project_list = [project for project in projects_from_json if project['projectID'] != delete_type]
                file_handler.delete_all_objects('project.json') 
                for project_item in project_list:
                    file_handler.write_to_json_dict(project_item, 'project.json')
                print(f"Project '{delete_type}' deleted.")
                return delete_type # Return the deleted project ID
            else:
                print(f"Project '{delete_type}' not found.")
                return None # Return None if project ID doesn't exist
        elif delete_type[0] == 'T':
            if delete_type in task_ids:
                # Create a list excluding the task to be deleted
                task_list = [task for task in tasks_from_json if task['taskID'] != delete_type]
                file_handler.delete_all_objects('task.json')
                for task_item in task_list:
                    file_handler.write_to_json_dict(task_item, 'task.json')
                print(f"Task '{delete_type}' deleted.")
                return delete_type # Return the deleted task ID
            else:
                print(f"Task '{delete_type}' not found.")
                return None # Return None if task ID doesn't exist
        else:
            print("Invalid input. Please enter 'project' or 'task'.")
            return None # Return None if invalid input for delete type

class Project(Operations):
    '''Class representing a project that inherits properties from operations.'''
    def __init__(self, Name, Priority, Duration, Comments, assignedTo, startDate, Deadline, Owner):
        '''
        Initialize a Project instance with the given attribute details.

        Args:
            Name (str): Project name.
            Priority (str): Priority level of the project.
            Duration (str): Project duration.
            Comments (str): Comments/description of the project.
            assignedTo (str): Person/team assigned to the project.
            startDate (str): Project start date.
            Deadline (str): Project deadline.
            Owner (str): Owner of the project.
        '''
        project_id = self.get_next_project_id()
        self.projectID = f'P{project_id:04}'
        self.projectName = Name
        self.projectPriority = Priority
        self.projectDuration = Duration
        self.projectComments = Comments
        self.assignedToProjectTL = assignedTo
        self.projectStartDate = startDate 
        self.projectDeadline = Deadline
        self.projectOwner = Owner
        self.projectStatus = 'Not Started'

    def get_next_project_id(self):
        '''
        Retrieves the next available project ID by examining existing projects in the JSON file.

        Returns:
            int: The next available task ID.
        '''
         # Initialize the last project ID to 0
        last_project_id = 0
        try:
            # Attempt to read existing projects from the JSON file
            projects_from_json = file_handler.read_from_json('project.json')
        except:
            pass # Ignore exceptions if reading fails
        else:
            # If reading succeeds, extract project IDs and find the latest inserted project ID
            project_ids = [project['projectID'] for project in projects_from_json]
            last_inserted_project_id = max(project_ids, key=lambda x: int(x[1:]))
            last_project_id = int(last_inserted_project_id[1:])
        finally:
            last_project_id += 1  # Increment the last project ID for the next project to be added
            return last_project_id # Return the next available project ID

class Task(Project):
    '''Class representing a task associated with a project that inherits properties of project and operations.'''
    def __init__(self, projectID, Name, Priority, Duration, Comments, assignedTo, startDate, Deadline):
        '''
        Initialize a Task instance associated with a specific project with the given attribute details.

        Args:
            projectID (str): ID of the project the task belongs to.
            Name (str): Task name.
            Priority (str): Priority level of the task.
            Duration (str): Task duration.
            Comments (str): Comments/description of the task.
            assignedTo (str): Person/team assigned to the task.
            startDate (str): Task start date.
            Deadline (str): Task deadline.
        '''
        self.projectID = projectID
        task_id = self.get_next_task_id()
        self.taskID = f'T{task_id:04}'
        self.taskName = Name
        self.taskPriority = Priority
        self.taskDuration = Duration
        self.taskComments = Comments
        self.assignedToTask = assignedTo
        self.taskStartDate = startDate
        self.taskDeadline = Deadline
        self.taskStatus = 'Not Started'

    def get_next_task_id(self):
            '''
            Retrieves the next available task ID by examining existing tasks in the JSON file.

            Returns:
                int: The next available task ID.
            '''
            # Initialize the last task ID to 0
            last_task_id = 0
             # Attempt to read existing tasks from the 'task.json' file
            try:
                tasks_from_json = file_handler.read_from_json('task.json')
            except:
                pass  # Ignore exceptions if reading fails
            else:
                # If reading succeeds, extract task IDs and find the latest inserted task ID
                task_ids = [task['taskID'] for task in tasks_from_json]
                last_inserted_task_id = max(task_ids, key=lambda x: int(x[1:]))
                last_task_id = int(last_inserted_task_id[1:])
            finally:
                last_task_id += 1 # Increment the last task ID for the next task to be added
                return last_task_id # Return the next available task ID
    

