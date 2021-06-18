import dash
import dash_design_kit as ddk
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from event_plotter import plotEvents
from dash.dependencies import Input, Output
from team_radar import team_radar_builder
import dash_html_components as html
import glob
import dash_table
import pathlib
import pandas as pd

from initial_figures import initial_figure_radar, initial_figure_events

# Theme export from Theme Builder to tailor the app's appearance
theme = {
    "accent": "#0a0a0a",
    "accent_positive": "#ede4e4",
    "accent_negative": "#C20000",
    "background_content": "#400707",
    "background_page": "rgb(0,0,0)",
    "body_text": "#f28c0f",
    "border": "#820505",
    "border_style": {
        "name": "underlined",
        "borderWidth": "0px 0px 1px 0px",
        "borderStyle": "solid",
        "borderRadius": 0
    },
    "button_border": {
        "width": "1px",
        "color": "#0a0a0a",
        "radius": "30px"
    },
    "button_capitalization": "uppercase",
    "button_text": "#2a2c2e",
    "button_background_color": "#f5ebeb",
    "control_border": {
        "width": "0px",
        "color": "#574141",
        "radius": "0px"
    },
    "control_background_color": "rgb(166, 28, 15)",
    "control_text": "#f5ebeb",
    "card_margin": "7px",
    "card_padding": "5px",
    "card_border": {
        "width": "0px",
        "style": "solid",
        "color": "#0a0a0a",
        "radius": "0px"
    },
    "card_background_color": "#36060e",
    "card_box_shadow": "0 0 0 #e3dede",
    "card_outline": {
        "width": "0px",
        "style": "solid",
        "color": "#0a0a0a"
    },
    "card_header_margin": "0px",
    "card_header_padding": "5px",
    "card_header_border": {
        "width": "0px",
        "style": "solid",
        "color": "#0a0a0a",
        "radius": "0px"
    },
    "card_header_background_color": "#0a0a0a",
    "card_header_box_shadow": "0px 0px 0px rgba(0,0,0,0)",
    "breakpoint_font": "1200px",
    "breakpoint_stack_blocks": "700px",
    "colorway": [
        "#00bfff",
        "#66c2a5",
        "#fc8d62",
        "#e78ac3",
        "#a6d854",
        "#ffd92f",
        "#e5c494",
        "#b3b3b3"
    ],
    "colorscale": [
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a",
        "#0a0a0a"
    ],
    "dbc_primary": "#70262c",
    "dbc_secondary": "#ffffff",
    "dbc_info": "#009AC7",
    "dbc_gray": "#f5f0f0",
    "dbc_success": "#f0f2f5",
    "dbc_warning": "#F9F871",
    "dbc_danger": "#C20000",
    "font_family": "Open Sans",
    "font_family_header": "Open Sans",
    "font_family_headings": "Open Sans",
    "font_size": "17px",
    "font_size_smaller_screen": "15px",
    "font_size_header": "24px",
    "title_capitalization": "uppercase",
    "header_content_alignment": "spread",
    "header_margin": "0px 0px 15px 0px",
    "header_padding": "0px",
    "header_border": {
        "width": "0px",
        "style": "solid",
        "color": "#e2e2e2",
        "radius": "0px"
    },
    "header_background_color": "#000000",
    "header_box_shadow": "none",
    "header_text": "#aaaaaa",
    "heading_text": "#aaaaaa",
    "text": "#aaaaaa",
    "report_background_content": "#FAFBFC",
    "report_background_page": "white",
    "report_text": "white",
    "report_font_family": "Computer Modern",
    "report_font_size": "20px"
}
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#140f0e',
    'color': 'white',
    'padding': '6px'
}

# Create list of event csv files available to select from via a pulldown menu
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
event_file_list = (glob.glob('*.csv'))
event_files = [w.replace("", "") for w in event_file_list]
event_files = [s for s in event_files]
dfglo = pd.read_csv(DATA_PATH.joinpath('Glosary.txt'),
                 encoding='utf-8-sig')
sfglo = pd.read_csv(DATA_PATH.joinpath('effectif.txt'),
                 encoding='utf-8-sig')



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}, ], )

app.title = "Wydad Football Science"
server = app.server
style = {'background-color': "black"}
# Configure controls using Dash Design Kit
static_graph_controls = [
    ddk.ControlItem(
        dcc.Dropdown(
            id='event-file',
            options=[
                {'label': i, 'value': i}
                for i in event_files
            ],
            multi=False,
            value=None
        ),
        label='Match:',
    ),
    ddk.ControlItem(
        dcc.Dropdown(
            id='team-dropdown',
            multi=False,
            options=[{'label': i, 'value': i} for i in ['Wydad', 'Adversaire']],
            value='Wydad'
        ),
        label='Équipe:',
    ),

    dcc.Location(id="url", refresh=False),
    html.Div(id='content'), ]
