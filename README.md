# 🗺️ Pathfinding Algorithm Visualizer (ICADMA-2025)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

This is a live, interactive web application built in Streamlit for a poster presentation at the **ICADMA-2025** (International Conference on Analysis, Discrete Mathematics, and Applications).

The app provides a real-time, data-driven comparison of two fundamental pathfinding algorithms:
1.  **Dijkstra's Algorithm** (an "uninformed" search)
2.  **A\* Search** (an "informed," heuristic-based search)

**Author:** [Sanika Tribhuvan](https://github.com/SanikaTribhuvan)

---

## 🚀 Live Demo

**The app is deployed and live on Streamlit Cloud!**

**[Click Here to Open the Live Application](https://pathfinding-algorithm-visualizer-m6rkahkr3n22nlz2gj4e6m.streamlit.app/)**

### 📸 Application Preview

*(Replace this with a screenshot of your beautiful app!)*
![App Screenshot Placeholder](https://user-images.githubusercontent.com/1011333/150314220-d6215166-f03e-4370-8746-e52a65a3818e.png)

## 💡 The "Google Maps" Secret: Core Concept

This application provides a visual and quantitative answer to the question: "How does Google Maps find the fastest route so quickly?"

It runs both algorithms on a real-world road network of Ahmednagar, India (**17,678 nodes & 47,039 roads**) downloaded from OpenStreetMap.

* **Dijkstra's Algorithm:** The "blind" algorithm. It guarantees the shortest path but wastes massive computation by exploring in all directions.
* **A\* Search:** The "smart" algorithm. It uses a **heuristic** (the Haversine "as-the-crow-flies" distance) to guide its search, finding the *exact same* optimal path while exploring **90-98% fewer nodes**.

## ✨ Key Features

* **Live Algorithm Comparison:** See a real-time performance breakdown of Dijkstra vs. A\* on any two points.
* **Data-Driven Results:** Calculates and compares **Nodes Explored** and **Computation Time (ms)**.
* **Location Search:** Uses `geopy` (Nominatim) to find and set points by name (e.g., "Ahmednagar Railway Station").
* **Dynamic Plotly Charts:** Instantly generates bar charts to visualize the performance difference.
* **GPX & JSON Export:** Download your calculated route as a standard `.gpx` file or get the raw performance stats as a `.json` file.
* **Interactive Folium Map:** A custom-styled dark-mode map for selecting start and end points.

## 🛠️ Tech Stack

* **Framework:** Streamlit
* **Graph Data:** OSMnx, NetworkX
* **Mapping:** Folium, `streamlit-folium`
* **Data Visualization:** Plotly
* **Utilities:** `geopy`, `gpxpy`, `qrcode`

## 🏁 How to Run Locally

This project is self-contained. The `ahmednagar.graphml` data file (18.1MB) is included in this repository.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/SanikaTribhuvan/Pathfinding-Algorithm-Visualizer.git](https://github.com/SanikaTribhuvan/Pathfinding-Algorithm-Visualizer.git)
    cd Pathfinding-Algorithm-Visualizer
    ```

2.  **Install Dependencies:**
    * This project is configured to run on **Python 3.11** (see `runtime.txt`).
    * Install all required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

The app will open in your browser at `http://localhost:8501`.
