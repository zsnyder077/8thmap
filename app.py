import streamlit as st
import folium
from geopy.geocoders import ArcGIS
import pandas as pd
from streamlit_folium import st_folium

# Load data
#file_path = 'Desktop/Voting_Destinations/votingLocs.csv'
df = pd.read_csv("votingLocs.csv")

# Initialize map
m = folium.Map(location=[38.82667174903602, -77.12094362224809], zoom_start=11.2)

last_red_marker = None

# Function to add address marker
def add_address_marker(address, map_obj):
    global last_red_marker
    geolocator = ArcGIS()

    try:
        location = geolocator.geocode(address, timeout=10)

        if location:
            latitude = location.latitude
            longitude = location.longitude

            # Popup message for the marker
            popup = folium.Popup(f"<div style='width: 75px;'><strong>{'Your Location'}</strong></div>", max_width=250)

            if last_red_marker:
                map_obj.remove_child(last_red_marker)

            # Add red marker for input location
            last_red_marker = folium.Marker(
                location=[latitude, longitude],
                icon=folium.Icon(icon='star', color='red'),
                popup=popup
            )
            map_obj.add_child(last_red_marker)

        else:
            st.error(f"Address not found: {address}")
    except Exception as e:
        st.error(f"Geocoding error: {e}")

# Add circle markers from data
for index, row in df.iterrows():
    latitude = row[3]  # Use the column name for latitude
    longitude = row[4]  # Use the column name for longitude
    column1_value = row[0]  # Assuming there's a column named 'Name'
    column2_value = row[1]  # Assuming there's a column named 'Description'

    popup_content = f'''
    <div style="width: 200px;">
    <strong>{column1_value}</strong><br>
    {column2_value}
    </div>
    '''

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=4,
        color='dodgerblue',
        fill=True,
        fill_color='lightblue',
        fill_opacity=0.4,
        popup=popup_content
    ).add_to(m)

# Streamlit app UI
st.title("Interactive Map with Address Input")

# Sidebar input for address
address = st.sidebar.text_input("Enter an address", "Your Address")

# Update the map with the address marker
if address:
    add_address_marker(address, m)

# Display the map using streamlit_folium
st_folium(m, width=725, height=500)

