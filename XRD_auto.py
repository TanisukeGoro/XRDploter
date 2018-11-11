#coding:utf-8
import cchardet
import re
import numpy as np
import os
import sys
import plotly
import plotly.offline as offline
import plotly.plotly as py
import plotly.graph_objs as go
# offline.init_notebook_mode(connected = False)
# 以下描画設定
# switch of privacy
SHARING = 'private'
FILEOPT = 'overwrite'
SAVE_DIR= '/Resarch_TsaiLab/XRD/vsCalcu/'
# congigはオフラインプロットのときに使用する。
# CONFIG  = {'showLink': False}

class TxtColor:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

class MsgTxt:
    # 体裁を揃えるために空白行を制御. 天才
    welcome_XRDploter = '\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n' + \
                          '+            Welcome to the XRD graphing program !!           +\n' + \
                          '+                     ver 1.0.0  2018.11.11                   +\n' + \
                          '+                       now configuration                     +\n' + \
                          '+              Sharing     : {0}{1}+\n'.format(SHARING, ' '*(33-len(SHARING))) + \
                          '+              Save dir    : {0}{1}+\n'.format(SAVE_DIR, ' '*(33-len(SAVE_DIR))) + \
                          '+              File update : {0}{1}+\n'.format(FILEOPT, ' '*(33-len(FILEOPT))) + \
                          '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    input_graphtitle  = '\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n' + \
                          '+                      Input Graph title                      +\n' + \
                          '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    multiplot_flag    = '\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n' + \
                          '+                     Lets Multiple plot.                     +\n' + \
                          '+              How mach do you shift to the y-axis?           +\n' + \
                          '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    error_xy_trace    = '\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n' + \
                          '+                           エラー !!                          +\n' + \
                          '+                     x-yの要素数が一致しません。                 +\n' + \
                          '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


color_index = [
    #check the color push coomand + shift + C
    'rgb(37, 154, 255)', # blue
    'rgb(212, 212, 212)', # grey
    'rgb(255, 96, 96)', # red
    'rgb(69, 198, 188)', # blue green
    'rgb(215, 214, 76)', # yellowgreen
    'rgb(27, 157, 26)', # green
    'rgb(250, 10, 16)', # red
    'rgb(212, 23, 255)', # parple
    'rgb(25, 73, 82)', # darkseagreen
    'rgb(194, 126, 185)',
    'rgb()',
    'rgb()',
    'rgb()',
    'rgb()',
    'rgb()',
]

# Global variable
G_title = ''

def get_file_data(args:str):
    print('args is "{0}"' .format(args))
    try:
        f =open(args, 'r')
    except:
        print(TxtColor.RED + 'FileOpenで[{}]が発生しました。'+TxtColor.END .format(sys.exc_info()))
        sys.exit(1)


    regData = r'^(?![-+]0+$)[-+]?([1-9][0-9]*)?[0-9](\.[0-9]+)?$'
    patternData = re.compile(regData)
    list_theta = []
    list_int =[]
    getSampleName = False

    for lines in f:
        int_data = lines.lstrip()
        int_data = lines.rstrip()
        int_data = lines.expandtabs(1)
        theta_int = int_data.split()
        if len(theta_int) == 2:
            thetaTF = patternData.match(theta_int[0])
            intTF = patternData.match(theta_int[1])

        if len(theta_int) == 2 and (thetaTF and intTF):
            theta_value = [float(theta_int[0])]
            int_value = [float(theta_int[1])]
            list_theta.extend (theta_value)
            list_int.extend (int_value)

    f.close()

    inpFile_dir = os.path.dirname(args)
    dirName = inpFile_dir + '/SampleName.txt'
    SNdata = open(dirName, "r")
    lines = SNdata.readlines()
    SNdata.close()
    print (TxtColor.GREEN + "Sample Name: {0}".format(lines[0]) + TxtColor.END )


    return (lines[0], list_theta, list_int)


