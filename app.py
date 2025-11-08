import streamlit as st
import streamlit.components.v1 as components
import os
import osmnx as ox
import networkx as nx
from streamlit_folium import st_folium
import folium
from math import radians, cos, sin, asin, sqrt
from heapq import heappush, heappop
from itertools import count
import qrcode
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from geopy.geocoders import Nominatim
import gpxpy
import gpxpy.gpx
from datetime import datetime
import time
import json
import base64
import io
from urllib.parse import urlencode, parse_qs

# ---------- PROFESSIONAL CONFIG & STYLING ----------
st.set_page_config(
    page_title="Google Maps' Secret: Graph Theory Route Finder | ICADMA 2025",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- PROFESSIONAL CSS STYLING ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    .main {
        background: linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%);
        padding: 0.5rem 1rem !important;
    }
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }
    
    .hero-header {
        background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        color: white;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(66, 133, 244, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(66, 133, 244, 0.08) 1px, transparent 1px);
        background-size: 40px 40px;
        animation: gridMove 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(40px, 40px); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        flex: 1;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        background: linear-gradient(90deg, #4285F4, #34A853, #FBBC04, #EA4335);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        color: #D1D5DB;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(52, 168, 83, 0.2);
        color: #34A853;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 2px solid rgba(52, 168, 83, 0.4);
    }
    
    .header-stats {
        display: flex;
        gap: 1rem;
        position: relative;
        z-index: 1;
        margin-left: 1rem;
        margin-right: 1rem;
    }
    
    .header-stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        min-width: 140px;
    }
    
    .header-stat-value {
        color: #34A853;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    
    .header-stat-label {
        color: #D1D5DB;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .header-qr {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .header-qr img {
        display: block;
        width: 80px;
        height: 80px;
    }
    
    .how-to-use-section {
        background: linear-gradient(135deg, #DBEAFE, #BFDBFE);
        border-left: 5px solid #4285F4;
        border-radius: 12px;
        padding: 1rem 2rem;
        color: #1E3A8A;
        line-height: 1.6;
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
    }
    
    .how-to-use-section b {
        color: #1E40AF;
        font-weight: 700;
    }
    
    .panel {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid #E5E7EB;
        margin-bottom: 0.75rem;
    }
    
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 3px solid #4285F4;
        display: block;
    }
    
    .selection-box {
        background: #F9FAFB;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.5rem;
        border: 2px solid #E5E7EB;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s;
    }
    
    .selection-box:hover {
        border-color: #4285F4;
        background: #F0F9FF;
    }
    
    .selection-icon {
        font-size: 1.2rem;
    }
    
    .selection-text {
        flex: 1;
    }
    
    .selection-label {
        font-size: 0.7rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.15rem;
    }
    
    .selection-value {
        font-size: 0.8rem;
        color: #1F2937;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4285F4, #34A853) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(66, 133, 244, 0.5) !important;
    }
    
    .comparison-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }
    
    .badge-dijkstra {
        background: linear-gradient(135deg, #DBEAFE, #BFDBFE);
        color: #1E40AF;
        border: 2px solid #93C5FD;
    }
    
    .badge-astar {
        background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
        color: #065F46;
        border: 2px solid #6EE7B7;
    }
    
    .efficiency-badge {
        display: block;
        background: linear-gradient(135deg, #34A853, #10B981);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-weight: 800;
        box-shadow: 0 6px 20px rgba(52, 168, 83, 0.3);
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .tooltip-help {
        font-size: 0.75rem;
        color: #6B7280;
        font-style: italic;
        margin-top: 0.25rem;
        margin-bottom: 0.5rem;
    }
    
    .progress-container {
        background: #F3F4F6;
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .progress-text {
        font-size: 0.85rem;
        color: #1F2937;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%) !important;
        border-left: 5px solid #34A853 !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.8rem !important;
        color: #065F46 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%) !important;
        border-left: 5px solid #4285F4 !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.8rem !important;
        color: #1E40AF !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%) !important;
        border-left: 5px solid #EA4335 !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.8rem !important;
        color: #991B1B !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: #1F2937 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        color: #6B7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader {
        background: #F9FAFB !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        color: #1F2937 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    .stSpinner > div {
        border-top-color: #4285F4 !important;
    }
    
    .stCaption {
        color: #6B7280 !important;
        font-size: 0.8rem !important;
    }
    
    a {
        color: #4285F4 !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    
    a:hover {
        color: #2A5FD9 !important;
        text-decoration: underline !important;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #F7FAFC, #EDF2F7);
        padding: 0.75rem;
        border-radius: 10px;
        border: 2px solid #E5E7EB;
        text-align: center;
        transition: all 0.3s;
        margin-bottom: 0.5rem;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0.15rem;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .leaflet-control-zoom,
    .leaflet-control-layers,
    .leaflet-bar,
    .leaflet-control-attribution {
        display: none !important;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.5rem;
        }
        .hero-subtitle {
            font-size: 0.9rem;
        }
    }
    
    div[data-testid="column"] {
        padding: 0 0.5rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- APP URL & QR CODE ----------
APP_URL = "https://pathfinding-algorithm-visualizer-amnatkdbyzpfz2m6gwynsr.streamlit.app/"

@st.cache_data
def generate_qr_base64(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

qr_base64_str = generate_qr_base64(APP_URL)

# ---------- DATA LOADING FUNCTION ----------
@st.cache_data
def load_graph():
    """Load the local graph file directly"""
    file_path = "ahmednagar.graphml"
    
    if not os.path.exists(file_path):
        st.error(f"❌ Graph file not found: {file_path}")
        st.stop()
    
    try:
        G = ox.load_graphml(file_path)
        return G
    except Exception as e:
        st.error(f"❌ Error loading graph: {e}")
        st.stop()

# ---------- ALGORITHM & HELPER FUNCTIONS ----------
def haversine_distance_coords(lat1, lon1, lat2, lon2):
    """Calculate haversine distance between two coordinate pairs"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    r = 6371
    return c * r * 1000

def haversine_distance(u, v):
    """Calculate haversine distance between two nodes in the graph"""
    u_coords = (G.nodes[u]['y'], G.nodes[u]['x'])
    v_coords = (G.nodes[v]['y'], G.nodes[v]['x'])
    return haversine_distance_coords(u_coords[0], u_coords[1], v_coords[0], v_coords[1])

def astar_path_with_explored_nodes(G, source, target, heuristic=None, weight="length"):
    if source not in G or target not in G:
        raise nx.NodeNotFound(f"Source or target not in graph.")
    if heuristic is None:
        heuristic = lambda u, v: 0
    push, pop, c = heappush, heappop, count()
    queue = [(0, next(c), source, 0, None)]
    enqueued, explored = {}, {}
    explored_nodes_list = []
    while queue:
        _, __, curnode, dist, parent = pop(queue)
        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return (path, len(explored), explored_nodes_list)
        if curnode in explored:
            continue
        explored[curnode] = parent
        explored_nodes_list.append(curnode)
        for neighbor, w in G[curnode].items():
            if neighbor in explored:
                continue
            cost = w.get(weight, 1)
            if cost is None:
                continue
            ncost = dist + cost
            if neighbor in enqueued:
                if ncost < enqueued[neighbor]:
                    enqueued[neighbor] = ncost
                else:
                    continue
            else:
                enqueued[neighbor] = ncost
            f_score = ncost + heuristic(neighbor, target)
            push(queue, (f_score, next(c), neighbor, ncost, curnode))
    raise nx.NetworkXNoPath(f"No path from {source} to {target}.")

def dijkstra_path_with_explored_nodes(G, source, target, weight="length"):
    if source not in G or target not in G:
        raise nx.NodeNotFound(f"Source or target not in graph.")
    push, pop, c = heappush, heappop, count()
    queue = [(0, next(c), source, None)]
    explored = {}
    explored_nodes_list = []
    while queue:
        dist, __, curnode, parent = pop(queue)
        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return (path, len(explored), explored_nodes_list)
        if curnode in explored:
            continue
        explored[curnode] = parent
        explored_nodes_list.append(curnode)
        for neighbor, w in G[curnode].items():
            if neighbor in explored:
                continue
            cost = w.get(weight, 1)
            if cost is None:
                continue
            ncost = dist + cost
            push(queue, (ncost, next(c), neighbor, curnode))
    raise nx.NetworkXNoPath(f"No path from {source} to {target}.")

def create_gpx_file(path_nodes, G):
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    for node in path_nodes:
        gpx_segment.points.append(
            gpxpy.gpx.GPXTrackPoint(G.nodes[node]['y'], G.nodes[node]['x'])
        )
    return gpx.to_xml()

def search_location(query):
    try:
        geolocator = Nominatim(user_agent="icadma_route_finder")
        location = geolocator.geocode(query + ", Ahmednagar, Maharashtra, India", timeout=10)
        if location:
            return (location.latitude, location.longitude, location.address)
        return None
    except:
        return None

def rebuild_map():
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=14,
        tiles="cartodbdark_matter",
        control_scale=False,
        zoom_control=False,
        attribution_control=False
    )
    
    # Draw the main route
    route_latlngs = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in st.session_state.route_path]
    
    # Add connection lines from clicked points to nearest nodes
    start_node_coords = (G.nodes[st.session_state.route_path[0]]['y'], G.nodes[st.session_state.route_path[0]]['x'])
    end_node_coords = (G.nodes[st.session_state.route_path[-1]]['y'], G.nodes[st.session_state.route_path[-1]]['x'])
    
    # Draw dashed lines to show connection to actual start/end points
    folium.PolyLine(
        [st.session_state.start_point, start_node_coords], 
        color="#34A853", 
        weight=4, 
        opacity=0.6, 
        dash_array="10"
    ).add_to(m)
    
    folium.PolyLine(
        [end_node_coords, st.session_state.end_point], 
        color="#34A853", 
        weight=4, 
        opacity=0.6, 
        dash_array="10"
    ).add_to(m)
    
    # Draw main route
    folium.PolyLine(route_latlngs, color="#34A853", weight=6, opacity=0.9, popup="Optimal Route (A*)").add_to(m)
    
    if st.session_state.show_dijkstra_nodes and st.session_state.dijkstra_explored_list:
        for node in st.session_state.dijkstra_explored_list[::10]:
            folium.CircleMarker(
                location=(G.nodes[node]['y'], G.nodes[node]['x']),
                radius=2, color='#4285F4', fill=True, fillOpacity=0.3
            ).add_to(m)
    
    if st.session_state.show_astar_nodes and st.session_state.astar_explored_list:
        for node in st.session_state.astar_explored_list[::10]:
            folium.CircleMarker(
                location=(G.nodes[node]['y'], G.nodes[node]['x']),
                radius=2, color='#34A853', fill=True, fillOpacity=0.3
            ).add_to(m)
    
    # Mark the actual clicked points
    folium.Marker(st.session_state.start_point, popup="🟢 Start (Your Click)", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker(st.session_state.end_point, popup="🔴 End (Your Click)", icon=folium.Icon(color="red", icon="flag")).add_to(m)
    
    # Mark the nearest graph nodes (optional - for debugging)
    folium.CircleMarker(
        start_node_coords,
        radius=5,
        color='#34A853',
        fill=True,
        fillOpacity=0.8,
        popup="Nearest Start Node"
    ).add_to(m)
    
    folium.CircleMarker(
        end_node_coords,
        radius=5,
        color='#EA4335',
        fill=True,
        fillOpacity=0.8,
        popup="Nearest End Node"
    ).add_to(m)
    
    st.session_state.route_map = m

# ---------- LOAD DATA & INIT STATE ----------
G = load_graph()
center_lat = 19.0948
center_lon = 74.7480
total_nodes = G.number_of_nodes()
total_edges = G.number_of_edges()

for k in ["start_point", "end_point", "route_map", "prev_click", "route_history", 
          "show_dijkstra_nodes", "show_astar_nodes", "algorithm_view", 
          "nodes_explored_dijkstra", "nodes_explored_astar", "path_length",
          "dijkstra_explored_list", "astar_explored_list", "calculation_time_dijkstra", 
          "calculation_time_astar", "route_path", "animate_route", "animation_step",
          "start_node", "end_node"]:
    if k not in st.session_state:
        if k == "route_history":
            st.session_state[k] = []
        elif k in ["show_dijkstra_nodes", "show_astar_nodes", "animate_route"]:
            st.session_state[k] = False
        elif k == "algorithm_view":
            st.session_state[k] = "both"
        elif k == "animation_step":
            st.session_state[k] = 0
        else:
            st.session_state[k] = None

# ---------- HERO HEADER ----------
st.markdown(f"""
<div class="hero-header">
    <div class="hero-content">
        <div class="hero-title">GOOGLE MAPS' SECRET</div>
        <div class="hero-subtitle">How Graph Theory Finds Your Fastest Route</div>
        <div class="hero-badge">🏆 ICADMA-2025 | Live Algorithm Demonstration | Ahmednagar</div>
    </div>
    <div class="header-stats">
        <div class="header-stat-card">
            <div class="header-stat-value">{total_nodes:,}</div>
            <div class="header-stat-label">Nodes</div>
        </div>
        <div class="header-stat-card">
            <div class="header-stat-value">{total_edges:,}</div>
            <div class="header-stat-label">Roads</div>
        </div>
    </div>
    <div class="header-qr">
        <img src="data:image/png;base64,{qr_base64_str}" alt="QR Code">
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HOW TO USE SECTION ----------
st.markdown("""
<div class="how-to-use-section">
    <b>📝 How to Use:</b> 
    <b>Step 1:</b> Click map or search for <span style='color: #34A853;'>start point 🟢</span> → 
    <b>Step 2:</b> Click again or search for <span style='color: #EA4335;'>end point 🔴</span> → 
    <b>Step 3:</b> Press <b>Calculate Route</b> → 
    <b>Step 4:</b> Compare algorithm performance!
</div>
""", unsafe_allow_html=True)

# ---------- MAIN 2-COLUMN LAYOUT ----------
col_left, col_right = st.columns([1.5, 1], gap="small")

# ========== LEFT COLUMN: MAP ==========
with col_left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🗺️ Interactive Map</div>', unsafe_allow_html=True)
    st.caption("Click on the map to select start (🟢) and end (🔴) points")
    
    if st.session_state.route_map:
        st_folium(st.session_state.route_map, width=None, height=600, returned_objects=[])
    else:
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=14,
            tiles="cartodbdark_matter",
            control_scale=False,
            zoom_control=False,
            attribution_control=False
        )
        
        if st.session_state.start_point:
            folium.Marker(
                st.session_state.start_point,
                popup="🟢 Start",
                icon=folium.Icon(color="green", icon="play")
            ).add_to(m)
        
        if st.session_state.end_point:
            folium.Marker(
                st.session_state.end_point,
                popup="🔴 End",
                icon=folium.Icon(color="red", icon="flag")
            ).add_to(m)
        
        m.add_child(folium.LatLngPopup())
        map_data = st_folium(m, width=None, height=600, key="base_map")
        
        if map_data and map_data.get('last_clicked'):
            click_coords = (map_data['last_clicked']['lat'], map_data['last_clicked']['lng'])
            if st.session_state.prev_click != click_coords:
                st.session_state.prev_click = click_coords
                if st.session_state.start_point and st.session_state.end_point:
                    st.session_state.start_point = click_coords
                    st.session_state.end_point = None
                elif st.session_state.start_point:
                    st.session_state.end_point = click_coords
                else:
                    st.session_state.start_point = click_coords
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== RIGHT COLUMN: CONTROLS ==========
with col_right:
    # --- Search Panel ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🔍 Location Search</div>', unsafe_allow_html=True)
    search_query = st.text_input("🏙️ Search for a location", placeholder="e.g., Railway Station, College", key="search_input")
    
    if st.button("🔍 Search Location"):
        if search_query:
            with st.spinner("Searching..."):
                result = search_location(search_query)
                if result:
                    lat, lon, address = result
                    if not st.session_state.start_point:
                        st.session_state.start_point = (lat, lon)
                        st.success(f"✅ Start point set to: {address[:50]}...")
                        st.rerun()
                    elif not st.session_state.end_point:
                        st.session_state.end_point = (lat, lon)
                        st.success(f"✅ End point set to: {address[:50]}...")
                        st.rerun()
                    else:
                        st.info("Both points already set. Clear to search again.")
                else:
                    st.error("Location not found. Try a different search.")
        else:
            st.warning("Please enter a location to search.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Selection & Action Panel ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📍 Current Selection</div>', unsafe_allow_html=True)
    
    if st.session_state.start_point:
        st.markdown(f"""
        <div class="selection-box">
            <div class="selection-icon">🟢</div>
            <div class="selection-text">
                <div class="selection-label">Start Point</div>
                <div class="selection-value">{st.session_state.start_point[0]:.4f}, {st.session_state.start_point[1]:.4f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click on map or search to set start point")
    
    if st.session_state.end_point:
        st.markdown(f"""
        <div class="selection-box">
            <div class="selection-icon">🔴</div>
            <div class="selection-text">
                <div class="selection-label">End Point</div>
                <div class="selection-value">{st.session_state.end_point[0]:.4f}, {st.session_state.end_point[1]:.4f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click on map or search to set end point")
    
    if st.session_state.start_point and st.session_state.end_point and not st.session_state.route_map:
        if st.button("🚀 Calculate Route", key="calculate_btn", type="primary"):
            progress_placeholder = st.empty()
            try:
                start_node = ox.nearest_nodes(G, st.session_state.start_point[1], st.session_state.start_point[0])
                end_node = ox.nearest_nodes(G, st.session_state.end_point[1], st.session_state.end_point[0])
                
                progress_placeholder.markdown('<div class="progress-container"><div class="progress-text">🔵 Running Dijkstra\'s Algorithm...</div></div>', unsafe_allow_html=True)
                start_time_dijkstra = time.time()
                dijkstra_path, dijkstra_explored_count, dijkstra_explored_list = dijkstra_path_with_explored_nodes(G, start_node, end_node, weight='length')
                end_time_dijkstra = time.time()
                st.session_state.calculation_time_dijkstra = end_time_dijkstra - start_time_dijkstra
                st.session_state.nodes_explored_dijkstra = dijkstra_explored_count
                st.session_state.dijkstra_explored_list = dijkstra_explored_list
                
                progress_placeholder.markdown('<div class="progress-container"><div class="progress-text">🟢 Running A* Algorithm...</div></div>', unsafe_allow_html=True)
                start_time_astar = time.time()
                astar_path, astar_explored_count, astar_explored_list = astar_path_with_explored_nodes(G, start_node, end_node, heuristic=haversine_distance, weight='length')
                end_time_astar = time.time()
                st.session_state.calculation_time_astar = end_time_astar - start_time_astar
                st.session_state.nodes_explored_astar = astar_explored_count
                st.session_state.astar_explored_list = astar_explored_list
                
                st.session_state.route_path = astar_path
                
                # Calculate path length correctly including connections to start/end points
                path_length = 0
                
                # Add distance from clicked start point to nearest node
                start_node_coords = (G.nodes[start_node]['y'], G.nodes[start_node]['x'])
                start_connection_dist = haversine_distance_coords(
                    st.session_state.start_point[0], st.session_state.start_point[1],
                    start_node_coords[0], start_node_coords[1]
                )
                path_length += start_connection_dist
                
                # Add main route distance
                for i in range(len(astar_path)-1):
                    edge_data = G[astar_path[i]][astar_path[i+1]]
                    if isinstance(edge_data, dict):
                        # MultiGraph - get first edge
                        path_length += list(edge_data.values())[0].get('length', 0)
                    else:
                        # Simple graph
                        path_length += edge_data.get('length', 0)
                
                # Add distance from nearest node to clicked end point
                end_node_coords = (G.nodes[end_node]['y'], G.nodes[end_node]['x'])
                end_connection_dist = haversine_distance_coords(
                    end_node_coords[0], end_node_coords[1],
                    st.session_state.end_point[0], st.session_state.end_point[1]
                )
                path_length += end_connection_dist
                
                st.session_state.path_length = f"{path_length/1000:.2f} km"
                st.session_state.start_node = start_node
                st.session_state.end_node = end_node
                
                progress_placeholder.markdown('<div class="progress-container"><div class="progress-text">🗺️ Rendering map...</div></div>', unsafe_allow_html=True)
                rebuild_map()
                
                progress_placeholder.empty()
                st.rerun()
            except Exception as e:
                progress_placeholder.empty()
                st.error(f"⚠️ Error calculating route: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Theory Panel ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    with st.expander("📚 Algorithm Theory", expanded=False):
        st.markdown("""
        **Dijkstra's Algorithm:** Explores all directions equally, guaranteed shortest path.
        - Time Complexity: O((V + E) log V)
        - Explores many nodes
        
        **A* Algorithm:** Uses heuristic (straight-line distance) to guide search toward goal.
        - Time Complexity: O(E)
        - Explores fewer nodes
        - More efficient for point-to-point routing
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FULL WIDTH RESULTS PANEL ==========
if st.session_state.route_map:
    # --- Visualization Controls Panel ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    viz_col, button_col = st.columns([2, 1])
    with viz_col:
        st.markdown('<div class="section-header">🎛️ Visualization Controls</div>', unsafe_allow_html=True)
        st.markdown('<div class="tooltip-help">💡 Toggle explored nodes visualization (slows map)</div>', unsafe_allow_html=True)
        
        col_toggle1, col_toggle2 = st.columns(2)
        with col_toggle1:
            show_dijkstra_new = st.checkbox("🔵 Dijkstra Nodes", value=st.session_state.show_dijkstra_nodes)
        with col_toggle2:
            show_astar_new = st.checkbox("🟢 A* Nodes", value=st.session_state.show_astar_nodes)
        
        if show_dijkstra_new != st.session_state.show_dijkstra_nodes or show_astar_new != st.session_state.show_astar_nodes:
            st.session_state.show_dijkstra_nodes = show_dijkstra_new
            st.session_state.show_astar_nodes = show_astar_new
            rebuild_map()
            st.rerun()
    
    with button_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Clear & Search Again", key="clear_btn"):
            for k in ["start_point", "end_point", "route_map", "prev_click", 
                      "nodes_explored_dijkstra", "nodes_explored_astar", "path_length",
                      "dijkstra_explored_list", "astar_explored_list", "route_path"]:
                st.session_state[k] = None
            st.session_state.show_dijkstra_nodes = False
            st.session_state.show_astar_nodes = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Performance Comparison Panel ---
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Algorithm Performance Comparison</div>', unsafe_allow_html=True)
    
    col_result1, col_result2, col_result3 = st.columns(3)
    
    with col_result1:
        st.metric(
            label="📏 Route Distance",
            value=st.session_state.path_length if st.session_state.path_length else "N/A"
        )
    
    with col_result2:
        efficiency = 100 * (1 - st.session_state.nodes_explored_astar / st.session_state.nodes_explored_dijkstra) if st.session_state.nodes_explored_dijkstra > 0 else 0
        st.metric(
            label="⚡ A* Efficiency",
            value=f"{efficiency:.1f}%",
            delta="More Efficient" if efficiency > 0 else "Same"
        )
    
    with col_result3:
        time_saved = st.session_state.calculation_time_dijkstra - st.session_state.calculation_time_astar
        st.metric(
            label="⏱️ Time Saved",
            value=f"{time_saved*1000:.1f}ms",
            delta=f"{(time_saved/st.session_state.calculation_time_dijkstra*100):.0f}% faster" if (time_saved > 0 and st.session_state.calculation_time_dijkstra > 0) else "Similar"
        )
    
    col_algo1, col_algo2 = st.columns(2)
    
    with col_algo1:
        st.markdown('<div class="comparison-badge badge-dijkstra">🔵 Dijkstra\'s Algorithm</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.nodes_explored_dijkstra:,}</div>
            <div class="stat-label">Nodes Explored</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.calculation_time_dijkstra*1000:.1f}ms</div>
            <div class="stat-label">Computation Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_algo2:
        st.markdown('<div class="comparison-badge badge-astar">🟢 A* Algorithm</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.nodes_explored_astar:,}</div>
            <div class="stat-label">Nodes Explored</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.calculation_time_astar*1000:.1f}ms</div>
            <div class="stat-label">Computation Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="efficiency-badge">A* explored {efficiency:.1f}% fewer nodes! 🎯</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📈 Interactive Performance Charts</div>', unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_nodes = go.Figure(data=[
            go.Bar(name='Dijkstra', x=['Nodes Explored'], y=[st.session_state.nodes_explored_dijkstra], marker_color='#4285F4'),
            go.Bar(name='A*', x=['Nodes Explored'], y=[st.session_state.nodes_explored_astar], marker_color='#34A853')
        ])
        fig_nodes.update_layout(
            title="Nodes Explored Comparison",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_nodes, use_container_width=True)
    
    with chart_col2:
        fig_time = go.Figure(data=[
            go.Bar(name='Dijkstra', x=['Computation Time'], y=[st.session_state.calculation_time_dijkstra*1000], marker_color='#4285F4'),
            go.Bar(name='A*', x=['Computation Time'], y=[st.session_state.calculation_time_astar*1000], marker_color='#34A853')
        ])
        fig_time.update_layout(
            title="Computation Time Comparison (ms)",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown('<div class="section-header">💾 Export & Share</div>', unsafe_allow_html=True)
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        if st.session_state.route_path:
            gpx_data = create_gpx_file(st.session_state.route_path, G)
            st.download_button(
                label="📥 Download GPX",
                data=gpx_data,
                file_name=f"route_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gpx",
                mime="application/gpx+xml"
            )
    
    with export_col2:
        share_url = f"{APP_URL}"
        st.markdown(f'<a href="{share_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #4285F4, #34A853); color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 600;">🔗 Share Route</a>', unsafe_allow_html=True)
    
    with export_col3:
        stats_json = {
            "distance": st.session_state.path_length,
            "dijkstra_nodes": st.session_state.nodes_explored_dijkstra,
            "astar_nodes": st.session_state.nodes_explored_astar,
            "efficiency": f"{efficiency:.1f}%",
            "time_dijkstra": f"{st.session_state.calculation_time_dijkstra*1000:.1f}ms",
            "time_astar": f"{st.session_state.calculation_time_astar*1000:.1f}ms"
        }
        st.download_button(
            label="📊 Download Stats",
            data=json.dumps(stats_json, indent=2),
            file_name=f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #6B7280; font-size: 0.85rem;">
    Built with ❤️ for ICADMA-2025 | Powered by Graph Theory & Python<br>
    <b>Created by Sanika Tribhuvan</b><br>
    📧 <a href="mailto:tribhuvansanika@gmail.com" style="color:#34A853;font-weight:600;">Contact: tribhuvansanika@gmail.com</a><br>
    🔗 <a href="https://github.com/SanikaTribhuvan/Pathfinding-Algorithm-Visualizer" target="_blank" style="color:#4285F4;font-weight:600;">View on GitHub</a>
</div>
""", unsafe_allow_html=True)