Wydad_Football_Science = (
    "Une application d'analyse de données de football multi-onglets basée sur Dash pour Le Wydad Atheltic Club"
    "Les données utilisées ont été mises à disposition par Wydad Football Science, afin que les analystes puissent évaluer les performances des deux équipes pendant le match."
    " Ce produit est une version très réduite")
how_is_it_worked_out = (
    "REMIDI Kamal | 25 ANS | PhD STUDENT IN ECONOMICS |"
    "Football CLUB MIDTJYLLAND PART TIME DATA ANALYST |"
    "FUTUR ENTRAINEUR DU WAC ")
# Configure main app layout
app.layout = ddk.App(theme=theme, children=[html.Header(
    html.Details(id='details_header',
                 children=[
                     html.Summary('À propos'),

                     html.Div(id='infopanel', children=[
                         html.H2(id='app_title', children='"Numbers don t lie, people do"'),

                         html.H1(id='match_header'),
                         html.P(className='paraheader', id='match_date'),
                         html.P(className='paraheader', id='match_stadium'),
                         html.P(className='paraheader', id='match_ref'),
                         html.Br(),
                         html.P(className='paraheader', children='Wydad Football Science?'),
                         html.Br(),
                         html.P(className='para', children=Wydad_Football_Science),
                         html.Br(),
                         html.P(className='para', children=how_is_it_worked_out),
                         html.Br(),
                     ])
                 ])
),
    ddk.Header([
        ddk.Logo(src=app.get_asset_url('jpg.jpg')),
        ddk.Title('Wydad Football Science'),

    ]),
    dcc.Tabs([
        dcc.Tab(label='Analyse',style=tab_style, selected_style=tab_selected_style, children=[
    ddk.Row([
        ddk.ControlCard(static_graph_controls, orientation='horizontal'),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon1",
                        children=[ddk.Graph(id='radar-graph', figure=initial_figure_radar(),
                                            config={
                                                'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d', 'autoScale2d',
                                                                           'resetScale2d']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon2",
                        children=[ddk.Graph(id='events-shots', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon3",
                        children=[ddk.Graph(id='Assists to Shots', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon4",
                        children=[ddk.Graph(id='events-progressive-passes', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon5",
                        children=[ddk.Graph(id='events-crosses', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon6",
                        children=[ddk.Graph(id='events-through', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon7",
                        children=[ddk.Graph(id='events-recovery', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon8",
                        children=[ddk.Graph(id='events-lost', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon9",
                        children=[ddk.Graph(id='events-Dribbles', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon10",
                        children=[ddk.Graph(id='events-duels', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon11",
                        children=[ddk.Graph(id='events-key-passes', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon12",
                        children=[ddk.Graph(id='events-box', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon13",
                        children=[ddk.Graph(id='Goal-kick', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines']})],
                        type="default",
                        )
        ]
                 ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon14",
                        children=[ddk.Graph(id='CORNER', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd': ['drawline',
                                                                            'drawopenpath',
                                                                            'drawcircle',
                                                                            'drawrect',
                                                                            'eraseshape'
                                                                            ],
                                                    'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d',
                                                                               'autoScale2d', 'resetScale2d']})],
                        type="default",
                        ),
        ]
                 ),
    ]),
        ]),
        dcc.Tab(label='Effectif',style=tab_style, selected_style=tab_selected_style, children=[
            dcc.Tab(label='Effectif', style=tab_style, selected_style=tab_selected_style, children=[html.Div([
                dash_table.DataTable(
                    id='table',
                    data=sfglo.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in sfglo.columns],

                    fixed_rows={'headers': True},

                    style_table={'height': '600px',
                                 'overflowY': 'auto',
                                 'overflowX': 'auto'},

                    style_cell={'whiteSpace': 'normal',
                                'height': 'auto',
                                'fontSize': 20,
                                'textAlign': 'left',
                                'backgroundColor': '#09090a'},

                    style_header={'backgroundColor': '#09090a',
                                  'border': '2px solid #cd4f39',
                                  'fontSize': 20,
                                  'color': 'white'},
                    style_cell_conditional=[
                        {'if': {'column_id': 'Num'},
                         'width': '10%'},
                        {'if': {'column_id': 'Joueur'},
                         'width': '90%'},

                    ],
                ),

            ], style={'width': '100%',
                      'display': 'block',
                      'padding': '25px 5px 5px 30px',
                      }
            ),
        ]),
        ]),
        dcc.Tab(label='Glossaire',style=tab_style, selected_style=tab_selected_style, children=[html.Div([
         dash_table.DataTable(
                 id='table1',
                 data=dfglo.to_dict('records'),
                 columns=[{"name": i, "id": i} for i in dfglo.columns],

                 fixed_rows={'headers': True},

             style_table={'height': '600px',
                          'overflowY': 'auto',
                          'overflowX': 'auto'},

             style_cell={'whiteSpace': 'normal',
                         'height': 'auto',
                         'fontSize': 20,
                         'textAlign': 'left',
                         'backgroundColor': '#09090a'},

             style_header={'backgroundColor': '#09090a',
                           'border': '2px solid #cd4f39',
                           'fontSize': 20,
                           'color': 'white'},
                 style_cell_conditional=[
            {'if': {'column_id': 'Abreviatura'},
             'width': '10%'},
            {'if': {'column_id': 'Definición'},
             'width': '90%'},

                  ],
         ),


                 ],style={'width': '100%',
                 'display': 'block',
                 'padding': '25px 5px 5px 30px',
          }
              ),
         ]),
         ]),
    html.Footer(
        [html.H6("Wydad Football Science 2021 | Tous droits réservés ©",
                 style={'text-align': "center", 'color': "white", "font-size": "15px"})]),
    ]
)

@app.callback(
    [Output('events-shots', 'figure'), Output('Assists to Shots', 'figure'),Output('CORNER', 'figure'),Output('Goal-kick', 'figure'), Output('events-progressive-passes', 'figure'),Output('events-crosses', 'figure'),Output('events-recovery', 'figure'), Output('events-lost', 'figure'),Output('events-Dribbles', 'figure'), Output('events-duels', 'figure'),Output('events-key-passes', 'figure'), Output('events-box', 'figure'),Output('events-through', 'figure')],
    [Input('event-file', 'value'),
     Input('team-dropdown', 'value')], prevent_initial_call=True)
def event_graph(event_file, team):
    if team is not None and event_file is not None:
        fig_shots = plotEvents('Tirs', event_file, team, 'Wydad')
        fig_crn = plotEvents('Corners', event_file, team, 'Wydad')
        fig_gk = plotEvents('Six mètres', event_file, team, 'Wydad')
        fig_box = plotEvents('Touches dans la surface', event_file, team, 'Wydad')
        fig_dribbles = plotEvents('Dribbles', event_file, team, 'Wydad')
        fig_duels = plotEvents('Duels', event_file, team, 'Wydad')
        fig_lost = plotEvents('Perte du ballon', event_file, team, 'Wydad')
        fig_assists = plotEvents('Tirs Assists', event_file, team, 'Wydad')
        fig_pey = plotEvents('Key Passes', event_file, team, 'Wydad')
        fig_recovery = plotEvents('Récupérations', event_file, team, 'Wydad')
        fig_crosses = plotEvents('Centres', event_file, team, 'Wydad')
        fig_progressive_passes = plotEvents('Les passes progressives dans dernier tiers', event_file, team, 'Wydad')
        fig_through = plotEvents('Les passes derrière la ligne', event_file, team, 'Wydad')

        for x in [fig_shots, fig_assists, fig_crosses,fig_gk,fig_crn, fig_progressive_passes, fig_box, fig_dribbles, fig_duels, fig_lost, fig_recovery, fig_pey, fig_through]:
            # Change modebar drawing item colour so that it stands out (vs. grey)
            x.update_layout(newshape=dict(line_color='#009BFF'))
        return fig_shots, fig_assists, fig_crosses, fig_progressive_passes, fig_box, fig_dribbles, fig_duels, fig_lost, fig_recovery, fig_pey, fig_through, fig_gk, fig_crn

    else:
        fig = initial_figure_events()
        return fig, fig, fig, fig, fig, fig, fig, fig, fig, fig, fig, fig, fig


# Callback for KPI Radar
@app.callback(
    Output('radar-graph', 'figure'),
    [Input('event-file', 'value'),
     Input('team-dropdown', 'value')], prevent_initial_call=True)
def radar_graph(radar_file, team):
    if team is not None:
        fig = team_radar_builder(radar_file, team)
        return fig
    else:
        fig = initial_figure_radar()
        fig.update_layout(margin=dict(l=80, r=80, b=30, t=55))
        # Disable zoom. It just distorts and is not fine-tunable
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        return fig

if __name__ == '__main__':
    app.run_server(debug=False)
