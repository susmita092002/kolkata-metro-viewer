import streamlit as st
import pydeck as pdk
from haversine import haversine

# Neon dark theme config
st.set_page_config(page_title="Kolkata Metro Viewer", layout="wide")
st.markdown(
    """
    <style>
    body { background-color: #0f0f0f; color: #39ff14; }
    .stApp { background-color: #0f0f0f; }
    .st-bf { color: #39ff14 !important; }
    .st-bj { background-color: #1a1a1a !important; color: #39ff14 !important; }
    .st-ce, .st-de { color: #39ff14 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚇 Kolkata Metro Route Viewer")
st.markdown("Get a neon-glow route across the metro lines of Kolkata ✨")

# Metro line definitions
metro_lines = {
    "Blue Line": {
        "color": [0, 112, 192],
        "stations": [
            "Kavi Subhash", "Shahid Khudiram", "Kavi Nazrul", "Gitanjali", "Masterda Surya Sen", "Netaji",
            "Mahanayak Uttam Kumar", "Rabindra Sarobar", "Kalighat", "Jatin Das Park", "Netaji Bhavan",
            "Rabindra Sadan", "Maidan", "Park Street", "Esplanade", "Chandni Chowk", "Central",
            "Mahatma Gandhi Road", "Girish Park", "Shobhabazar Sutanuti", "Shyambazar", "Belgachia",
            "Dumdum", "Noapara", "Baranagar", "Dakshineswar"
        ]
    },
    "Green Line": {
        "color": [0, 255, 0],
        "stations": [
            "Salt Lake Sector V", "Karunamoyee", "Central Park", "City Centre", "Bengal Chemical",
            "Salt Lake Stadium", "Phoolbagan", "Sealdah", "Esplanade", "Mahakaran", "Howrah", "Howrah Maidan"
        ]
    },
    "Purple Line": {
        "color": [255, 0, 255],
        "stations": [
            "Joka", "Thakurpukur", "Sakherbazar", "Behala Chowrasta", "Behala Bazar", "Taratala", "Majerhat"
        ]
    },
    "Orange Line": {
        "color": [255, 165, 0],
        "stations": [
            "Kavi Subhash", "Satyajit Ray", "Jyotirindra Nandi", "Kavi Sukanta", "Hemanta Mukhopadhyay"
        ]
    }
}

# Coordinates for all stations
station_coords = {
    "Kavi Subhash": (22.4524, 88.3773), "Shahid Khudiram": (22.4615, 88.3795),
    "Kavi Nazrul": (22.4725, 88.3842), "Gitanjali": (22.4850, 88.3857),
    "Masterda Surya Sen": (22.4908, 88.3835), "Netaji": (22.5010, 88.3728),
    "Mahanayak Uttam Kumar": (22.5039, 88.3490), "Rabindra Sarobar": (22.5030, 88.3375),
    "Kalighat": (22.5123, 88.3310), "Jatin Das Park": (22.5225, 88.3265),
    "Netaji Bhavan": (22.5285, 88.3240), "Rabindra Sadan": (22.5350, 88.3215),
    "Maidan": (22.5450, 88.3190), "Park Street": (22.5525, 88.3165), "Esplanade": (22.5625, 88.3140),
    "Chandni Chowk": (22.5675, 88.3120), "Central": (22.5725, 88.3100),
    "Mahatma Gandhi Road": (22.5780, 88.3080), "Girish Park": (22.5835, 88.3060),
    "Shobhabazar Sutanuti": (22.5900, 88.3040), "Shyambazar": (22.5955, 88.3020),
    "Belgachia": (22.6010, 88.3000), "Dumdum": (22.6125, 88.2960),
    "Noapara": (22.6250, 88.2920), "Baranagar": (22.6355, 88.2900), "Dakshineswar": (22.6500, 88.2880),
    "Salt Lake Sector V": (22.5795, 88.4310), "Karunamoyee": (22.5820, 88.4190),
    "Central Park": (22.5850, 88.4070), "City Centre": (22.5880, 88.3950),
    "Bengal Chemical": (22.5910, 88.3830), "Salt Lake Stadium": (22.5940, 88.3710),
    "Phoolbagan": (22.5970, 88.3590), "Sealdah": (22.6000, 88.3470),
    "Mahakaran": (22.6030, 88.3350), "Howrah": (22.6060, 88.3230), "Howrah Maidan": (22.6090, 88.3110),
    "Joka": (22.4450, 88.3050), "Thakurpukur": (22.4550, 88.3100),
    "Sakherbazar": (22.4650, 88.3150), "Behala Chowrasta": (22.4750, 88.3200),
    "Behala Bazar": (22.4850, 88.3250), "Taratala": (22.4950, 88.3300),
    "Majerhat": (22.5050, 88.3350),
    "Satyajit Ray": (22.4580, 88.3840), "Jyotirindra Nandi": (22.4630, 88.3860),
    "Kavi Sukanta": (22.4680, 88.3880), "Hemanta Mukhopadhyay": (22.4730, 88.3900)
}

all_stations = list(station_coords.keys())

# Dropdown input
source = st.selectbox("🚉 Select Source Station", all_stations)
destination = st.selectbox("🎯 Select Destination Station", all_stations)

# Route details
def get_route_and_time(src, dst):
    dist_km = haversine(station_coords[src], station_coords[dst])
    time_min = round(dist_km / 30 * 60)
    return dist_km, time_min

# All line paths
line_layers = []
for line, info in metro_lines.items():
    coords = [station_coords[stn][::-1] for stn in info["stations"] if stn in station_coords]
    if len(coords) > 1:
        line_layers.append({
            "coordinates": coords,
            "color": info["color"]
        })

# Highlight selected route
highlight = []
if source != destination:
    highlight = [{
        "coordinates": [station_coords[source][::-1], station_coords[destination][::-1]],
        "color": [0, 255, 0]
    }]

# Station labels
labels = [{"position": station_coords[stn][::-1], "name": stn} for stn in station_coords]

# Show the map
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=(station_coords[source][0] + station_coords[destination][0]) / 2,
        longitude=(station_coords[source][1] + station_coords[destination][1]) / 2,
        zoom=11,
        pitch=45,
        bearing=0,
    ),
    layers=[
        pdk.Layer("PathLayer", data=line_layers, get_path="coordinates", get_color="color",
                  width_scale=3, width_min_pixels=3),
        pdk.Layer("PathLayer", data=highlight, get_path="coordinates", get_color="color",
                  width_scale=6, width_min_pixels=6),
        pdk.Layer("ScatterplotLayer", data=labels, get_position="position", get_color=[255, 255, 0],
                  get_radius=80),
        pdk.Layer("TextLayer", data=labels, get_position="position", get_text="name",
                  get_size=14, get_color=[0, 255, 255], get_alignment_baseline="'bottom'")
    ],
    tooltip={"text": "{name}"}
))

# Info box
if source != destination:
    dist_km, time_min = get_route_and_time(source, destination)
    st.markdown(f"### ✅ Route: **{source} → {destination}**")
    st.info(f"📏 Distance: **{dist_km:.2f} km**")
    st.success(f"⏱️ Travel Time: **{time_min} minutes**")

    direct_lines = [ln for ln in metro_lines if source in metro_lines[ln]["stations"] and destination in metro_lines[ln]["stations"]]
    if not direct_lines:
        st.warning("🚧 No direct connection. You may need an interchange.")
        src_lines = [ln for ln in metro_lines if source in metro_lines[ln]["stations"]]
        dst_lines = [ln for ln in metro_lines if destination in metro_lines[ln]["stations"]]
        for s_line in src_lines:
            for d_line in dst_lines:
                common = set(metro_lines[s_line]["stations"]) & set(metro_lines[d_line]["stations"])
                if common:
                    st.info(f"🔁 Try changing at: **{', '.join(common)}**")
                    break
