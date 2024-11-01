import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# タイトル
st.title("散布図作成アプリ")

# CSVファイルのアップロード
uploaded_file = st.sidebar.file_uploader("CSVファイルをアップロードしてください", type="csv")

# ファイルがアップロードされた場合
if uploaded_file is not None:
    # CSVファイルを読み込む
    df = pd.read_csv(uploaded_file)
    st.write("アップロードされたデータフレーム:")
    st.dataframe(df)

    # サイドバーにX軸とY軸の選択
    x_axis = st.sidebar.selectbox('X軸に使用する列を選択してください', df.columns)
    y_axis = st.sidebar.selectbox('Y軸に使用する列を選択してください', df.columns)

    # プロットサイズをサイドバーのスライダーで調整
    marker_size = st.sidebar.slider('プロットのサイズを調整してください', 5, 20, 10)

    # チェックボックスでカテゴリ列を選ぶかサイドバーで設定
    color_check = st.sidebar.checkbox('群ごとに色分けしますか？')
    color_col = None
    
    if color_check:
        # 群分けに使う列をサイドバーで選択
        color_col = st.sidebar.selectbox('色分けに使用する列を選択してください', df.columns)

    # 散布図をプロットする
    if color_col:
        # 群ごとに色を変える場合
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, 
                         title=f'{x_axis} vs {y_axis}の散布図（色分け）', 
                         size_max=marker_size)
    else:
        # 群分けしない場合
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{x_axis} vs {y_axis}の散布図', 
                         size_max=marker_size)

    # プロットのサイズをスライダーで調整
    fig.update_traces(marker=dict(size=marker_size))

    # 回帰直線の計算
    x = df[x_axis]
    y = df[y_axis]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # 回帰式の作成
    regression_line = slope * x + intercept

    # 回帰直線を散布図に追加
    fig.add_scatter(x=x, y=regression_line, mode='lines', name='回帰直線')

    # プロットの設定
    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_zeroline=True,
        yaxis_zeroline=True,
        xaxis_zerolinecolor='black',
        yaxis_zerolinecolor='black',
        xaxis_linecolor='black',
        yaxis_linecolor='black',
        xaxis_ticks='outside',
        yaxis_ticks='outside',
        font=dict(size=18),  # グラフ全体のフォントサイズをさらに大きく
        xaxis=dict(
            titlefont=dict(size=24, color='black'),  # X軸ラベルのフォントサイズを大きく、色を黒に設定
            tickfont=dict(size=20, color='black'),  # X軸の数値のフォントサイズを大きく、色を黒に設定
            linewidth=3,              # X軸の線を太く
            ticks='outside',
            dtick=None,  # 自動設定
        ),
        yaxis=dict(
            titlefont=dict(size=24, color='black'),  # Y軸ラベルのフォントサイズを大きく、色を黒に設定
            tickfont=dict(size=20, color='black'),  # Y軸の数値のフォントサイズを大きく、色を黒に設定
            linewidth=3,              # Y軸の線を太く
            ticks='outside',
            dtick=None,  # 自動設定
        ),
        height=600,  # 縦横比を1:1にするため高さを設定
        width=600,   # 縦横比を1:1にするため幅を設定
    )

    # グラフを表示
    st.plotly_chart(fig)

    # 回帰式、相関係数、有意差をグラフの下に表示
    correlation_text = (
        f"回帰式: y = {slope:.2f}x + {intercept:.2f}<br>"
        f"相関係数 (R): {r_value:.2f}<br>"
        f"p値: {p_value:.4f}<br>"
    )
    
    if p_value < 0.05:
        correlation_text += "有意な相関があります (p < 0.05)"
    else:
        correlation_text += "有意な相関はありません (p ≥ 0.05)"

    # 回帰式、相関係数、有意差をグラフの下に表示
    st.markdown(correlation_text, unsafe_allow_html=True)

else:
    st.sidebar.write("CSVファイルをアップロードしてください。")
