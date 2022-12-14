import streamlit as st
import os
import time
import pandas as pd
import plotly.express as px
from pathlib import Path
from overcatch import OverCatch
# from io import BytesIO

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# local path
filepath ='C:/Python/repos_python/streamlit_bluescreen/bluescreen/'
# colab path
# filepath ='/content/streamlit_bluescreen/'

# set page
st.set_page_config(
    page_title="OVERCATCH",
    page_icon="๐ฎ",
    layout="wide",
)
st.title("๐ฎ OVERCATCH")
# st.header("Let's do this!")
with st.sidebar :
    # st.markdown("## Catch the hack together๐ค")
    code = '''
import random

members = [
'์ฅ๊ทํ๐',
'๊ณฝํ์๐ป',
'๊น๊ฐ์ฐ๐๏ธ',
]

def hello():
    print("Hello, World!")
    print("We're TEAM BLUESCREEN")

    for i in range(0, 3):
        print(f'{i+1}๋ฒ ๊ฐ์ 
            {random.randint(20000000, 
            20221026)} {members[i]}')
        if i == 2:
            print("๋ฒํธ ๋!")

hello()
-------------------------------------
>> Hello, World!
   We're TEAM BLUESCREEN
   1๋ฒ ๊ฐ์ 20171119 ์ฅ๊ทํ๐
   2๋ฒ ๊ฐ์ 20181457 ๊ณฝํ์๐ป
   3๋ฒ ๊ฐ์ 20191012 ๊น๊ฐ์ฐ๐๏ธ
   ๋ฒํธ ๋!
        '''
    st.code(code, language='python')
    
st.subheader("Step 1๏ธโฃ Upload a video that you want to know")

# ํด๋์ ํ์ผ์ ์ฃผ๋ฉด, ํด๋น ํด๋์ ํ์ผ์ ์ ์ฅํ๋ ํจ์
def save_uploaded_file(directory, file):
    # ํด๋ ํ์ธ
    if not os.path.exists(directory):
        os.makedirs(directory)
        # print("done to make directory")
    # ํด๋์ ํ์ผ ์ ์ฅ
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
        # print("done to save original video")
    return st.success('Saved file : {} in {}'.format(file.name, directory))

# ์ด๋ ๊ฒ ํด๋ ์นํ์ด์ง ์๋ก๊ณ ์นจ ์ ๋ฐ์ดํฐ ๋ฐ์ดํฐ ์ด๊ธฐํ ๋จ > DB ์จ์ผ ํด๊ฒฐ๋ ๋ฏ
if 'resultdict' not in st.session_state:
    st.session_state.resultdict = dict()

if 'latestvideo' not in st.session_state:
    st.session_state.latestvideo = ''

if 'seqdict' not in st.session_state:
    st.session_state.seqdict = dict()

if 'targetdict' not in st.session_state:
    st.session_state.targetdict = dict()

uploaded_file = st.file_uploader("Upload Video about a minute long", type=['mp4'])
if uploaded_file is not None:
    save_uploaded_file('original', uploaded_file)
    # print("done to video upload")

    # yolo > lstm ํต๊ณผ
    # result_dict์ file.name, percentage ์ ์ฅ ๋ฐ ๋ฐํ
    with st.spinner('YOLO is working pretty hard...'):
        # time.sleep(500)
        oc = OverCatch(uploaded_file.name)
        # float
        per, seq, chr = oc.predict()
        # print("YOLO IS DONE")
        # ๋ชจ๋ธ ํต๊ณผํ๋ค๊ณ  ๊ฐ์ ํ ์ดํ ์ฝ๋. page2์ history gallery์ ๋์ผํ๊ฒ ์ฌ์ฉ
        st.session_state.resultdict[f"{uploaded_file.name}"] = per
        # print(st.session_state.resultdict)
        st.session_state.latestvideo = Path(f"{uploaded_file.name}").stem
        # print(st.session_state.latestvideo)
        st.session_state.seqdict[f'{st.session_state.latestvideo}'] = seq
        # print(st.session_state.seqdict)
        st.session_state.targetdict[f'{st.session_state.latestvideo}'] = chr
        # print(st.session_state.targetdict)
    st.success("YOLO IS DONE!")


if len(st.session_state.resultdict) != 0:
    # make a horizontal line
    st.write("ใฐ๏ธ" * 62)
    st.subheader("Step 2๏ธโฃ Watch this video")
    st.markdown("#### We truly created about 60,000 custom datasets for yolov5 model ourselves๐ฆ")
    
    # ์์ ๋์ฐ๊ธฐ
    # st.markdown("### Finished to detect OVERWATCH characters using YOLOv5")
    fp = f"{filepath}result/{str(Path(st.session_state.latestvideo).stem)}/{st.session_state.latestvideo}.mp4"
    # print("full file path : "+fp)

    st.markdown("<h1 style='text-align: center; color: grey;'>PLAY NOW ๐</h1>", unsafe_allow_html=True)

    video_file = open(fp, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    if uploaded_file is not None:
        with st.spinner('LSTM is working now...'):
            time.sleep(3)
        st.success('LSTM IS DONE!')

    hackper = st.session_state.resultdict[f"{st.session_state.latestvideo}.mp4"]
    df = pd.DataFrame(
        {
            "Normal": [1-hackper],
            "Hack": [hackper],
        }
    )

    st.write("ใฐ๏ธ" * 62)
    st.subheader("Step 3๏ธโฃ Lets check the probability of hack")

    left, right = st.columns((7,3))
    with left:
        st.text("\n")
        st.text("\n")
        st.text("\n")
        st.text("\n")
        chart_data = pd.DataFrame(
        data = st.session_state.seqdict[f'{st.session_state.latestvideo}'],
        columns = [st.session_state.targetdict[f'{st.session_state.latestvideo}']])
        st.line_chart(chart_data)
        # st.markdown(f'### It is {int(hackper*100)}% hack')

    with right:
        fig=px.bar(df, labels={'index': ' ', 'value':'percentage'})
        st.plotly_chart(fig, use_container_width=True)
    
    if hackper >= 0.5:
        st.markdown("<h2 style='text-align: center; color: #FF5733;'>โ ๏ธ Ohhhh WHAT THE HACK! ๐ฎโโ๏ธ</h2>", unsafe_allow_html=True)
        # st.markdown("## โ ๏ธ _Hmmm.. THIS IS A CHEATER!_ ๐ฎโโ๏ธ")
    else: st.markdown("<h2 style='text-align: center; color: #DAF7A6;'>๐ Hooooray! SUCH A NICE GAMER ๐</h2>", unsafe_allow_html=True)
        # st.markdown("## ๐ _SUCH A NICE GAMER_ ๐")
    
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.write("ใฐ๏ธ" * 62)



    # st.write(st.session_state.resultdict)