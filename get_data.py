import osmnx as ox

# This query will get the *center point* of the city
city_center_query = "Ahmednagar, Maharashtra, India"
# 30km radius - covers entire city and surrounding highways
distance_in_meters = 30000  # 30 kilometers

print(f"Starting download for: {city_center_query} (30km radius)")
print("Downloading complete road network including flyovers, bridges, highways...")
print("This will take 2-5 minutes depending on your internet speed...")

try:
    # 1. Get the center point (latitude, longitude)
    center_point = ox.geocode(city_center_query)
    print(f"✓ Center point found: {center_point}")
    
    # 2. Download the graph with ALL road types
    print("\n⏳ Downloading road network data from OpenStreetMap...")
    G = ox.graph_from_point(
        center_point, 
        dist=distance_in_meters, 
        network_type="drive",  # All drivable roads
        simplify=True,  # Simplifies the graph for better performance
        retain_all=False,  # Removes isolated road segments
        truncate_by_edge=True  # Clean boundaries
    )
    
    print("✓ Download complete! Processing data...")
    
    # 3. Print detailed diagnostics
    print("\n" + "="*50)
    print("📊 GRAPH STATISTICS")
    print("="*50)
    print(f"Total nodes (intersections): {G.number_of_nodes():,}")
    print(f"Total edges (road segments): {G.number_of_edges():,}")
    
    # Check what types of roads we have
    road_types = {}
    bridge_count = 0
    tunnel_count = 0
    
    for u, v, data in G.edges(data=True):
        if 'highway' in data:
            highway = data['highway']
            if isinstance(highway, list):
                for h in highway:
                    road_types[h] = road_types.get(h, 0) + 1
            else:
                road_types[highway] = road_types.get(highway, 0) + 1
        
        # Count bridges/flyovers
        if data.get('bridge') in ['yes', True]:
            bridge_count += 1
        if data.get('tunnel') in ['yes', True]:
            tunnel_count += 1
    
    print(f"\n🛣️  ROAD TYPES INCLUDED:")
    for road_type, count in sorted(road_types.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {road_type}: {count:,} segments")
    
    print(f"\n🌉 SPECIAL STRUCTURES:")
    print(f"   • Bridges/Flyovers: {bridge_count:,}")
    print(f"   • Tunnels: {tunnel_count:,}")
    
    # 4. Show the coverage area
    lats = [n[1]['y'] for n in G.nodes(data=True)]
    lons = [n[1]['x'] for n in G.nodes(data=True)]
    
    print(f"\n📍 COVERAGE AREA:")
    print(f"   • Latitude:  {min(lats):.4f} to {max(lats):.4f}")
    print(f"   • Longitude: {min(lons):.4f} to {max(lons):.4f}")
    print(f"   • Approximate radius: ~{distance_in_meters/1000}km from center")
    
    # 5. Save the graph file
    print(f"\n💾 Saving to 'ahmednagar.graphml'...")
    ox.save_graphml(G, "ahmednagar.graphml")
    
    # Estimate file size
    import os
    file_size_mb = os.path.getsize("ahmednagar.graphml") / (1024 * 1024)
    
    print("\n" + "="*50)
    print("✅ SUCCESS!")
    print("="*50)
    print(f"✓ File saved: ahmednagar.graphml ({file_size_mb:.2f} MB)")
    print(f"✓ Ready to use in your Streamlit app!")
    print(f"\n💡 This file size is optimal for web deployment:")
    if file_size_mb < 10:
        print(f"   EXCELLENT - Can push directly to GitHub")
    elif file_size_mb < 25:
        print(f"   GOOD - Should work well, slightly slower initial load")
    else:
        print(f"   LARGE - Consider using GitHub Releases for hosting")
    
    print("\n🚀 Next steps:")
    print("   1. Replace your old ahmednagar.graphml file")
    print("   2. Restart your Streamlit app")
    print("   3. Test the flyover routing!")

except Exception as e:
    print(f"\n" + "="*50)
    print("❌ ERROR: Could not download map data")
    print("="*50)
    print(f"Error details: {e}")
    print("\n🔧 Possible solutions:")
    print("   1. Check your internet connection")
    print("   2. Wait a few minutes (OpenStreetMap might be rate-limiting)")
    print("   3. Try a smaller radius (e.g., 20000 meters)")
    print("   4. Verify the city name is correct")
    print("\n💡 If error persists, try running:")
    print("   pip install --upgrade osmnx")