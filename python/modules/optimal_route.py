from geopy.distance import geodesic
import pandas as pd
import streamlit as st


def compute_optimal_route(location_probs, top_n=10):
    sorted_locations = location_probs.sort_values("avg_probability", ascending=False).head(top_n).reset_index(drop=True)

    route = [sorted_locations.loc[0]]
    visited = {0}
    current_index = 0

    while len(visited) < len(sorted_locations):
        current_city = sorted_locations.loc[current_index]
        min_dist = float("inf")
        next_index = None

        for i in range(len(sorted_locations)):
            if i not in visited:
                dist = geodesic(
                    (current_city["latitude"], current_city["longitude"]),
                    (sorted_locations.loc[i]["latitude"], sorted_locations.loc[i]["longitude"])
                ).km
                if dist < min_dist:
                    min_dist = dist
                    next_index = i

        visited.add(next_index)
        route.append(sorted_locations.loc[next_index])
        current_index = next_index

    route_df = pd.DataFrame(route).reset_index(drop=True)
    route_df["step"] = route_df.index + 1
    route_df["probabilitate_%"] = (route_df["avg_probability"] * 100).round(2)
    return route_df

def show_route_map(route_df):
    import pydeck as pdk
    import pandas as pd

    path = route_df[['longitude', 'latitude']].values.tolist()

    arc_data = pd.DataFrame({
        "from_lon": [path[i][0] for i in range(len(path) - 1)],
        "from_lat": [path[i][1] for i in range(len(path) - 1)],
        "to_lon": [path[i+1][0] for i in range(len(path) - 1)],
        "to_lat": [path[i+1][1] for i in range(len(path) - 1)],
    })

    arc_layer = pdk.Layer(
        "ArcLayer",
        data=arc_data,
        get_source_position=["from_lon", "from_lat"],
        get_target_position=["to_lon", "to_lat"],
        get_width=4,
        get_source_color=[255, 255, 255],
        get_target_color=[255, 0, 0],
        auto_highlight=True,
        pickable=False,
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=route_df,
        get_position='[longitude, latitude]',
        get_radius=30000,
        get_fill_color='[255, 0, 0]',
        pickable=True,
        get_tooltip=True
    )

    view_state = pdk.ViewState(
        latitude=route_df["latitude"].mean(),
        longitude=route_df["longitude"].mean(),
        zoom=4,
        pitch=30,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[arc_layer, scatter_layer],
        initial_view_state=view_state,
        tooltip={"text": "Etapa {step}: {city}, {state}\nProbabilitate: {probabilitate_%}"}
    ))