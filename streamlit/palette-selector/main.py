import polars as pl
from great_tables import GT, html
from great_tables.data import sza

import streamlit as st


@st.cache_data
def get_sza():
    return pl.from_pandas(sza)


def get_sza_gt():
    sza_pivot = (
        get_sza()
        .filter((pl.col("latitude") == "20") & (pl.col("tst") <= "1200"))
        .select(pl.col("*").exclude("latitude"))
        .drop_nulls()
        .pivot(values="sza", index="month", on="tst", sort_columns=True)
    )

    return (
        GT(sza_pivot, rowname_col="month")
        .data_color(
            domain=[90, 0],
            palette=[color1, "white", color2],
            na_color="white",
        )
        .tab_header(
            title="Solar Zenith Angles from 05:30 to 12:00",
            subtitle=html("Average monthly values at latitude of 20&deg;N."),
        )
        .sub_missing(missing_text="")
    )


st.title("Great Tables shown in Streamlit")

_, col1, _, col2, _ = st.columns([1, 1, 1, 1, 1])
with col1:
    color1 = st.color_picker("Color 1", "#663399")
with col2:
    color2 = st.color_picker("Color 2", "#FFA500")

st.write(get_sza_gt().as_raw_html(), unsafe_allow_html=True)
