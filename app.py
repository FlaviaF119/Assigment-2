import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


DATA_URL = "https://tourism.api.opendatahub.com/v1/Accommodation"


def get_municipality(x):
    if not isinstance(x, dict):
        return "Unknown"

    municipality_info = x.get("MunicipalityInfo", {})

    if not isinstance(municipality_info, dict):
        return "Unknown"

    name = municipality_info.get("Name", {})

    if not isinstance(name, dict):
        return "Unknown"

    return name.get("it", "Unknown")


all_items = []

for page in range(1, 18):

    response = requests.get(
        DATA_URL,
        params={
            "pagesize": 1000,
            "pagenumber": page
        }
    )

    print("Page:", page)
    print("Status:", response.status_code)

    data = response.json()

    all_items.extend(data["Items"])


df = pd.DataFrame(all_items)

print("Dataset shape:", df.shape)

print(
    "Missing LocationInfo:",
    df["LocationInfo"].isna().sum()
)


df["Municipality"] = df["LocationInfo"].apply(
    get_municipality
)


print(
    "Missing Municipality:",
    df["Municipality"].isna().sum()
)


municipality_counts = df["Municipality"].value_counts()

print("Top 10 municipalities:")
print(municipality_counts.head(10))

print(
    "Number of different municipalities:",
    df["Municipality"].nunique()
)


top15 = municipality_counts.head(15)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top15.index,
    y=top15.values
)

plt.xlabel("Municipality")
plt.ylabel("Number of accommodations")
plt.title("Top 15 Municipalities by Number of Accommodations")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


st.title("Accommodation Dashboard")

st.write(
    "Explore accommodations by municipality."
)


selected_municipality = st.selectbox(
    "Choose a municipality",
    municipality_counts.index
)


filtered_df = df[
    df["Municipality"] == selected_municipality
]


type_counts = filtered_df["AccoType"].value_counts()


st.subheader(
    f"Accommodation types in {selected_municipality}"
)


st.bar_chart(type_counts)


st.write(
    f"Number of accommodations: {len(filtered_df)}"
)