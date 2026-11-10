# Campus Navigation System — ADSA Mini Project

## Features
- Browser-based campus navigation application (Flask).
- Eight sample campus locations and weighted undirected graph.
- Dijkstra, BFS, DFS, Floyd–Warshall route calculations.
- Prim and Kruskal minimum spanning tree calculations.
- Campus connection list and responsive interface.
- Standalone C console companion implementing the six algorithm options.

## Requirements
- Windows 10/11
- Python 3.11 or later
- GCC (optional, for the C console program)

## Run the web application (Windows PowerShell)
Open PowerShell in this folder and run:

```powershell
py -m pip install -r requirements.txt
py app.py
```

If `py` and `python` are not on PATH but Python 3.11 is installed at the path used in your setup, run:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" app.py
```

Open http://127.0.0.1:5000 and keep the terminal open while presenting.

## Compile and run the C program (optional)
Install GCC, then:

```powershell
gcc -std=c11 -Wall -Wextra campus_navigation.c -o campus_navigation.exe
.\campus_navigation.exe
```

## Demo
1. Open the web app.
2. Choose Main Gate as source and Library as destination.
3. Select Dijkstra and click Calculate Route.
4. Expected result: Main Gate → Admin Block → CSE Department → Library, 420 m.
5. Try BFS, DFS and Floyd–Warshall.
6. Select Prim or Kruskal to display the campus minimum spanning tree.
7. In the C console program, choose an algorithm and enter location indices shown on screen.

## Customize the graph
Edit `LOCATIONS` and `GRAPH` in `algorithms.py`. The graph is undirected, so each edge distance must be entered in both symmetric matrix positions. Use 0 where no direct edge exists.

## Important project note
The browser application uses Python implementations of the graph algorithms through Flask. The C file is a companion console implementation for demonstrating the algorithms in C; it is not invoked by the Flask web app. This keeps the web demo simple and reliable while allowing the C implementations to be assessed separately.
