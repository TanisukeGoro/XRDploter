#coding:utf-8
from module.msgtxt import MsgTxt
from module.plotlayout import PlotLayout
from module.color_config import TerminalFontColor
from module.color_config import PlotColor

import cchardet
import re
import numpy as np
import os
import sys
import plotly
# import plotly.offline as offline
import plotly.plotly as py
import plotly.graph_objs as go
# offline.init_notebook_mode(connected = False)
# 以下描画設定
# switch of privacy
PLTMODE = 'online'
SHARING = 'private'
FILEOPT = 'overwrite' #new or abs
SAVE_DIR= '/Resarch_TsaiLab/XRD/AlPdRuFe_compare/'
msg1 = MsgTxt(PLTMODE=PLTMODE, SHARING=SHARING, FILEOPT=FILEOPT, SAVE_DIR=SAVE_DIR)
# congigはオフラインプロットのときに使用する。
# CONFIG  = {'showLink': False}

# Global variable
graph_title = 'XRD auto-ploter v1.0.0'
G_title =''
# G_title = 'Al<sub>72.0</sub>Pd<sub>16.4</sub>(Ru<sub>(100-x)%</sub>, Fe<sub>x%</sub>)<sub>11.4</sub>,1273K 48h; x = 100, 80, 75, 70 '

def get_file_data(file_path:str):

    print('File is "{0}"' .format(os.path.basename(file_path)))
    try:
        f =open(file_path, 'r')
    except:
        print(TerminalFontColor.RED + 'FileOpenで[{}]が発生しました。'+TerminalFontColor.END .format(sys.exc_info()))
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

    inpFile_dir = os.path.dirname(file_path)
    dirName = inpFile_dir + '/SampleName.txt'
    SNdata = open(dirName, "r")
    lines = SNdata.readlines()
    SNdata.close()
    print(lines)
    # lines = ['11', '1223']
    print (TerminalFontColor.GREEN + "Sample Name: {0}".format(lines[0]) + TerminalFontColor.END )


    return (lines[0], list_theta, list_int)


def layout_single(mode:bool):
    if mode:
        yaxis = 'Intensity / count'
    else:
        yaxis = 'Intensity / arb.unit'
    global G_title

    if G_title == '' or G_title == 'str':
        G_title = graph_title
    layout_set = PlotLayout(YAXIS=yaxis, G_title=G_title)
    # print (layout_set.playout)
    # print (layout_set)
    return layout_set.playout


def chack_number_of_xy_element(x, y):
    if len(x) != len(y):
        print(TerminalFontColor.RED + msg1.error_xy_trace + TerminalFontColor.END)
        sys.exit(1)


def chack_filename_length(fname: str):

    if len(fname) > 35:
        chack_len =TerminalFontColor.RED + msg1.plot_file_name(fname) +TerminalFontColor.END
        print(chack_len.caution_charleng)
        change_fileYN = input('>> ')

        while not (change_fileYN == 'y' or change_fileYN == 'n'):
            print(TerminalFontColor.RED + 'Please check yes(y) or not(n)' + TerminalFontColor.END)
            change_fileYN = input('>> ')

        if change_fileYN == 'y':
            print(TerminalFontColor.BLUE + msg1.input_filename + TerminalFontColor.END)
            fname = input('>> ')

    return fname


def XRDplot(*input_file_path: str):
    data =[]
    y_shift = 0

    if len(input_file_path) == 1:
        inp = input_file_path[0]
        sample_name, theta, int = get_file_data(inp)
        chack_number_of_xy_element(theta, int)
        print ('filemane: {}'.format(sample_name))
        trace0 = go.Scatter(
            x = theta,
            y = int,
            mode ='lines',
            name = sample_name,
            line = dict(
                #color = ('rgb(205, 12, 24)'),
                color = (PlotColor.color_index[0]),
                width = 2,
                #dash = 'dot'
            )
        )
        data = [trace0]
        filename = sample_name
        filename = chack_filename_length(filename)
        filename = SAVE_DIR + sample_name
        layout = layout_single(True)
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename=filename ,auto_open=True, sharing=SHARING)
        # offline.plot(fig, filename =filename, auto_open=True)
        # offline.plot(fig, filename = filename, image="png", auto_open=True)


    if len(input_file_path) > 1:
        filename = ""
        print (TerminalFontColor.GREEN + msg1.multiplot_flag + TerminalFontColor.END)
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
                    color = (PlotColor.color_index[i]),
                    width = 2,
                    )
            )

            if i == 0:
                filename = sample_name
            else:
                # filename = SAVE_DIR + 'Ru100to70%Comparison'
                filename = filename + '_vs_' + sample_name
            data +=  [trace]

        filename = chack_filename_length(filename)
        filename = SAVE_DIR + filename

        layout = layout_single(False)
        fig = go.Figure(data =data, layout = layout)

        if PLTMODE =='online':
            py.plot(fig, filename = filename, auto_open=True, fileopt=FILEOPT, sharing=SHARING)
        else:
            offline.plot(fig, filename = filename,auto_open=True, config=config)

if __name__ == "__main__":
    sys.argv.pop(0)
    commandline_argv = sys.argv
    msg1.msgbox()
    print(TerminalFontColor.BLUE + str(msg1) + TerminalFontColor.END)
    print (TerminalFontColor.BLUE + 'Do you input Graph title? -> y / n ' + TerminalFontColor.END)
    title_name = 'y'

    while not (title_name == 'y' or title_name == 'n'):
        print(TerminalFontColor.RED + 'Please check yes(y) or not(n)' + TerminalFontColor.END)
        title_name = input('>> ')

    if title_name == 'y':
        print(TerminalFontColor.BLUE + msg1.input_graphtitle + TerminalFontColor.END)
        # G_title = input('>> ')
        print ('>> ' + G_title)

    XRDplot(*commandline_argv)
