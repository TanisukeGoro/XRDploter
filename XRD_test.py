#coding:utf-8
"""
created 2018.07.06
author Abe keishi
XRD-Ploter ver 0.2
``````````description```````````
引数にファイル名を与えてXRDプロットを行うプログラム
引数が１つの場合は規格化せずそのままプロット
引数が複数の場合は規格化して、y-axisに100ずつのoff-setをかける。
データはtab区切りでも空白区切りでも読み込み可能。
読み込みデータの文字コードはutf-8にすること。
ファイル名に「＃」が入っているとバグる。(サンプル名がファイル名になった時)
`````````````````````````````````
### 今後の方針
- 異なるtheta軸のファイルのプロットに対応(そもそもバグを起こすか未確認)
"""
#文字コードの判定に使いたけど上手くいかないので今後追加する。cchardet
import cchardet
#正規表現のためのモジュール
import re
import numpy as np
#コマンドライン引数の取得用
import sys
#plotlyをimport
import plotly
import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode(connected = True)


#
#````````````2018.07.06```````````````
#ファイル名を受け取り、サンプル名とx-yデータを返す関数
#引数: args　(string型)
#戻値: SampleName, list_int, list_theta
#
#
def SampleName(args:str):
    print('args is "{0}"' .format(args))
    try:
        f =open(args, 'r')
    except :
        print('FileOpenで[{}]が発生しました。' .format(sys.exc_info()))
        sys.exit(1)


    #正規表現の事前コンパイル。実行速度が少し早くなるはず。regは正規表現の頭文字
    regSample = r'(Sample)\s*([a-xA-Z0-9_-]+)'
    pattern = re.compile(regSample)
    #正規表現で整数, 小数, 浮動小数点数に対応して数値の分離を試みたが難しいようだ。
    #仕方ないので文字列がint, float型にキャスト可能か判定することで対応する。2018.07.06
    #regData = r'\s*(^-?\d+?\.\d+?$)\s*(^-?\d+?\.\d+?$)'
    #regData =r'\s*([+-]?[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?)\s*([+-]?[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?)'
    #patternData = re.compile(regData)
    #正規表現で数値かどうか判定 2018.07.07 10:45追加
    regData = r'^(?![-+]0+$)[-+]?([1-9][0-9]*)?[0-9](\.[0-9]+)?$'
    patternData = re.compile(regData)

    #出力用のデータを事前に配列として宣言する。
    list_theta = []
    list_int =[]
    getSampleName = False

    for lines in f:
        #regular expressiona(正規表現)によるマッチング
        #サンプル名を取得 groupメソッドは(0)は元の文字列, (1)以降は正規表現にヒットした文字列
        matchSumN = pattern.search(lines)
        if matchSumN:
            #print (matchSumN.group(2))
            SampleName = matchSumN.group(2)
            getSampleName = True

        #theta, intensity取得の為の前処理
        #先頭と末尾の空白があれば削除
        int_data = lines.lstrip()
        int_data = lines.rstrip()

        #2018.07.19
        #tab区切りから空白区切りに変更。tabを空白に変換してから空白区切りにすれば
        #tab区切りデータも空白区切りデータも両方扱える。
        int_data = lines.expandtabs(1)
        theta_int = int_data.split()

        #2-columnかつ区切られた2つが数値であればx-yデータとして取得
        #isdigitはintのみにtrueになる。floatはfalseになる。ファック
        #以下の正規表現で数値か否かをboolean型のthetaTF, intTFに代入
        if len(theta_int) == 2:
            thetaTF = patternData.match(theta_int[0])
            intTF = patternData.match(theta_int[1])

        if len(theta_int) == 2 and (thetaTF and intTF):
            #floatにキャスト
            theta_value = [float(theta_int[0])]
            int_value = [float(theta_int[1])]
            #listにする
            list_theta.extend (theta_value)
            list_int.extend (int_value)

    f.close()

    #もしSample名が取得できなかった場合はファイル名をサンプル名とする。
    #ファイル名を取得するためにosライブラリをインポート
    if not getSampleName :
        import os
        SampleName, extension = os.path.splitext(os.path.basename(args) )



    return (SampleName, list_theta, list_int)

