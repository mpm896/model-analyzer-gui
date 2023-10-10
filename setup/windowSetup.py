import PySimpleGUI as sg
import scripts.utils as u
import time

DEFAULT_WINDOW_SIZE = (867, 422)
THEME = 'Black2'


def make_window(layout: list, title: str = None, size: tuple = DEFAULT_WINDOW_SIZE, theme=THEME) -> sg.Window:
    return sg.Window(title=title, layout=layout, 
                     finalize=True, resizable=True, 
                     size=size)

def make_dataframe_window(df_list: list, title: str = None) -> sg.Window:
    '''
    Create a window with tabs, each containing a Pandas DataFrame
    Args: 
        df_list (list): List containing groups of Pandas DataFrames
    '''
    sg.theme(THEME)
    layouts = {}

    for df in df_list:
        for key in df:
            try:
                header, values = u.read_table(key)
            except TypeError:
                header = df[key].columns.tolist()
                values = df[key].values.astype('object')
                values[:,0:2] = values[:,0:2].astype('int')
                values = values.tolist()

                # Write the headings and values to a csv file
                u.write_table(key, df[key].columns.tolist(), values)
                
            df_layout = [[
                sg.Table(values=values, headings=header,
                        key=f"-DF TABLE-", enable_events=True,
                        expand_x=True, expand_y=True,
                        select_mode='extended')
            ]]
            layouts[key] = df_layout

    tabgroup = [[sg.Tab(key, layouts[key], key=key, tooltip=f'{key}') for key in layouts]]
    
    tableLayout = [[
            sg.TabGroup(tabgroup, key='TabGroup', 
                        expand_x=True, expand_y=True,
                        enable_events=True)
        ]]
    
    return make_window(tableLayout, title=title)

def make_plotting_window(df_list: list, title: str = None) -> sg.Window:
    '''
    Make a window giving the user options for plotting their 
    data from the dataframes
    '''
    pass