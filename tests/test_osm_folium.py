import folium

map_osm = folium.Map(location=[32.7592, -117.2516], zoom_start=12)
map_osm.save('osm.html')

map_1 = folium.Map(location=[45.372, -121.6972], zoom_start=12,tiles='Stamen Terrain')
folium.Marker([45.3288, -121.6625], popup='Mt. Hood Meadows',
                   icon = folium.Icon(icon = 'cloud')).add_to(map_1)
folium.Marker([45.3311, -121.7113], popup='Timberline Lodge',
                   icon = folium.Icon(color ='green')).add_to(map_1)
folium.Marker([45.3300, -121.6823], popup='Some Other Location',
                   icon = folium.Icon(color ='red')).add_to(map_1)
map_1.save('iconTest.html')