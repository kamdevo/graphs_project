"""
Prueba de planaridad implementada desde cero (sin librerias externas de grafos).

Se basa en el algoritmo clasico de "adicion de caminos" de
Demoucron-Malgrange-Pretelaat (DMP):

1. Se descompone el grafo en sus componentes biconexas (algoritmo de
   Hopcroft-Tarjan via low-link), porque el algoritmo de insercion de
   caminos solo esta definido para grafos biconexos. Un grafo es plano
   si y solo si cada una de sus componentes biconexas es plana.

2. Para cada componente biconexa se parte de un ciclo cualquiera como
   "mapa" inicial (2 caras). Luego, repetidamente:
     - se calculan los "fragmentos" (segmentos) que aun faltan por
       insertar: cuerdas directas entre vertices ya dibujados, o
       componentes conexas de vertices todavia no dibujados.
     - un fragmento es "admisible" en una cara si todos sus puntos de
       contacto con el grafo ya dibujado caen sobre el borde de esa cara.
     - si algun fragmento no tiene ninguna cara admisible, el grafo NO
       es plano.
     - se inserta primero el fragmento mas restringido (el que solo
       tiene una cara admisible); si no hay ninguno forzado, se elige
       cualquiera. Insertar un camino de ese fragmento divide la cara
       elegida en dos caras nuevas.
   Si se logran insertar todas las aristas, la componente es plana.
"""


def _biconnected_components(adj):
    """Devuelve las componentes biconexas como listas de aristas (u, v)."""
    disc = {}
    low = {}
    parent = {}
    edge_stack = []
    components = []
    counter = [0]

    import sys
    sys.setrecursionlimit(10000)

    def dfs(u):
        disc[u] = low[u] = counter[0]
        counter[0] += 1
        for v in adj[u]:
            if v not in disc:
                parent[v] = u
                edge_stack.append((u, v))
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    comp = []
                    while edge_stack and edge_stack[-1] != (u, v):
                        comp.append(edge_stack.pop())
                    if edge_stack:
                        comp.append(edge_stack.pop())
                    components.append(comp)
            elif v != parent.get(u) and disc[v] < disc[u]:
                edge_stack.append((u, v))
                low[u] = min(low[u], disc[v])

    for u in adj:
        if u not in disc:
            dfs(u)
            if edge_stack:
                components.append(list(edge_stack))
                edge_stack.clear()

    return components


def _find_cycle(vertices, adj):
    """Encuentra un ciclo cualquiera dentro del grafo (para usar como mapa inicial)."""
    visited = set()
    parent = {}

    def dfs(u, par):
        visited.add(u)
        parent[u] = par
        for v in adj[u]:
            if v == par:
                continue
            if v in visited:
                cycle = [u]
                cur = u
                while cur != v:
                    if parent[cur] is None:
                        break
                    cur = parent[cur]
                    cycle.append(cur)
                if cur == v:
                    return cycle
                continue
            result = dfs(v, u)
            if result is not None:
                return result
        return None

    start = next(iter(vertices))
    return dfs(start, None)


def _compute_fragments(vertices, adj, embedded_vertices, embedded_edges):
    """Calcula los fragmentos (cuerdas y componentes) que faltan por dibujar."""
    fragments = []

    # Tipo 1: cuerdas directas entre dos vertices ya dibujados
    for u in embedded_vertices:
        for v in adj[u]:
            if v in embedded_vertices:
                e = (min(u, v), max(u, v))
                if e not in embedded_edges and u < v:
                    fragments.append({
                        'vertices': set(),
                        'edges': {e},
                        'contacts': {u, v},
                    })

    # Tipo 2: componentes conexas de vertices aun no dibujados
    outside = vertices - embedded_vertices
    visited = set()
    for start in outside:
        if start in visited:
            continue
        comp = set()
        stack = [start]
        visited.add(start)
        comp.add(start)
        while stack:
            node = stack.pop()
            for nb in adj[node]:
                if nb not in embedded_vertices and nb not in visited:
                    visited.add(nb)
                    comp.add(nb)
                    stack.append(nb)

        frag_edges = set()
        contacts = set()
        for node in comp:
            for nb in adj[node]:
                e = (min(node, nb), max(node, nb))
                frag_edges.add(e)
                if nb in embedded_vertices:
                    contacts.add(nb)

        fragments.append({
            'vertices': comp,
            'edges': frag_edges,
            'contacts': contacts,
        })

    return fragments


