import ipywidgets as widgets
from IPython.display import display
from tabulate import tabulate


def tabulate_for_jupyter(table):
    output_widget = widgets.Output()
    with output_widget:
        display(widgets.HTML(value="<pre>" + table + "</pre>"))
    output_widget.layout.overflow_x = "scroll"
    output_widget.layout.width = '100%'
    display(output_widget)


def print_column_description(result_dict):
    column_names = list(result_dict.keys())
    column_descriptions = list(result_dict.values())
    headers = ["column_names", "description"]
    table_column_description_list = [[column_names[i], column_descriptions[i]] for i in range(len(column_names))]
    tabulate_result = tabulate(table_column_description_list, headers=headers, tablefmt="simple_grid")
    tabulate_for_jupyter(tabulate_result)


def print_result_data(result_data):
    query_result = result_data.data
    headers = query_result[0].keys()
    values = [list(record.values()) for record in query_result]
    tabulate_result = tabulate(values, headers=headers, tablefmt="simple_grid")
    tabulate_for_jupyter(tabulate_result)


def print_columns(column_names):
    headers = [f"COLUMN_{i + 1}" for i in range(len(column_names))]
    tabulate_result = tabulate([column_names], headers=headers, numalign="right", stralign="right",
                               tablefmt="simple_grid")
    tabulate_for_jupyter(tabulate_result)
