import streamlit as st
import folium
from geopy.geocoders import ArcGIS
import pandas as pd
from streamlit_folium import st_folium

# Sample dataset for markers
df = pd.DataFrame({
    'Name': ['Location1', 'Location2'],
    'Description': ['Description1', 'Description2'],
    'Latitude': [38.826671, 38.927000],
    'Longitude': [-77.120943, -77.020943]
})

# Streamlit app title
st.title("Interactive Map with Address Input")

# Function to add a marker for an address entered by the user
def add_address_marker(address, map_obj):
    geolocator = ArcGIS()
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            popup = folium.Popup(f"<div style='width: 75px;'><strong>{'Your Location'}</strong></div>", max_width=250)
            folium.Marker(
                location=[latitude, longitude],
                icon=folium.Icon(icon='star'),
                popup=popup
            ).add_to(map_obj)
        else:
            st.error(f"Address not found: {address}")
    except Exception as e:
        st.error(f"Geocoding error: {e}")

# Creating a base map
m = folium.Map(location=[38.826671, -77.120943], zoom_start=11.2)

# Add the markers for each row in the dataframe
for index, row in df.iterrows():
    latitude = row['Latitude']
    longitude = row['Longitude']
    column1_value = row['Name']
    column2_value = row['Description']
    
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

# Form to input address
st.sidebar.header("Enter Address")
address = st.sidebar.text_input("Address")

if address:
    add_address_marker(address, m)

# Display the map
st_folium(m, width=700, height=500)
