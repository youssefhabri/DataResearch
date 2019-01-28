#!/usr/bin/python
import re
import os
import sys
import plotly
import plotly.graph_objs as go
import pandas as pd


def plot_chat_graph(filename):
    date = None
    # time = None
    username = None
    # message = None

    users = {}
    dates = []

    # 11/28/17, 00:21 - username: Msg Text
    regex_rule = r'^([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}),\s([0-9]{2}:[0-9]{2})\s-\s(.+?):\s(.+)$'
    p = re.compile(regex_rule)

    with open(filename) as file:
        for line in file:
            m = p.match(line)
            if m:
                date = m.groups()[0]
                # time = m.groups()[1]
                username = m.groups()[2]
                # message = m.groups()[3]
            else:
                # message = line
                pass

            # add new user if not existing
            if users.get(username) is None:
                users[username] = {}

            # Convert date from text to pandas' Timestamp
            key = pd.Timestamp(date)
            # key = pd.Timestamp(date + ' ' + time)

            # Add date to the dates array
            if key not in dates:
                dates.append(key)

            if users[username].get(key) is not None:
                users[username][key] = users[username][key] + 1
            else:
                users[username][key] = 1

    data = []

    for k, v in users.items():
        if k is None:
            continue

        # trace = go.Scatter(
        #     x = dates,
        #     y = pd.Series(v, index=dates).fillna(0),
        #     mode = 'lines+markers',
        #     name = k
        # )

        trace = go.Bar(
            x=dates,
            y=pd.Series(v, index=dates).fillna(0),
            name=k
        )
        data.append(trace)

    layout = go.Layout(
        title='Chat History Graph',
        barmode='group',
        xaxis=dict(
            title='Timeline',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Number of Messages',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )

    plotly.offline.plot({
        'data': data,
        'layout': layout
    }  # , image='svg', image_width=1600, image_height=900
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            plot_chat_graph(sys.argv[1])
        else:
            print('{} is not a valid file!'.format(sys.argv[1]))
    else:
        print("No chat history file have been entered")
