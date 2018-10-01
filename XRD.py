#coding:utf-8
import cchardet
import re
import numpy as np
import sys
import plotly
import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode(connected = True)
# Global variable
G_title = ''

def SampleName(args:str):
    #print('args is "{0}"' .format(args))
    try:
        f =open(args, 'r')
    except :
        print('FileOpenで[{}]が発生しました。' .format(sys.exc_info()))
        sys.exit(1)


    regSample = r'(Sample)\s*([a-xA-Z0-9_-]+)'
    pattern = re.compile(regSample)
    regData = r'^(?![-+]0+$)[-+]?([1-9][0-9]*)?[0-9](\.[0-9]+)?$'
    patternData = re.compile(regData)
    list_theta = []
    list_int =[]
    getSampleName = False

    for lines in f:
        #print (lines)
        matchSumN = pattern.search(lines)
        if matchSumN:
            SampleName = matchSumN.group(2)
            getSampleName = True
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

    if not getSampleName :
        import os
        SampleName, extension = os.path.splitext(os.path.basename(args) )
    ans_S =''
    print ('Do you change the Sumple name?? -> y / n')
    ans_S = input('>> ')
    while not (ans_S == 'y' or ans_S == 'n'):
            print('Please check yes(y) or not(n)')
            ans_S = input('>> ')
    if ans_S == 'y':
        SampleName = input(SampleName + '>> ')

    print ("Sample Name : {0}" .format(SampleName))
    return (SampleName, list_theta, list_int)

def layout_single(mode:bool) :
    if mode:
        yaxis = 'Intensity / count'
    else :
        yaxis = 'Intensity / arb.unit'
    global G_title
    if G_title == '' or G_title == 'str':
        G_title = 'XRD ploter v0.2.1'

    layout_set = go.Layout(
        title = G_title,
        titlefont = dict(
            size = 24,
            ),
        xaxis =dict(
            title = "2-Theta / 2" + u"\u03B8",
            titlefont=dict(
            family='Arial-Black, sans-serif',
            size=20,
            color='black',
            ),
            tickfont=dict(
            family='Arial-Black, serif',
            size=16,
            color='black'
            ),
            showgrid=False,
            showline = True,
            mirror= 'ticks',
            zeroline=True,
            linewidth=4,
            ticks="inside",
            tickwidth=4,
            #type='log',
        ),
        yaxis =dict(
            title = yaxis,
            titlefont=dict(
            family='Arial-Black, sans-serif',
            size=20,
            color='black',
            ),
            tickfont=dict(
            family='Arial-Black, serif',
            size=16,
            color='black'
            ),
            showgrid=False,
            showline = True,
            mirror= 'ticks',
            zeroline=True,
            linewidth=4,
            ticks="inside",
            tickwidth=4,
            #type='log',
        ),
        #legend=dict(x=0.1, y=1.2, orientation="h"),
        legend=dict(
            traceorder='reversed',
            font = dict(
            size = 14,
            ),
        ),
    )

    return layout_set

def XRDplot(*inpFile:str):
    data =[]
    y_shift = 0
    #print(inpFile)
    #print(len(inpFile))
    if len(inpFile) == 1:
        inp = inpFile[0]
        Sample, theta, int = SampleName(inp)
        if len(theta) != len(int):
            print("x-yの要素数が一致しません。")
            sys.exit(1)

        print ('filemane : {}' .format(Sample))
        trace0 = go.Scatter(
            x = theta,
            y = int,
            mode ='lines',
            name = Sample,
            line = dict(
                #color = ('rgb(205, 12, 24)'),
                width = 2,
                #dash = 'dot'
            )
        )
        data = [trace0]
        layout = layout_single(True)
        fig = go.Figure(data =data, layout = layout)
        #offline.plot(fig, filename = Sample ,image ="png", auto_open=True)
        offline.plot(fig, filename = Sample ,auto_open=True)



    if len(inpFile) > 1:
        filename = ""
        print(' _______________________________________________')
        print('|************* Lets Multiple plot. *************|')
        print('|       How mach do you shift to the y-axis?    |')
        print(' -----------------------------------------------')
        y_shift = input('>> ')
        y_shift = float(y_shift)

        for i, curr_inp in enumerate(inpFile):
            Sample, theta, int = SampleName(curr_inp)
            I_max = (max(int))
            Int_arb = list(map(lambda x: ((x / I_max * 100) + (i*y_shift)), int))
>>>>>>> y-axis_shift_1
            trace = go.Scatter(
                x = theta,
                y = Int_arb,
                name = Sample,
                line = dict(
                    width = 2,
                    )
            )
            if i == 0:
                filename = Sample
            else :
                filename = filename + '_vs_' + Sample
            data +=  [trace]
        layout = layout_single(False)
        fig = go.Figure(data =data, layout = layout)
        offline.plot(fig, filename = filename,auto_open=True)


def Q_title():
    print ('Do you input Graph title? -> y / n ')
    ans = input('>> ')
    return ans

if __name__ == "__main__" :
    args = sys.argv
    args.pop(0)
    ans = ''
    while not (ans == 'y' or ans == 'n'):
        print('Please check yes(y) or not(n)')
        ans = Q_title()
    if ans == 'y':

        print('|***** Input Graph title *****|')
        G_title = input('>> ')
    XRDplot(*args)