def layout_single(mode:bool):
    if mode:
        yaxis = 'Intensity / count'
    else:
        yaxis = 'Intensity / arb.unit'
    global G_title

    if G_title == '' or G_title == 'str':
        G_title = 'XRD ploter v0.8.3'

    layout_set = go.Layout(
        title = G_title,
        titlefont = dict(
            size = 16,
            ),
        height = 400,
        width = 600,
        margin = dict(
            r=20,
            t=30,
            b=60,
            l=40,
            pad=0,
        ),
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
            showgrid=False,
            showline = True,
            mirror= 'ticks',
            zeroline=True,
            linewidth=4,
            ticks="inside",
            tickwidth=4,
            # autorange = True,
            range=[20, 90],
            #type='log',
        ),
        yaxis =dict(
            title = yaxis,
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

    return layout_set


def chack_number_of_xy_element(x, y):
    if len(x) != len(y):
        print(TxtColor.RED + MsgTxt.error_xy_trace + TxtColor.END )
        sys.exit(1)

def XRDplot(*input_file_path: str):
    data =[]
    y_shift = 0

    if len(input_file_path) == 1:
        inp = input_file_path[0]
        sample_name, theta, int = get_file_data(inp)
        chack_number_of_xy_element(theta, int)
        print ('filemane: {}' .format(sample_name))
        trace0 = go.Scatter(
            x = theta,
            y = int,
            mode ='lines',
            name = sample_name,
            line = dict(
                #color = ('rgb(205, 12, 24)'),
                color = (color_index[0]),
                width = 2,
                #dash = 'dot'
            )
        )
        data = [trace0]
        filename = SAVE_DIR + sample_name
        layout = layout_single(True)
        fig = go.Figure(data=data, layout=layout)
        pt.plot(fig, filename=filename ,auto_open=True, sharing=SHARING)
        # offline.plot(fig, filename =filename, auto_open=True)
        # offline.plot(fig, filename = filename, image="png", auto_open=True)


    if len(input_file_path) > 1:
        filename = ""
        print (TxtColor.GREEN + MsgTxt.multiplot_flag + TxtColor.END)
        y_shift = input('>> ')
        y_shift = float(y_shift)

        for i, curr_inp in enumerate(input_file_path):
            sample_name, theta, int = get_file_data(curr_inp)
            chack_number_of_xy_element(theta, int)
            I_max = (max(int))
            Int_arb = list(map(lambda x: ((x / I_max * 100) + (i*y_shift)), int))
            trace = go.Scatter(
                x = theta,
                y = Int_arb,
                name = sample_name,
                line = dict(
                    color = (color_index[i]),
                    width = 2,
                    )
            )

            if i == 0:
                filename = sample_name
            else:
                # filename = SAVE_DIR + 'Ru100to70%Comparison'
                filename = SAVE_DIR + filename + '_vs_' + sample_name
            data +=  [trace]

        layout = layout_single(False)
        fig = go.Figure(data =data, layout = layout)

        py.plot(fig,
                filename = filename,
                auto_open=True,
                fileopt=FILEOPT)
        # offline.plot(fig, filename = filename,auto_open=True, config=config)


def Question_title():
    print (TxtColor.BLUE + 'Do you input Graph title? -> y / n ' + TxtColor.END)
    title_name = input('>> ')
    return title_name


if __name__ == "__main__":
    sys.argv.pop(0)
    commandline_argv = sys.argv
    print(TxtColor.BLUE + MsgTxt.welcome_XRDploter + TxtColor.END)
    title_name = ''
    title_name = Question_title()

    while not (title_name == 'y' or title_name == 'n'):
        print(TxtColor.RED + 'Please check yes(y) or not(n)' + TxtColor.END)
        title_name = Question_title()

    if title_name == 'y':
        print(TxtColor.BLUE + MsgTxt.input_graphtitle + TxtColor.END)
        G_title = input('>> ')

    XRDplot(*commandline_argv)