def _find_attachment_path(frag):
    """Encuentra un camino entre dos puntos de contacto del fragmento,
    pasando solo por vertices internos (no dibujados) del fragmento."""
    contacts = list(frag['contacts'])

    if not frag['vertices']:
        # Es una cuerda directa: el "camino" es solo la arista u-v
        return [contacts[0], contacts[1]]

    adj = {}
    for (a, b) in frag['edges']:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    contact_set = set(contacts)
    start = contacts[0]
    visited = {start}
    parent = {start: None}
    queue = [start]
    target = None

    while queue and target is None:
        node = queue.pop(0)
        for nb in adj.get(node, ()):
            if nb in visited:
                continue
            visited.add(nb)
            parent[nb] = node
            if nb in contact_set and nb != start:
                target = nb
                break
            queue.append(nb)

    path = [target]
    cur = target
    while parent[cur] is not None:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def _is_biconnected_planar(vertices, edge_list):
    vertices = set(vertices)
    n = len(vertices)

    if n <= 4:
        return True

    edge_set = set((min(u, v), max(u, v)) for u, v in edge_list)
    m = len(edge_set)

    # Condicion necesaria (formula de Euler para grafos planos simples):
    # E <= 3V - 6. Si se viola, ya sabemos que no es plano (poda rapida).
    if m > 3 * n - 6:
        return False

    adj = {v: set() for v in vertices}
    for u, v in edge_set:
        adj[u].add(v)
        adj[v].add(u)

    cycle = _find_cycle(vertices, adj)
    if cycle is None:
        return True  # no deberia pasar en una componente biconexa con n>=3

    embedded_vertices = set(cycle)
    embedded_edges = set()
    for i in range(len(cycle)):
        a, b = cycle[i], cycle[(i + 1) % len(cycle)]
        embedded_edges.add((min(a, b), max(a, b)))

    faces = [list(cycle), list(reversed(cycle))]
    remaining = edge_set - embedded_edges

    while remaining:
        fragments = _compute_fragments(vertices, adj, embedded_vertices, embedded_edges)
        fragments = [f for f in fragments if f['edges'] - embedded_edges]

        if not fragments:
            break

        options = []
        for frag in fragments:
            contacts = frag['contacts']
            adm = [i for i, f in enumerate(faces) if contacts.issubset(set(f))]
            if not adm:
                return False  # ningun contacto disponible -> no es plano
            options.append((frag, adm))

        # preferir el fragmento mas restringido (una sola cara admisible)
        chosen = None
        for frag, adm in options:
            if len(adm) == 1:
                chosen = (frag, adm[0])
                break
        if chosen is None:
            chosen = (options[0][0], options[0][1][0])

        frag, face_idx = chosen
        path = _find_attachment_path(frag)
        u, v = path[0], path[-1]
        face = faces[face_idx]

        iu = face.index(u)
        rotated = face[iu:] + face[:iu]
        iv = rotated.index(v)
        arc1 = rotated[:iv + 1]            # de u a v
        arc2 = rotated[iv:] + rotated[:1]  # de v a u

        middle = path[1:-1]
        new_face1 = arc1 + list(reversed(middle))
        new_face2 = arc2 + middle
        faces[face_idx:face_idx + 1] = [new_face1, new_face2]

        embedded_vertices.update(middle)
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            e = (min(a, b), max(a, b))
            embedded_edges.add(e)
            remaining.discard(e)

    return len(remaining) == 0


def is_planar_graph(vertices, edges):
    """
    vertices: iterable de nodos
    edges: iterable de tuplas (u, v) [sin pesos, sin loops repetidos]
    """
    vertices = set(vertices)
    edge_set = set((min(u, v), max(u, v)) for u, v in edges if u != v)

    n = len(vertices)
    if n <= 4:
        return True

    adj = {v: set() for v in vertices}
    for u, v in edge_set:
        adj[u].add(v)
        adj[v].add(u)

    components = _biconnected_components(adj)
    for comp_edges in components:
        comp_vertices = set()
        for u, v in comp_edges:
            comp_vertices.add(u)
            comp_vertices.add(v)
        if len(comp_vertices) <= 4:
            continue
        if not _is_biconnected_planar(comp_vertices, comp_edges):
            return False
    return True