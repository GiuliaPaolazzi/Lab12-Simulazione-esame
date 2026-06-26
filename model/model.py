import copy
from datetime import datetime, date

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapActors = {}
        self._bestPath = None
        self._lun = 0

    def getAllRatings(self):
        voti= list(DAO.getAllRatings())
        return voti
    def getAllActors(self, r1,r2):
        actors = DAO.getAllActors(r1,r2)
        return actors

    def buildGraph(self, r1, r2):
        self._grafo.clear()
        self._attori = DAO.getAllActors(r1,r2)
        self._grafo.add_nodes_from(self._attori)
        for a in self._attori:
            self._idMapActors[a.id] = a
        self._archi= DAO.getAllEdgesPesati(r1,r2, self._idMapActors)
        for a in self._archi:
            self._grafo.add_edge(a.actor1, a.actor2, weight=a.peso)

    def getTop5(self):
        archiO = self._grafo.edges
        return sorted(archiO(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getConnessaInfo(self):
        components = list(nx.connected_components(self._grafo))
        largest = max(components, key=len)
        subGrafo = self._grafo.subgraph(largest).copy()
        return len(components), largest

    def getNumNodes(self):
        return len(self._grafo.nodes)
    def getNumEdges(self):
        return len(self._grafo.edges)
    def getPercorsoLungo(self):
        self._bestPath = []
        parziale = []
        for n in self._grafo.nodes:
            parziale.append(n)
            self.ricorsione(parziale)
        return self._bestPath

    def ricorsione(self, parziale):
        ultimo = parziale[-1]
        data = ultimo.date_of_birth
        vicini =  list(self._grafo.neighbors(ultimo))
        successori= []
        for v in vicini:
            if v not in parziale and v.date_of_birth > data:
                successori.append(v)
        #ottimo- non ci sono più nodi
        if len(successori) == 0 and len(parziale) > self._lun:
            self._lun = len(parziale)
            self._bestPath = copy.deepcopy(parziale)
            return self._bestPath

        #vado avanti
        for n in successori:
            if n.date_of_birth > data:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()

        pass

