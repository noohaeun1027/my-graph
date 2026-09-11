import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("365일 동안 영화별 일관객 수가 어떻게 변했는지 살펴보는 그래프입니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # UTF-8 계열 인코딩을 우선 사용
    try:
        df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_URL, encoding="utf-8")

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 열을 숫자로 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # 날짜순으로 정렬
    df = df.sort_values(["날짜", "순위"])

    return df


df = load_data()


# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
if df.empty:
    st.error("데이터를 불러오지 못했습니다.")
    st.stop()


# ==================================================
# 그래프 1
# ==================================================
st.divider()
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 365일 동안 그 영화의 일관객 수가 "
    "어떻게 변했는지 볼 수 있습니다."
)

# 영화 목록 만들기
movie_list = sorted(
    df["영화명"]
    .dropna()
    .astype(str)
    .unique()
)

selected_movie = st.selectbox(
    "🎞️ 영화를 선택하세요",
    movie_list
)

# 선택한 영화만 추출
movie_df = df[df["영화명"].astype(str) == selected_movie].copy()

# 같은 날짜에 여러 기록이 있을 경우 날짜별 일관객 합계
movie_daily = (
    movie_df
    .groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 선 그래프
fig = px.line(
    movie_daily,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

# 마우스를 올렸을 때 날짜와 관객수가 보이도록 설정
fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,.0f}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "이 그래프를 통해 선택한 영화의 날짜별 관객 수 변화와 "
    "관객이 많았던 시점 및 적었던 시점을 알 수 있습니다."
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()
st.header("📊 그래프 2. 앞으로 추가할 그래프")

st.info("여기에 두 번째 그래프를 추가할 예정입니다.")


st.divider()
st.header("📊 그래프 3. 앞으로 추가할 그래프")

st.info("여기에 세 번째 그래프를 추가할 예정입니다.")
