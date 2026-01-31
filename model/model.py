import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.map_artists = {}
        self.load_all_artists()

        self.artists_id_with_min_albums = []
        self.archi_id = []
        self.best_percorso = []
        self.best_peso = 0

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")
        for artist in self._artists_list:
            self.map_artists[artist.id] = artist

    def load_artists_with_min_albums(self, min_albums):
        self.artists_id_with_min_albums = DAO.read_artists_with_min_albums(min_albums)

    def build_graph(self):
        self._graph.clear()
        #implemento nodi
        for artist_id in self.artists_id_with_min_albums:
            self._graph.add_node(artist_id)
        #implemento archi
        self.load_archi()
        if not self.archi_id:
            print('Nessun arco')
            return
        else:
            for id1,id2,peso in self.archi_id:
                self._graph.add_edge(id1,id2, peso = peso)

    def calcola_percorso(self, d_min, n_art, id_partenza):
        print(d_min, n_art, id_partenza)
        self.best_percorso = []
        self.best_peso = 0
        artisti = self.get_id_artisti(d_min)
        if not artisti:
            self.best_percorso = []
            self.best_peso = []

        else:
            lp = [id_partenza]
            vp = 0
            grafo = nx.subgraph(self._graph, artisti)
            self.ricorsione(grafo, lp, vp, n_art)
            print(self.best_percorso, self.best_peso)

        return self.best_percorso, self.best_peso

    def load_archi(self):
        self.archi_id = DAO.load_archi(self.artists_id_with_min_albums)
        print(self.artists_id_with_min_albums)
        print(self.archi_id)

    def get_id_artisti(self, d_min):
        artisti_grafo = list(self._graph.nodes())
        artisti_validi = DAO.read_artisti_d_min(artisti_grafo, d_min)
        if not artisti_validi:
            return
        else:
            return artisti_validi

    def ricorsione(self, grafo, lp, vp, n_art):

        if len(lp) == n_art:
            if vp>self.best_peso:
                self.best_peso = vp
                self.best_percorso = lp.copy()
                print(lp, vp)
        for i,j,data in grafo.edges(lp[-1],data=True):

            if j in lp:
                continue

            lp.append(j)
            self.ricorsione(grafo, lp, vp + data['peso'], n_art)
            lp.pop(-1)
