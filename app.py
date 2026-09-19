import streamlit as st
import pandas as pd
import requests

DATA_URL = "https://tourism.api.opendatahub.com/v1/Accommodation"


# Load data from API
@st.cache_data
def load_data():

    all_items = []

    for page in range(1, 18):

        response = requests.get(
            DATA_URL,
            params={
                "pagesize": 1000,
                "pagenumber": page
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        all_items.extend(data["Items"])

    df = pd.DataFrame(all_items)

    # Extract municipality
    df["Municipality"] = df["LocationInfo"].apply(
        lambda x: x["MunicipalityInfo"]["Name"]["it"]
    )

    # Extract accommodation type
    df["AccommodationType"] = df["AccoTypeId"]

    return df


# Title
st.title("South Tyrol Accommodation Explorer")

st.write(
    "Explore where accommodation options are most concentrated "
    "and what types of accommodation are available."
)


# Load data
try:
    df = load_data()

except requests.exceptions.RequestException:
    st.error(
        "The accommodation data is currently unavailable. "
        "Please try again later."
    )
    st.stop()


# Top 10 municipalities
top_10 = df["Municipality"].value_counts().head(10)

st.subheader("Top 10 municipalities by number of accommodations")

st.bar_chart(top_10)


# Interactive selection
selected_municipality = st.selectbox(
    "Choose a municipality to explore:",
    top_10.index
)


# Filter data
filtered_df = df[
    df["Municipality"] == selected_municipality
]


# Accommodation types
type_counts = filtered_df["AccommodationType"].value_counts()

st.subheader(
    f"Accommodation types in {selected_municipality}"
)

st.bar_chart(type_counts)


# Limitation
st.info(
    "Limitation: the API does not provide accommodation prices, "
    "so the app cannot compare prices or affordability."
)
