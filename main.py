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

fig = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True
)

fig.update_traces(
    hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>"
)

st.plotly_chart(fig, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 그래프 2. 일관객 합계가 가장 큰 5편 ─────────────────────
st.header("2. 일관객 합계가 가장 큰 5편의 흥행 곡선")

# 영화별 이 기간의 일관객 합계를 계산합니다.
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 일관객 합계가 가장 큰 5편을 선택합니다.
top5_movies = movie_total.head(5).index.tolist()

# 상위 5편의 데이터만 가져옵니다.
top5 = df[df["영화명"].isin(top5_movies)].copy()

# 날짜별·영화별 일관객을 합산합니다.
top5 = (
    top5.groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values(["날짜", "영화명"])
)

# 다섯 영화를 색으로 구분한 선 그래프를 만듭니다.
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

# 범례를 클릭하면 영화를 켜고 끌 수 있습니다.
fig2.update_layout(
    legend_title_text="영화"
)

st.plotly_chart(fig2, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 앞으로 그래프 3, 4, 5가 이 아래에 추가됩니다 ──────────

# ── 그래프 3. 날짜별 10위권 일관객 합계 ──────────────────────
st.header("3. 날짜별 10위권 일관객 합계")

# 날짜별로 그날 10위권 영화의 일관객을 모두 더합니다.
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일을 찾습니다.
top3_days = (
    daily_total
    .sort_values("일관객", ascending=False)
    .head(3)
)

# 영역 그래프
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

# 마우스를 올리면 날짜와 합계가 보이게 합니다.
fig3.update_traces(
    hovertemplate="날짜 %{x|%Y-%m-%d}<br>10위권 일관객 합계 %{y:,}명<extra></extra>"
)

# 가장 큰 3일을 그래프 위에 표시합니다.
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=f"{row['날짜'].strftime('%Y-%m-%d')}<br>{row['일관객']:,}명",
        showarrow=True,
        arrowhead=2,
        yshift=10
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    height=550
)

st.plotly_chart(fig3, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 앞으로 그래프 4, 5가 이 아래에 추가됩니다 ─────────────
# ── 그래프 4. 일관객 합계 TOP 10 ─────────────────────────────
st.header("4. 일관객 합계 TOP 10")

# 영화별 총 관객 수를 계산합니다.
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# 영화별로 10위권에 기록된 날짜 수를 계산합니다.
movie_days = (
    df[df["영화명"].isin(movie_total.index)]
    .groupby("영화명")["날짜"]
    .nunique()
)

# 그래프용 데이터프레임을 만듭니다.
movie_summary = pd.DataFrame({
    "영화명": movie_total.index,
    "총관객": movie_total.values,
    "10위권_일수": movie_days.reindex(movie_total.index).values
})

# 관객이 많은 영화가 그래프 위쪽에 오도록 순서를 뒤집습니다.
movie_summary = movie_summary.sort_values("총관객", ascending=True)

# 가로 막대그래프를 만듭니다.
fig4 = px.bar(
    movie_summary,
    x="총관객",
    y="영화명",
    orientation="h",
    labels={
        "총관객": "일관객 합계",
        "영화명": "영화"
    }
)

# 마우스를 올리면 총 관객 수와 10위권에 든 날수가 보이게 합니다.
fig4.update_traces(
    customdata=movie_summary[["10위권_일수"]],
    hovertemplate=(
        "영화 %{y}"
        "<br>일관객 합계 %{x:,}명"
        "<br>10위권에 든 날수 %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="일관객 합계(명)",
    yaxis_title="영화",
    height=550
)

st.plotly_chart(fig4, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 앞으로 그래프 5가 이 아래에 추가됩니다 ─────────────────
# ── 그래프 5. 월 × 요일별 일관객 합계 히트맵 ─────────────────
st.header("5. 월 × 요일별 일관객 합계")

# 날짜에서 월과 요일을 뽑습니다.
heatmap_data = df.copy()
heatmap_data["월"] = heatmap_data["날짜"].dt.month

# 월요일=0, 화요일=1, ..., 일요일=6
weekday_order = [
    "월요일", "화요일", "수요일",
    "목요일", "금요일", "토요일", "일요일"
]

heatmap_data["요일"] = heatmap_data["날짜"].dt.dayofweek.map(
    dict(enumerate(weekday_order))
)

# 월 × 요일별 일관객을 합산합니다.
heatmap_data = (
    heatmap_data
    .groupby(["월", "요일"], as_index=False)["일관객"]
    .sum()
)

# 피벗해서 히트맵 형태로 만듭니다.
heatmap_table = heatmap_data.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

# 요일을 월요일부터 일요일 순서로 정렬합니다.
heatmap_table = heatmap_table.reindex(columns=weekday_order)

# Plotly 히트맵을 만듭니다.
fig5 = px.imshow(
    heatmap_table,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    x=weekday_order,
    y=heatmap_table.index,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="YlOrRd"
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계 %{z:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    height=550
)

st.plotly_chart(fig5, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
