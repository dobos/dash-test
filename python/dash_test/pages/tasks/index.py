import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
from dash.dash_table import DataTable

dash.register_page(__name__, path="/tasks")

def layout(**kwargs):
    def get_task_link(task_id):
        href = dash.page_registry['pages.tasks.task']['relative_path']
        # Generate markdown link in the form of
        # [Task 12312434](task?task_id=12312434)
        return f'[Task {task_id}]({href}?task_id={task_id})'
        

    df = pd.DataFrame({
        'Date': ['2018-08-30 22:52:25', '2021-09-29 13:33:49'],
        'TaskID': [1444008, 1724734],
    })

    df['Link'] = df['TaskID'].map(get_task_link)

    columns = [
        {
            'id': 'Date',
            'name': 'Date'
        },
        {
            'id': 'Link',
            'name': 'Task ID',
            'presentation': 'markdown'
        }
    ]

    return html.Div([
        html.H1('This is our Tasks page'),
        html.Div([
            "Select a task: ",
            DataTable(
                data=df.to_dict(orient='records'),
                columns=columns
            )
        ]),
    ])

