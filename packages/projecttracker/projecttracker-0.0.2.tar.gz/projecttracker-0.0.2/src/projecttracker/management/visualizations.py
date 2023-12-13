import plotly.express as px
import datetime
import pandas as pd
from projecttracker.utils import file_handler, input_handler

def gantt_chart():
    '''
    Generates and displays a Gantt chart.
    '''
    try:
        data = []
        projects_from_json = file_handler.read_from_json('project.json')
        project_list = [project for project in projects_from_json]
        for x in project_list:
                data.append(dict(Project=x["projectName"], Start=x["projectStartDate"], Finish=x["projectDeadline"], Priority=x["projectPriority"]))

        # Create a Gantt chart
        fig = px.timeline(data, x_start="Start", x_end="Finish", y="Project", hover_data={"Priority": True}, title='Project Schedule')

        # Show the Gantt chart
        fig.show()

        # Display Gantt chart for a specific project's tasks
        project_id = input_handler.get_projectID_input()
        data_project = []
        tasks_from_json = file_handler.read_from_json('task.json')
        task_list = [task for task in tasks_from_json if task['projectID'] == project_id]

        for x in task_list:
            data_project.append(dict(Task=x['taskName'], Start=x['taskStartDate'], Finish=x['taskDeadline'], Priority=x['taskPriority']))

        # Create a Gantt chart for each Project holding different Tasks
        fig = px.timeline(data_project, x_start="Start", x_end="Finish", y="Task", hover_data={"Priority": True}, labels={"Task": f"Project: {project_id}"}, title=f'Task Schedule for Project {project_id}')

         # Current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Add a vertical line for the current date
        fig.update_layout(shapes=[
            dict(
                type="line",
                x0=current_date,
                x1=current_date,
                y0=0,
                y1=1,
                yref="paper",
                line=dict(color="black", width=2),
            )
        ])

        # Show the Gantt chart for each Project holding different Tasks
        fig.show()
    except:
        print('No data is present to create the graph.')


def pie_chart():
    '''
    Generates and displays a Pie chart for task status distribution in a project.
    '''
    try:
        project_id = input_handler.get_projectID_input()
        data = []
        tasks_from_json = file_handler.read_from_json('task.json')
        task_list = [task for task in tasks_from_json if task['projectID'] == project_id]

        for x in task_list:
            data.append(dict(Task=x['taskName'], Start=x['taskStartDate'], Finish=x['taskDeadline'], Status=x['taskStatus']))

        # Create a Pie chart for the Project holding different Tasks
        fig = px.pie(data, names='Status', title=f'Task Status Distribution for {project_id}')

        # Show the Pie Chart
        fig.show()
    except:
        print('No data is present to create the graph.')


def scatter_plot():
    '''
    Generates and displays a Scatter plot showing project duration vs. priority.
    '''
    try:
        data = []
        projects_from_json = file_handler.read_from_json('project.json')
        project_list = [project for project in projects_from_json]

        # Create a scatter plot
        fig = px.scatter(project_list, x='projectPriority', y='projectDuration', color='projectPriority', title='Project Duration vs. Priority', size_max=50)

        # Update layout
        fig.update_layout(xaxis_title='projectPriority', yaxis_title='projectDuration', showlegend=True)

        # Show the figure
        fig.show()
    except:
        print('No data is present to create the graph.')

def bar_chart():
    '''
    Generates and displays a Bar chart showing the number of tasks in each project.
    '''
    try:
        tasks_from_json = file_handler.read_from_json('task.json')
        df = pd.DataFrame(tasks_from_json)

        # Group by project and count the number of tasks in each project
        project_counts = df.groupby('projectID').size().reset_index(name='Number of Tasks')

        # Create a bar plot
        fig = px.bar(project_counts, x='projectID', y='Number of Tasks', title='Number of Tasks in Each Project')

        # Update layout
        fig.update_layout(xaxis_title='Project', yaxis_title='Number of Tasks', showlegend=False)

        # Show the figure
        fig.show()
    except:
        print('No data is present to create the graph.')