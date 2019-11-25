import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
import global_record
import grab_list
import numpy as np
import pickle
import get_movie_info
import display_final_movie

colors = {
    'background': '#111111',
    'text': '#000080'
}
num_movie_rate = 8
num_final_recommend = 10

file = open('cop.txt', 'rb')
cop = pickle.load(file)

obs = grab_list.read_csv()
id_set = obs.id_set
id_title_set = obs.id_title_set


def add_movies(zipped_list):
    result = []
    for item in zipped_list:
        item_index = item[0]
        item_movie_id = item[1]
        item_json = get_movie_info.get_movie_json(item_movie_id)
        name = item_json[get_movie_info.MovieJsonKeys.name]
        poster = get_movie_info.poster_url_constant + item_json[get_movie_info.MovieJsonKeys.poster_url]
        overview = item_json[get_movie_info.MovieJsonKeys.overview]
        text_font_size = '12px' if len(overview) < 600 else '11px' if len(overview) < 700 else '10px' if len(overview) < 900 else '9px'
        result.append(
            html.Div([
                html.Div(
                    id='movie_title_{}'.format(item_index),
                    children=name,
                    style={
                        'margin': '5px',
                        'textAlign': 'center',
                        'color': colors['text']}),
                html.Div(
                    className='container',
                    children=[html.Img(className='image', id='image_{}'.format(item_index), src=poster),
                              html.Div(className='middle',
                                       children=html.Div(
                                           className='text',
                                           children=f'Movie overview: {overview}',
                                           style={'font-size': text_font_size}))]),
                html.Div(
                    dcc.Dropdown(
                        id='rating_{}'.format(item_index),
                        options=[{'label': str(i), 'value': i} for i in np.arange(0, 5.5, 0.5)],
                        value=3,
                        placeholder="Please select a rating"),
                    style={
                        'width': '80%',
                        'margin-left': '20px',
                        'padding-left': '10%',
                        'padding-right': '10%',
                        'color': colors['text']})
            ], style={'margin': '15px', 'width': '22%', 'display': 'inline-block'})
        )
    return result

user_val = []
user_val.extend([{'label': str(i), 'value': i} for i in np.arange(1, 467, 1)])

def main():
    movie_div = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                         global_record.initial_movie_id_list[10:(10+num_final_recommend)]))
    #global_record.set_curr_movie_id_list(global_record.initial_movie_id_list)
    search_bar = html.Div(
        children=[
            html.Div(children='Please type a user ID',
                     style={'text-align': 'center',
                            'font-size': '16px',
                            'margin-bottom': '20px'}),
            html.Div(dcc.Dropdown(
                id='user_id_dropdown',
                options=user_val,
                # multi=True,
                placeholder="Please select/type a user id"))
        ]
    )
    search_button_div = html.Div(html.Button(id='user_id_button', children='Find User'),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '100px',
                                        'width': '40%',
                                        'margin-left': '30%',
                                        'text-align': 'center'})
    '''
    submit_button_div = html.Div(html.Button(id='my_button', children='Submit'),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '100px',
                                        'width': '40%',
                                        'padding-left': '45%',
                                        'padding-right': '15%'})
    '''
    movie_div = add_movies(zip(range(num_movie_rate), global_record.get_curr_movie_id_list()[:num_movie_rate]))
    #movie_div.append(submit_button_div)
    app_recommender_tab = html.Div(children=[])
    app_recommender_tab.children.append(html.Div(search_bar, style={'margin-top': '50px'}))
    app_recommender_tab.children.append(search_button_div)
    app_recommender_tab.children.append(html.Div("List of movies:"))
    app_recommender_tab.children.append(html.Div(id='recommend_main_div', children=movie_div))
    '''
    app_recommender_tab = html.Div([
        # html.H1(children='Movie Recommendation System'),
        search_bar,
        search_button_div,
        html.Div("List of movies:"),
        # TODO: initial movie_id list to be changed
        # html.Div(id='recommend_main_div', children=add_movies(zip(range(num_movie_rate), sample_list_movie_id[:num_movie_rate))),
        # html.Div(html.Button(id='my_button', children='Submit'),
        #          style={'margin': '15px', 'width': '40%', 'padding-left': '40%', 'padding-right': '20%'})])
        html.Div(id='recommend_main_div', children=movie_div)])
        '''
    return app_recommender_tab


def call_back_recom():
    list_state = [State('user_id_dropdown', 'value')]
    '''
    list_state = [State(f'rating_{i}', 'value') for i in range(num_movie_rate)]
    list_state.append(State('my_button', 'children'))

    submit_button_div = html.Div(html.Button(id='my_button', children='Submit'),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '100px',
                                        'width': '40%',
                                        'padding-left': '45%',
                                        'padding-right': '15%'})

    back_button_div = html.Div(html.Button(id='my_button', children='Go Back', n_clicks=0),
                               style={'margin-top': '50px',
                                      'margin-bottom': '100px',
                                      'width': '40%',
                                      'padding-left': '45%',
                                      'padding-right': '15%'})
    '''
    # TODO: should add restrictions to click button (all dropdown boxes should be filled out)
    @app.callback(
        Output('recommend_main_div', 'children'),
        [Input('user_id_button', 'n_clicks')],
        list_state)
    def update_multi_output(n_clicks, *input_value):
        ctx = dash.callback_context
        if not ctx.triggered:
            user_click = 'No clicks yet'
        else:
            user_click = ctx.triggered[0]['prop_id'].split('.')[0]
        button_text = input_value[-1]
        if n_clicks is not None and n_clicks > 0:
            # input_value = ctx.states.values()
            # rating of the current movies
            list_rating = list(map(float, input_value[:-1]))
            # should be able to get movie id's of current movies
            list_current_movie_id = global_record.get_curr_movie_id_list()
            if global_record.get_total_list_shown() == 2:
                # TODO: dynamic input needed here
                result = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                                  global_record.initial_movie_id_list[
                                                                  10:(10 + num_final_recommend)]))
                result.append(back_button_div)
                return result
            else:
                list_filter = list(input_value)
                print(list_filter)
                user_id = int(list_filter[0])
                print(user_id)
                # then use rating and id of current movies, to calculate id's of the next 15 movies
                # list_next_movie_id = get_next_recommendations(list_rating, list_current_movie_id)
                # movie id's of the next 15 movies
                #list_next_movie_id = [862 if r < 3 else 2 for r in list_rating]
                list_next_movie_id = []
                movie_names = cop.user_recommendation_dic[user_id]
                for mn in movie_names:
                    print(mn)
                    #print(id_title_set[mn])
                    list_next_movie_id.append(int(id_title_set[mn]))
                print(list_next_movie_id)
                ls = []
                for ids in list_next_movie_id:
                    if ids in id_set:
                        ls.append(ids)
                # TODO: call backend to filter here (param is a list: 'Genre', 'Year', 'Country', 'Director', 'Actors')
                #list_next_movie_id = [862 if r == 2000 else 2 for r in list_filter]
                list_next_movie_id = ls
                num_movie_rate = len(list_next_movie_id)
                print(list_next_movie_id)
                #global_record.set_curr_movie_id_list(list_next_movie_id)
                #global_record.add_total_list_shown()
                result = add_movies(zip(range(num_movie_rate), list_next_movie_id))
                #result.append(submit_button_div)
                return result
        # elif n_clicks is not None and n_clicks > 0 and button_text == 'Go Back':
        #     global_record.set_total_list_shown(0)
        #     global_record.set_curr_movie_id_list(global_record.initial_movie_id_list)
        #     return movie_div
        else:
            raise PreventUpdate


if __name__ == '__main__':
    main()
