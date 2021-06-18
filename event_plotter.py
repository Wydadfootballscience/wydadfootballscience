# import dash
# import dash_core_components as dcc
# import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import math
from plotly.subplots import make_subplots

# Disable non-applicable Pandas warnings
pd.options.mode.chained_assignment = None  # default='warn'


# Find and piece together assists by finding shots, then checking if the action directly before
# a shot was a pass (or cross, which is treated as a subset of pass in this dataset).
# If so, count it as an assist.


# Locate and build a dataframe of all set plays, ignoring kick-offs and throw-ins


# Make all actions graph from left to right. Depending on which team starts on the left hand side,
# make adjustments to both teams for the opposite half which does NOT go left to right
def left_justify_events(df, team_on_left):
    df_half1 = df.loc[df['Period'] == 1]
    df_half2 = df.loc[df['Period'] == 2]
    if df.iloc[0]['Team'] == team_on_left:
        # Reverse all the second half events
        df_half2['Start_X'] = df_half2['Start_X'].map(lambda x: 1 - x)
        df_half2['End_X'] = df_half2['End_X'].map(lambda x: 1 - x)
        df_half2['Start_Y'] = df_half2['Start_Y'].map(lambda x: 1 - x)
        df_half2['End_Y'] = df_half2['End_Y'].map(lambda x: 1 - x)
        pass
    else:
        # Reverse all the first half events
        df_half1['Start_X'] = df_half1['Start_X'].map(lambda x: 1 - x)
        df_half1['End_X'] = df_half1['End_X'].map(lambda x: 1 - x)
        df_half1['Start_Y'] = df_half1['Start_X'].map(lambda x: 1 - x)
        df_half1['End_Y'] = df_half1['End_Y'].map(lambda x: 1 - x)

    df = pd.concat([df_half1, df_half2])
    return df


# Once number of clusters is auto-calculated, graph the cluseters
def create_cluster_graph(df, num_clusters):
    # creates a new trace for each set of data
    fig = make_subplots(
        rows=math.ceil(num_clusters / 2), cols=2,  # round up to nearest integer
        subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))
    x = df['x']
    y = df['y']
    r = 1  # rows
    c = 1  # columns
    for index, row in df.iterrows():
        fig.add_trace(go.Scatter(x=x, y=y, marker=dict(color="#009BFF", size=8),
                                 opacity=.8),
                      row=r, col=c)
        if c == 2:
            c = 1
            r = r + 1
        else:
            c = c + 1
    return fig


# Auto-determine which clustering model fits best with the data and select that
def get_num_clusters(df, maxclusters):
    # Get optimal number of clusters given the pattern
    global best_n_clusters
    sil_score_max = -1  # this is the minimum possible score

    for n_clusters in range(2, maxclusters):
        model = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
        labels = model.fit_predict(df)
        sil_score = silhouette_score(df, labels)
        # print("The average silhouette score for %i clusters is %0.2f" % (n_clusters, sil_score))
        if sil_score > sil_score_max:
            sil_score_max = sil_score
            best_n_clusters = n_clusters
    return best_n_clusters


# Draw arrow annotations for passes, crosses, etc.
def drawAnnotations(df):
    # Create annotations for all passes
    annotations_list = []
    for index, row in df.iterrows():
        colour = 'white'
        opacity_setting = 0.3

        # drop all rows that don't have a value in End_X because we don't want annotations for them
        df.dropna(subset=['End_X'], inplace=True)
        arrow = go.layout.Annotation(dict(
            x=row['End_X'],
            y=row['End_Y'],
            xref="x", yref="y",
            text="",
            showarrow=True,
            axref="x", ayref='y',
            ax=row['Start_X'],
            ay=row['Start_Y'],
            arrowhead=2,
            arrowwidth=1.5,
            arrowcolor=colour,
            opacity=opacity_setting,
            startstandoff=4
        )
        )
        annotations_list.append(arrow)

    return annotations_list


