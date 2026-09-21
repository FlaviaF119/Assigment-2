import pandas as pd
import requests
import matplotlib.pyplot as plt
import streamlit as st


# API
DATA_URL = "https://tourism.api.opendatahub.com/v1/Accommodation"


# Download data
all_items = []

for page in range(1, 18):

    response = requests.get(
        DATA_URL,
        params={
            "pagesize": 1000,
            "pagenumber": page
        }
    )

    if response.status_code == 200:
        data = response.json()
        all_items.extend(data["Items"])
    else:
        st.error("The API is currently unavailable.")
        st.stop()


df = pd.DataFrame(all_items)

if df.empty:
    st.info("There is currently no data available to display.")
    st.stop()


# Function to get municipality
def get_municipality(x):
    try:
        return x["MunicipalityInfo"]["Name"]["it"]
    except (TypeError, KeyError):
        return "Unknown"


# Create Municipality column
df["Municipality"] = df["LocationInfo"].apply(
    get_municipality
)


# Function to get accommodation type
def get_accommodation_type(x):
    try:
        return x["Id"]
    except (TypeError, KeyError):
        return "Unknown"


# Create AccommodationType column
df["AccommodationType"] = df["AccoType"].apply(
    get_accommodation_type
)


# Count accommodations by municipality
municipality_counts = df["Municipality"].value_counts()


# -----------------------------
# STREAMLIT APP
# -----------------------------

st.title("Accommodation Dashboard")

st.write(
    "Explore the types of accommodation available in each municipality."
)


# Choose a municipality
selected_municipality = st.selectbox(
    "Choose a municipality",
    municipality_counts.index
)


# Filter the data
filtered_df = df[
    df["Municipality"] == selected_municipality
]


# Count accommodation types
type_counts = filtered_df["AccommodationType"].value_counts()


# Show chart
st.subheader(
    f"Accommodation types in {selected_municipality}"
)


fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(
    type_counts.index,
    type_counts.values
)


ax.set_xlabel("Accommodation Type")
ax.set_ylabel("Number of Accommodations")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

st.pyplot(fig)


# Show total number of accommodations
st.write(
    f"Number of accommodations: {len(filtered_df)}"
)

st.info(
    "Limitation: the API does not provide accommodation prices, "
    "so the app cannot compare costs between municipalities."
)