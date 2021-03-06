""" this is layout module for plotly. """
import plotly.graph_objs as go
class PlotLayout:
    def __init__(self, YAXIS='Y-axis', G_title='Title'):
        self._yaxis = YAXIS
        self._gtitle = G_title
        self.playout =go.Layout(
            title =dict(
                text=self._gtitle,
                x=0.5
            ),
            titlefont = dict(
                size = 20,
                ),
            height = 600,
            width = 800,
            plot_bgcolor = 'white',
            margin = dict(
                r=20,
                t=30,
                b=60,
                l=40,
                pad=0,
            ),
            hidesources = True,
            xaxis =dict(
                title = "2-Theta / 2" + u"\u03B8",
                titlefont=dict(
                family='Arial-Black, sans-serif',
                size=22,
                color='black',
                ),
                tickfont=dict(
                family='Arial-Black, serif',
                size=18,
                color='black'
                ),
                linecolor='black',
                showgrid=False,
                showline = True,
                mirror= 'ticks',
                zeroline=True,
                linewidth=4,
                ticks="inside",
                tickwidth=4,
                # autorange = True,
                range=[20, 80],
                #type='log',
            ),
            yaxis =dict(
                title = self._yaxis,
                titlefont=dict(
                family='Arial-Black, sans-serif',
                size=22,
                color='black',
                ),
                tickfont=dict(
                family='Arial-Black, serif',
                size=18,
                color='black'
                ),
                linecolor='black',
                showgrid=False,
                showline = True,
                mirror= 'ticks',
                zeroline=True,
                linewidth=4,
                showticklabels = False,
                ticks="inside",
                tickwidth=4,
                autorange = True,
                # range=[0, 105],
                #type='log',
            ),
            legend=dict(
                x=0.55,
                y=1.0,
                # orientation="h",
                traceorder='reversed',
                font = dict(
                size = 16,
                ),
            ),
        )
