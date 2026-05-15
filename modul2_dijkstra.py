# — Dijkstra (implementasikan dari sini) —
def dijkstra(graph: Graph, source: str) -> Tuple[Dict[str, int],
Dict[str, Optional[str]]]:
    """
    Mengembalikan (dist, parent).
    dist[v] = jarak minimum dari source ke v.
    parent[v] = predecessor v pada shortest path tree.
    Big-O: O(V^2 + E) dengan array sederhana (tanpa heap library).
    """
    INF = float('inf')
    dist = {v: INF for v in graph.adj}
    parent = {v: None for v in graph.adj}
    visited = set()
    dist[source] = 0

    # TODO: implementasikan loop Dijkstra
    while len(visited) < len(graph.adj):

        current = None
        current_dist = INF

        for node in graph.adj:
           
            if node not in visited and dist[node] < current_dist:

                current = node
                current_dist = dist[node]

        if current is None:
            break

        visited.add(current)

        for neighbor, weight in graph.neighbors(current):

            if neighbor not in visited:

                new_dist = dist[current] + weight

                if new_dist < dist[neighbor]:

                    dist[neighbor] = new_dist
                    parent[neighbor] = current
    return dist, parent


def reconstruct_path(parent: Dict[str, Optional[str]], source: str, target: str) -> List[str]:
    """Rekonstruksi jalur dari parent dict. Big-O: O(V)."""
    # TODO: implementasikan
    path = []

    current = target

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path
    pass
