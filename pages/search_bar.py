import streamlit as st

text = st.text_input("애니메이션을 검색하세요")

# text를 입력하는 검색창 하나 만들기
# ani_list에 있는 글자가 일부라도 들어가면
# img_list에 있는 해당 그림이 출력되는 검색창을 하나 만들어주세요
ani_list = ['짱구는못말려', '몬스터','릭앤모티']
img_list = ['https://i.imgur.com/t2ewhfH.png', 
            'https://i.imgur.com/ECROFMC.png', 
            'https://i.imgur.com/MDKQoDc.jpg']

for ani, img in zip(ani_list, img_list):
    if text in ani:
        st.image(img)
