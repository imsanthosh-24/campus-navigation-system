import heapq

LOCATIONS = [
    "Main Gate", "Admin Block", "CSE Department", "Library",
    "Canteen", "Hostel", "Auditorium", "Bus Stop"
]
GRAPH = [
    [0,200,0,0,0,0,0,150],
    [200,0,120,0,0,0,180,0],
    [0,120,0,100,150,0,0,0],
    [0,0,100,0,100,200,0,0],
    [0,0,150,100,0,100,120,0],
    [0,0,0,200,100,0,0,150],
    [0,180,0,0,120,0,0,100],
    [150,0,0,0,0,150,100,0]
]

def neighbors(u):
    return [v for v, w in enumerate(GRAPH[u]) if w > 0]

def reconstruct(prev, target):
    path = []
    cur = target
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))

def dijkstra(s, t):
    n = len(LOCATIONS); dist = [float("inf")]*n; prev = [-1]*n
    dist[s] = 0; pq = [(0,s)]
    while pq:
        d,u = heapq.heappop(pq)
        if d != dist[u]: continue
        for v in neighbors(u):
            nd = d + GRAPH[u][v]
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u; heapq.heappush(pq,(nd,v))
    return dist[t], reconstruct(prev,t) if dist[t] < float("inf") else []

def bfs(s,t):
    from collections import deque
    q=deque([s]); seen={s}; prev=[-1]*len(LOCATIONS)
    while q:
        u=q.popleft()
        if u==t: break
        for v in neighbors(u):
            if v not in seen:
                seen.add(v); prev[v]=u; q.append(v)
    path=reconstruct(prev,t) if t in seen else []
    return sum(GRAPH[a][b] for a,b in zip(path,path[1:])),path

def dfs(s,t):
    seen=set(); prev=[-1]*len(LOCATIONS); stack=[s]
    while stack:
        u=stack.pop()
        if u in seen: continue
        seen.add(u)
        if u==t: break
        for v in reversed(neighbors(u)):
            if v not in seen and prev[v] == -1 and v != s:
                prev[v]=u; stack.append(v)
    path=reconstruct(prev,t) if t in seen else []
    return sum(GRAPH[a][b] for a,b in zip(path,path[1:])),path

def prim_mst():
    n=len(LOCATIONS); used={0}; edges=[]; total=0
    while len(used)<n:
        candidates=[(GRAPH[u][v],u,v) for u in used for v in range(n) if v not in used and GRAPH[u][v]]
        if not candidates: break
        w,u,v=min(candidates); used.add(v); total+=w
        edges.append((u,v,w))
    return total,edges

def kruskal_mst():
    parent=list(range(len(LOCATIONS)))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    edges=sorted((GRAPH[i][j],i,j) for i in range(len(LOCATIONS)) for j in range(i+1,len(LOCATIONS)) if GRAPH[i][j])
    chosen=[]; total=0
    for w,u,v in edges:
        a,b=find(u),find(v)
        if a!=b:
            parent[a]=b; chosen.append((u,v,w)); total+=w
    return total,chosen

def floyd_warshall(s,t):
    n=len(LOCATIONS); d=[[float("inf")]*n for _ in range(n)]; nxt=[[None]*n for _ in range(n)]
    for i in range(n):
        d[i][i]=0
        for j in range(n):
            if GRAPH[i][j]: d[i][j]=GRAPH[i][j]; nxt[i][j]=j
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]+d[k][j]<d[i][j]:
                    d[i][j]=d[i][k]+d[k][j]; nxt[i][j]=nxt[i][k]
    if nxt[s][t] is None and s!=t: return float("inf"),[]
    path=[s]
    while s!=t:
        s=nxt[s][t]; path.append(s)
    return d[path[0]][t],path

def run_algorithm(name,s,t):
    name=name.lower()
    if name=="dijkstra": distance,path=dijkstra(s,t); label="Dijkstra"
    elif name=="bfs": distance,path=bfs(s,t); label="BFS"
    elif name=="dfs": distance,path=dfs(s,t); label="DFS"
    elif name=="floyd": distance,path=floyd_warshall(s,t); label="Floyd–Warshall"
    elif name in ("prim","kruskal"):
        total,edges=prim_mst() if name=="prim" else kruskal_mst()
        return {"algorithm":name.title(),"mode":"mst","total":total,
                "edges":[{"from":LOCATIONS[u],"to":LOCATIONS[v],"distance":w} for u,v,w in edges],
                "message":"Minimum spanning tree for the entire campus network."}
    else: raise ValueError("Unknown algorithm selected.")
    if not path: return {"algorithm":label,"error":"No route exists between these locations."}
    return {"algorithm":label,"mode":"route","distance":int(distance),
            "route":[LOCATIONS[i] for i in path],
            "message":" → ".join(LOCATIONS[i] for i in path)}
