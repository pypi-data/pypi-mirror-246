from datetime import datetime

def get_user_choice():
    '''
    Gets user choice as an integer input.
    
    Returns:
        int: User choice.
    '''
    try:
        choice = int(input('Enter your choice:'))
        return choice
    except ValueError:
        print('Invalid input')

def get_project_input():
    '''
    Gets user input for Project Name.
    
    Returns:
        str: Project name input by the user.
    '''
    return input('Enter Project Name:')
    
def get_task_input():
    '''
    Gets user input for Task Name.

    Returns:
        str: Task name input by the user.
    '''
    return input('Enter Task Name:')

def get_projectID_input():
    '''
    Gets user input for Project ID.

    Returns:
        str: Project ID input by the user.
    '''
    return input('Enter Project ID:')

def get_priority_input():
    '''
    Gets user input for priority.

    Returns:
        str: Priority input by the user.
    '''
    return input('Enter priority (low, medium, high):').lower()

def get_duration_input():
    '''
    Gets user input for duration.

    Returns:
        str: Duration input by the user.
    '''
    return input('Enter duration in months:')

def get_comments_input():
    '''
    Gets user input for comments.

    Returns:
        str: Comments input by the user.
    '''
    return input('Enter comments:')
    
def get_assigned_input():
    '''
    Gets user input for the name of the person the task is assigned to.

    Returns:
        str: Person's name input by the user.
    '''
    return input('Enter name of the person it is assigned to:')

def get_start_date_input():
    '''
    Gets user input for a start date in 'YYYY-MM-DD' format.

    Returns:
        str: Start date input by the user.
    '''
    return input('Enter start date (YYYY-MM-DD):')
    
def get_deadline_input():
    '''
    Gets user input for a deadline in 'YYYY-MM-DD' format.

    Returns:
        str: Deadline input by the user.
    '''
    return input('Enter deadline (YYYY-MM-DD):')
    
def get_owner_input():
    '''
    Gets user input for the name of the owner.

    Returns:
        str: Owner's name input by the user.
    '''
    return input('Enter name of the owner:')
    
def get_project_task_id():
    '''
    Gets user input for a project or task ID in uppercase.

    Returns:
        str: Project or task ID input by the user in uppercase.
    '''
    return input('Enter project or task ID:').upper()

def any_key_continue():
    '''
    Asks the user to press any key to continue.

    Returns:
        str: User's input (any key pressed).
    '''
    return input("Press any key to continue.")

def get_file_path():
    '''
    Gets user input for file path.
    
    Returns:
        str: File path input by the user.
    '''
    return input('Enter the file path you want to download the file to:')