def layout_single(mode:bool) :
    #グラフのレイアウト決定用の関数。
    #引数にboolean型を使用。
    if mode:
        yaxis = 'Intensity / count'
    else :
        yaxis = 'Intensity / arb.unit'

    layout_set = go.Layout(
        xaxis =dict(
            #軸ラベルのthetaはUnicodeで記述する。
            title = "2-Theta / 2" + u"\u03B8",
            #軸ラベルのフォント指定
            titlefont=dict(
            family='Arial-Black, sans-serif',
            size=18,
            color='black',
            ),
            #軸の数値の書式設定
            showgrid=False,#グリッド線の描画
            showline = True,#軸の線の描画
            mirror= 'ticks', #軸線の鏡映(枠線にする)
            zeroline=True, # y=0の線を描画
            linewidth=4, #軸の太さ
            ticks="inside", # 目盛線-内側
            type='log',#対数軸に変更
        ),
        yaxis =dict(
            #軸ラベルのthetaはUnicodeで記述する。
            title = yaxis,
            #軸ラベルのフォント指定
            titlefont=dict(
            family='Arial-Black, sans-serif',
            size=18,
            color='black',
            ),
            #軸の数値の書式設定
            tickfont=dict(
            family='Arial-Black, serif',
            size=16,
            color='black'
            ),
            showgrid=False, #グリッド線の描画
            showline = True, #軸線の描画
            mirror= 'ticks', #軸線の鏡映(枠線にする)
            zeroline=True, # x=0の線を描画
            linewidth=4,
            type='log',#対数軸に変更
            ticks="inside", # 目盛線-内側

        ),
        legend=dict(x=0.1, y=1.2, orientation="h"),#凡例を一行に並べる。,凡例の位置を変更する。

    )

    return layout_set


#複数ファイルに対応する為に可変長引数とする。
def XRDplot(*inpFile:str):
    #plotデータ用の変数。listとして宣言
    data =[]
    #要素の出力
    print(inpFile)
    #タプルの数をカウント
    print(len(inpFile))
    #input file が１つなら規格化をせずにそのままプロット
    if len(inpFile) == 1:
        inp = inpFile[0]
        #引数にFile pathを与えて戻値としてSample名とx-yデータを受け取る、
        Sample, theta, int = SampleName(inp)

        #theta, intの要素数が一致しているか確認
        #一致していなければエラーを出力して終了。
        if len(theta) != len(int):
            print("x-yの要素数が一致しません。")
            sys.exit(1)

        trace0 = go.Scatter(
        x = theta,
        y = int,
        mode ='lines',
        name = Sample
        )
        data = [trace0]
        """
        もしブラウザ上にプロットしたい時は、
        offline.plot()のオプションに auto_opne = True を使う。
        こっちのが画面が大きくていいかもてかコマンドラインで実行する場合にいいのかもしれない。
        そうでもなければoffline.iplot()で実行すればよろし。この場合はコマンドラインからの実行には対応できない。と思う。
        """
        #グラフのレイアウトを指定
        layout = layout_single(True)
        fig = go.Figure(data =data, layout = layout)
        offline.plot(fig, filename = Sample ,image ="png", auto_open=True)

    if len(inpFile) > 1:
        #forの中でスコープされてしまうのでここで空の文字列を宣言しパブリク化する。
        filename = ""
        for i, curr_inp in enumerate(inpFile):
            Sample, theta, int = SampleName(curr_inp)
            #print('count i is [{0}]' .format(i))
            #最大強度の取
            I_max = (max(int))
            #print('Imax : %f' % I_max)
            #map関数を用いてlist全体に規格化を適用。戻り値はシーケンスになっているのでlistに変換して取得する。また、lammda式によって式を表現している。
            #i個目のデータはy-axis offsetをかけている
            Int_arb = list(map(lambda x: (x / I_max * 100) + (i)*100, int))
            trace = go.Scatter(
            x = theta,
            y = Int_arb,
            #mode ='lines',
            name = Sample
            )
            if i == 0:
                filename = Sample
            else :
                filename = filename + '_vs_' + Sample
            data +=  [trace]
        layout = layout_single(False)
        fig = go.Figure(data =data, layout = layout)
        offline.plot(fig, filename = filename, image ="png",auto_open=True)

#CやJacaでいうmain関数的な。他のモジュールからインポートした時は使えないので注意。
if __name__ == "__main__" :
    #引数を取得
    args = sys.argv
    #取得した第一引数はpythonのファイル名なので削除
    args.pop(0)
    #引数にアスタリスクを付けることでリストやタルプを展開して渡すことができる。
    XRDplot(*args)
    #XRDplot(args)