# Main function - graph all football events which occur in a match
def plotEvents(eventType, filename, team, team_on_left):
    # Read in event csv data file
    global df, filtered_df, fig, filtered_df1
    data_file = '' + filename
    events_df = pd.read_csv(data_file)
    events_df = events_df.loc[events_df['Team'] == team]
    events_df.reset_index(drop=True, inplace=True)

    # change coordinates to into floating numbers
    events_df['Start_X'] = pd.to_numeric(events_df['Start_X'], downcast="float")
    events_df['Start_Y'] = pd.to_numeric(events_df['Start_Y'], downcast="float")
    events_df['End_X'] = pd.to_numeric(events_df['End_X'], downcast="float")
    events_df['End_Y'] = pd.to_numeric(events_df['End_Y'], downcast="float")

    # Left justify all events so that they ALL go from left to right
    events_df = left_justify_events(events_df, team_on_left)

    # For events involving the graphing of movement of the ball from one location to another
    if (eventType == "Les passes progressives dans dernier tiers") or (eventType == "Centres") or (
            eventType == "Tirs Assists") or (eventType == "Key Passes") or (eventType == "Les passes derrière la ligne") or (eventType =="Corners") or (eventType == "Six mètres"):

        # Pick proper df based on what's being graphed
        if eventType == 'Les passes progressives dans dernier tiers':
            df = events_df.loc[events_df['Type'] == 'PASS']
            df.reset_index(drop=True, inplace=True)
            df = df.loc[(df['End_X'] - df['Start_X']) > .1]  # limit passes to those greater than 10M forward
            df = df.loc[df['End_X'] > .7]
        elif eventType == 'Tirs Assists':
            df = events_df.loc[events_df['Subtype'].str.contains('Assists', na=False)]
            df.reset_index(drop=True, inplace=True)
        elif eventType == 'Centres':
            df = events_df.loc[events_df['Subtype'].str.contains('Cross', na=False)]
            df.reset_index(drop=True, inplace=True)
        elif eventType == 'Key Passes':
            df = events_df.loc[events_df['Subtype'].str.contains('Key Passes', na=False)]
            df.reset_index(drop=True, inplace=True)
        elif eventType == 'Les passes derrière la ligne':
            df = events_df.loc[events_df['Subtype'].str.contains('Through', na=False)]
            df.reset_index(drop=True, inplace=True)
        elif eventType == 'Corners':
            df = events_df.loc[events_df['Subtype'].str.contains('CORNER', na=False)]
            df.reset_index(drop=True, inplace=True)
        elif eventType == 'Six mètres':
            df = events_df.loc[events_df['Subtype'].str.contains('Goal-kick', na=False)]
            df.reset_index(drop=True, inplace=True)

        # Replace all NaN values with none so we can use that to distinguish
        # action types in the plots
        df = df.where(pd.notnull(df), 'None')

        df_size = df.shape[0]

        # Draw the annotation arrows for passes etc. as long as there aren't too many
        # Where there ARE too many then cluster and create separate traces for each cluster
        if (df_size >= 1):  # or eventType == 'SetPlay':
            annotations_list = drawAnnotations(df)
        else:
            annotations_list = []

        color_discrete_map = {'CORNER': '#8a2608', 'Tirs Assists': '#009BFF',
                              'SHOT': '#009BFF', 'PASSM': '#a276f5', 'PASS': '#009BFF', 'BALL LOST': 'grey',
                              'BALL OUT': 'darkgrey', 'derriere la ligne': '#5e2770', 'Dribbles': '#990e45','Key Passes':'#267a05',
                              'Duels': '#db9eb6','centre rate': 'grey', 'Recovery': "#c96f14", 'Lost': "#807f7c", 'Box': '#cfc625','Centre':'#e0419c'}
        df['size'] = 15

        # Main graph for A > B events
        if eventType in ['Centres', 'Tirs Assists', 'Les passes progressives dans dernier tiers','Key Passes','Les passes derrière la ligne','Six mètres','Corners']:
            colorfactor = df['Type']
            fig = px.scatter(df, x="Start_X", y="Start_Y", color=colorfactor, size='size', text='From',
                             range_x=[-0.05,1.05], range_y=[-0.05,1.05],size_max=10, hover_name='Type',
                             color_discrete_map=color_discrete_map, opacity=0.8,
                             # marginal_x="histogram", marginal_y="rug",
                             hover_data={'Start_X': False, 'Start_Y': False, 'size': False, 'Type': False, 'From': True})

            fig.update_layout(
                annotations=annotations_list)

        # Add halos to markers
        fig.update_traces(marker=dict(
            line=dict(width=1,
                      color='darkgray')),
            selector=dict(mode='markers'))
    else:
        # This part is for the scatterplots without annotations
        if eventType == 'Tirs':
            filtered_df = events_df.loc[events_df['Type'] == 'SHOT']
        filtered_df['size'] = 10
        if eventType == 'Dribbles':
            filtered_df = events_df.loc[events_df['Subtype'] == 'Dribbles']
        filtered_df['size'] = 2
        if eventType == 'Duels':
            filtered_df = events_df.loc[events_df['Subtype'] == 'Duels']
        filtered_df['size'] = 2
        if eventType == 'Perte du ballon':
            filtered_df = events_df.loc[events_df['Subtype'] == 'Lost']
        filtered_df['size'] = 1
        if eventType == 'Touches dans la surface':
            filtered_df = events_df.loc[events_df['Type'] == 'Box']
        filtered_df['size'] = 1
        if eventType == 'Récupérations':
            filtered_df = events_df.loc[events_df['Type'] == 'Recovery']
        filtered_df['size'] = 1

        count_row = filtered_df.shape[0]
        if count_row > 4 and eventType == 'Tirs' or eventType == 'Dribbles' or eventType == 'Duels' or eventType == 'Perte du ballon' or eventType == 'Touches dans la surface' or eventType == 'Récupérations' :
            colorfactor1 = filtered_df['Type']
            color_discrete_map1 = {'CORNER': '#009BFF', 'Assists to Shots': '#009BFF',
                                  'SHOT': '#50568a', 'PASSM': '#a276f5', 'PASS': '#009BFF', 'BALL LOST': 'grey','Duel gagne': '#434c9c',
                                   'Key Passes': '#285248', 'dribble reussi': '#990e45',
                                  'Duels': '#db9eb6', 'Recovery': "#c96f14", 'Lost': "#807f7c", 'Box': '#cfc625','Passe ratee':'#7e8f8b','Ballon perdu': '#080807',
                                  'Through': '#009BFF'}
            filtered_df['size'] = 15
            fig = px.scatter(filtered_df, x="Start_X", y="Start_Y",color=colorfactor1,color_discrete_map=color_discrete_map1,
                             hover_name="Type", text='From', opacity=0.8,
                             range_x=[0, 1], range_y=[0, 1], size='size', size_max=10,
                             hover_data={'Start_X': False, 'Start_Y': False, 'size': False})

        fig.update_traces(marker=dict(
            line=dict(width=1,
                      color='darkgray')),
            selector=dict(mode='markers'))

    # Metrica data starts 0, 0 at top left corner. Need to account for that or markers will be wrong
    fig.update_yaxes(autorange="reversed")

    # Remove side color scale and hide zero and gridlines
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    # Format the title header to be centered
    fig.update_layout(
        title={
            'text': eventType,
            'y': 0.95,
            'x': 0.50,
            'xanchor': 'center',
            'yanchor': 'top'})

    # Make jersey number really small inside markers
    fig.update_traces(textfont_size=7, textfont_color='white')

    # Blank out legend title since we don't really need a title. It's self explanatory
    fig.update_layout(legend_title_text='')

    # Disable zoom. It just distorts and is not fine-tunable. Allowing zoom really messes these
    # graphs up, especially on mobile where the user can touch them accidentally very easily
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    # Position the legend horizontally on bottom
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.08,  # Negative number puts the legend at the bottom
        xanchor="left",
        x=0.05
    ))

    # Disable axis ticks and labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    image_file = 'assets/Pitch.png'
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=.647410)
    from PIL import Image
    img = Image.open(image_file)
    fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=1,
            sizey=1,
            sizing="fill",
            opacity=0.5,
            layer="below")
    )

    fig.update_layout(yaxis=dict(range=[-.05, 1.05]))
    fig.update_layout(xaxis=dict(range=[-.05, 1.05]))
    fig.update_layout(margin=dict(l=10, r=50, b=10, t=30))

    # Sets modebar colour to transparent. If it's black then it looks weird and doesn't match the background colour
    fig.update_layout(modebar=dict(bgcolor='rgba(0, 0, 0, 0)'))

    # Sets background to be transparent
    fig.update_layout(template='plotly_dark',
                      xaxis=dict(
                          showgrid=False,
                          showticklabels=False),
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)'
                      )

    fig.update_layout(
        font_family="Arial",
        title_font_family="Arial"
    )

    fig.update_layout(autosize=True)
    fig.update_layout(showlegend=False)
    fig.update_layout(hovermode="closest")

    return fig


# This part is here in case anybody wants to execute it standalone without Dash, especially for
# troubleshooting purposes
'''if __name__ == "__main__":
    app = dash.Dash()
    eventType = input('Enter event type: ')
    id = input('Enter teamid: ')
    filename = input('Enter event file name: ')
    left_team = input('Which team started on the left side of the pitch?:')
    fig = plotEvents(eventType, filename, id, left_team)
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    app.run_server(debug=True, use_reloader=False)'''
