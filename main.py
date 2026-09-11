# 영화 데이터 그래프 도감 1 - 시간
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)
    # 여덟 자리 숫자로 된 날짜 열을 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

# ── 그래프 1. 영화 하나의 흥행 곡선 ──────────────────────────
st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(df["영화명"].unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")
fig = px.line(one, x="날짜", y="일관객", markers=True)
fig.update_traces(hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>")
st.plotly_chart(fig, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
```python
# 영화 데이터 그래프 도감 1 - 시간
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)
    # 여덟 자리 숫자로 된 날짜 열을 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

# ── 그래프 1. 영화 하나의 흥행 곡선 ──────────────────────────
st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(df["영화명"].unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")
fig = px.line(one, x="날짜", y="일관객", markers=True)
fig.update_traces(
    hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>"
)
st.plotly_chart(fig, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 그래프 2. 일관객 합계 상위 5편의 흥행 곡선 ────────────────
st.header("2. 일관객 합계가 가장 큰 5편")

# 영화별로 이 기간의 일관객을 모두 더합니다.
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 일관객 합계가 가장 큰 5편의 영화명을 가져옵니다.
top5_movies = movie_total.head(5).index.tolist()

# 상위 5편의 데이터만 골라냅니다.
top5 = df[df["영화명"].isin(top5_movies)].copy()

# 날짜와 영화별로 일관객을 정리합니다.
top5 = (
    top5.groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values(["날짜", "영화명"])
)

# 다섯 영화를 색으로 구분한 하나의 선 그래프를 만듭니다.
fig2 = px.line(
    top5,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True
)

# 마우스를 올리면 날짜와 관객수가 보이게 합니다.
fig2.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,}명"
        "<extra>%{fullData.name}</extra>"
    )
)

# 범례를 클릭하면 영화별 선을 켜고 끌 수 있습니다.
fig2.update_layout(
    legend_title_text="영화"
)

st.plotly_chart(fig2, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 앞으로 그래프 3, 4, 5가 이 아래에 추가됩니다 ──────────
```


# ── 앞으로 그래프 2, 3, 4, 5가 이 아래에 추가됩니다 ──────────
