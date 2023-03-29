import dateutil
from datetime import datetime
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output, State
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc

from flask import request
from urllib.parse import urlparse, parse_qs, urlencode

dash.register_page(__name__, path="/tasks")

# TODO: this should go under `lib`
def update_form(element, href):
    args = parse_qs(urlparse(href).query)
    update_element(element, args)

# TODO: this should go under `lib`
def update_element(element, args):
    if hasattr(element, "id"):
        if element.id in args:
            value = args[element.id]
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            element.value = value

    # Call recursively for each child, if any
    if hasattr(element, "children"):
        for c in element.children:
            update_element(c, args)

def merge_args(href, args=None):
    # Merge arguments from the query string and form values, form
    # values taking precedence
    nargs = {}
    if href is not None:
        nargs.update({ k: v[0] for k, v in parse_qs(urlparse(href).query).items() })
    if args is not None:
        nargs.update({ k: v for k, v in args.items() if v is not None })
    return nargs

def is_arg(name, args):
    return name in args

def get_arg(name, args, type=str, default=None):
    if name not in args:
        return default
    
    if type == str:
        return args[name]
    elif type == datetime:
        return dateutil.parser.parse(args[name])
    else:
        raise NotImplementedError()

# TODO: move this to the library
def and_mask(mask, filter):
    if mask is None or (isinstance(mask, slice) and mask == slice(None)):
        return filter
    else:
        return mask & filter

# TODO: This is just the old markdown trick, use bootstrap table instead
#       of "fancy" datatable
def get_task_link(task_id):
    href = dash.page_registry['pages.tasks.task']['relative_path']
    # Generate markdown link in the form of
    # [Task 12312434](task?task_id=12312434)
    return f'[Task {task_id}]({href}?task_id={task_id})'

def layout(**kwargs):       
    return html.Div([
        dcc.Location(id='location', refresh=True),
        html.H1('This is our Tasks page'),
        html.Div(id='form_placeholder', children=on_create_form()),
        html.Div(id='list_placeholder'),
    ])

@callback(
    Output('list_placeholder', 'children'),
    inputs=dict(
        href=Input('location', 'href'),
        date_from=State('date_from', 'value'),
        date_to=State('date_to', 'value'),
    )
)
def on_render_list(href, **kwargs):

    # This is just the old data table way
    df = pd.DataFrame({
        'Date': [datetime(2018, 8, 30, 22, 52, 25), datetime(2021, 9, 29, 13, 33, 49)],
        'TaskID': [1444008, 1724734],
    })

    df['Link'] = df['TaskID'].map(get_task_link)

    # Merge query string parameters and form inputs
    args = merge_args(href, kwargs)

    # Normally, these are sent to SQL server as query parameters
    mask = slice(None)
    date_from = get_arg('date_from', args, datetime)
    if date_from is not None:
        mask = and_mask(mask, date_from <= df['Date'])
    date_to = get_arg('date_to', args, datetime)
    if date_to is not None:
        mask = and_mask(mask, df['Date'] <= date_to)

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

    return [
            "Select a task: ",
            DataTable(
                data=df[mask].to_dict(orient='records'),
                columns=columns
            )
        ]

@callback(
    Output('form_placeholder', 'children'),
    Input('location', 'href'),
)
def on_create_form(href=None):
    form = dbc.Form(id='tasks_filter_form',
        children=[
            html.Div([
                dbc.Label("Date from", html_for="date_from"),
                dbc.Input(type="text", id="date_from", pattern=r"\d{1,2}/\d{1,2}{}/\d{2,4}{}", placeholder='01/01/2023')
            ]),
            html.Div([
                dbc.Label("Date to", html_for="date_to"),
                dbc.Input(type="text", id="date_to", placeholder='12/31/2023')
            ]),
            dbc.Col(dbc.Button("Filter", type="submit", id="filter-submit"), width="auto"),
        ])
    
    if href is not None:
        update_form(form, href)
    
    return form

@callback(
    Output('location', 'href'),
    inputs=dict(
        href=Input('location', 'href'),
        n_clicks=Input('filter-submit', 'n_clicks'),
        date_from=State('date_from', 'value'),
        date_to=State('date_to', 'value')
    ),
    prevent_initial_call=True
)
def on_submit_form(href, n_clicks, **kwargs):
    # Called when the page is rendered for the first time and when the
    # form is submitted. Just ignore the former and render a new URL in
    # the latter case

    if n_clicks is not None:
        args = merge_args(href, kwargs)
        href = urlparse(href)._replace(query=urlencode(args)).geturl()
        return href
    else:
        return href
