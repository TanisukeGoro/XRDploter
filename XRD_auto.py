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
import plotly.offline as offline
import plotly.plotly as py
import plotly.graph_objs as go
# offline.init_notebook_mode(connected = False)
# 以下描画設定
# switch of privacy
# PLTMODE = 'online'
# SAVE_DIR= '/Resarch_TsaiLab/XRD/APCR/'
SHARING = 'private'
FILEOPT = 'overwrite' #new or abs

PLTMODE = 'offline'
SAVE_DIR= ''

# SAVE_DIR= '/Resarch_TsaiLab/XRD/Al72Pd16.4RuFe11.6/N10_N11_N17/900C/'
# SAVE_DIR = '/Volumes/KEISHI_2018/1.M1/1.修士研究/2.実験データ/1.XRD/SpecimenNo17/#13N17_20181206_950_48h/'
msg1 = MsgTxt(PLTMODE=PLTMODE, SHARING=SHARING, FILEOPT=FILEOPT, SAVE_DIR=SAVE_DIR)
# congigはオフラインプロットのときに使用する。
CONFIG  = {'showLink': False}

# Global variable
graph_title = 'XRD auto-ploter v1.0.0'
G_title =''
# G_title = 'Al<sub>72.0</sub>Pd<sub>16.4</sub>(Ru<sub>(100-x)%</sub>, Fe<sub>x%</sub>)<sub>11.4</sub>,1273K 48h; x = 100, 80, 75, 70 '
G_title = 'Al<sub>72.0</sub>Pd<sub>16.4</sub>(Ru<sub>(100-x)%</sub>, Fe<sub>x%</sub>)<sub>11.4</sub>'

def check_input_yesno(answer:str):
    while not (answer == 'y' or answer == 'n'):
        print(TerminalFontColor.RED + 'Please check yes(y) or not(n)' + TerminalFontColor.END)
        answer = input('>> ')
    return answer


def get_file_data(file_path:str):

    print('File is "{0}"' .format(os.path.basename(file_path)))
    try:
        f =open(file_path, 'r')
    except:
        print(TerminalFontColor.RED + \
        "FileOpenで[{0}]が発生しました。".format(sys.exc_info()) + \
        TerminalFontColor.END)
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
    if os.path.isfile(dirName):
        SNdata = open(dirName, "r")
        SampleName_text = SNdata.readlines()
        SNdata.close()
        print (TerminalFontColor.GREEN + "Sample Name: {0}".format(SampleName_text[0]) + \
         TerminalFontColor.END )
    else:
        print(TerminalFontColor.RED + 'SampleName.txt is not exist !!' + TerminalFontColor.END)
        print (TerminalFontColor.RED + "XRD_auto.py is exit." + TerminalFontColor.END)
        sys.exit()

    return (SampleName_text[0], list_theta, list_int)


def layout_single(mode:bool):
    if mode:
        yaxis = 'Intensity / count'
    else:
        yaxis = 'Intensity / arb.unit'
    global G_title

    if G_title == '' or G_title == 'str':
        G_title = graph_title

        print(TerminalFontColor.RED + msg1.no_setting_Gtitle + TerminalFontColor.END)
        doset_graphtitle = input('>> ')
        doset_graphtitle = check_input_yesno(doset_graphtitle)
        print(doset_graphtitle)
        if doset_graphtitle == 'y':
            print(TerminalFontColor.BLUE + msg1.input_graphtitle + TerminalFontColor.END)
            G_title = input('>> ')

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
        # chack_len =TerminalFontColor.RED + msg1.plot_file_name(fname) +TerminalFontColor.END
        chack_len =msg1.plot_file_name(fname)
        # print(chack_len.caution_charleng)
        change_fileYN = input('>> ')
        change_fileYN = check_input_yesno(change_fileYN)

        if change_fileYN == 'y':
            print(TerminalFontColor.BLUE + msg1.input_filename + TerminalFontColor.END)
            fname = input('>> ')

    return fname


def goXRDplot(*input_file_path: str):
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
        if PLTMODE =='online':
            py.plot(fig, filename=filename ,auto_open=True, sharing=SHARING)
        else:
            offline.plot(fig, filename = filename,auto_open=True, config=CONFIG)
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
            if I_max == 0:
                Int_arb = list(map(lambda x: (x + (i*y_shift)), int))
            else:
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

        # filename = "Al<sub>72.0</sub>Pd<sub>16.4</sub>(Ru<sub>(100-x)%</sub>, Fe<sub>x%</sub>)<sub>11.4</sub>; 900 C48h, 1000C 48h, 1000C, 720h"
        filename = chack_filename_length(filename)
        filename = SAVE_DIR + filename

        layout = layout_single(False)
        fig = go.Figure(data =data, layout = layout)

        if PLTMODE =='online':
            py.plot(fig, filename = filename, auto_open=True, fileopt=FILEOPT, sharing=SHARING)
        else:
            offline.plot(fig, filename = filename,auto_open=True, config=CONFIG)


if __name__ == "__main__":
    sys.argv.pop(0)
    commandline_argv = sys.argv
    msg1.msgbox()
    print(TerminalFontColor.BLUE + str(msg1) + TerminalFontColor.END)
    print (TerminalFontColor.BLUE + 'Do you input Graph title? -> y / n ' + TerminalFontColor.END)
    # graph title
    title_name = 'y'
    title_name = check_input_yesno(title_name)

    if title_name == 'y':
        print(TerminalFontColor.BLUE + msg1.input_graphtitle + TerminalFontColor.END)
        # G_title = input('>> ')
        print ('>> ' + G_title)

    goXRDplot(*commandline_argv)
