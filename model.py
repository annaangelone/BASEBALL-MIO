import copy
import itertools

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._years = DAO.getYears()
        self._grafo = nx.Graph()
        self._squadre = []

        self._idMap = {}

        self._bestPath = []
        self._bestObj = 0



    def squadreAnno(self, anno):
        self._squadre = DAO.getSquadreAnno(anno)

        for s in self._squadre:
            self._idMap[s.ID] = s

        return self._squadre


    def buildGraph(self, anno):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._squadre)

        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v:
                    salarioU = DAO.getSalarioSquadra(u.ID, anno)[0]
                    salarioV = DAO.getSalarioSquadra(v.ID, anno)[0]

                    salarioTot = salarioU + salarioV

                    self._grafo.add_edge(u, v, weight=salarioTot)


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)


    def getDettagliSquadra(self, squadra):

        vicini = self._grafo.neighbors(squadra)

        listaSquadreVicine = []
        for v in vicini:
            peso = self._grafo[squadra][v]["weight"]
            listaSquadreVicine.append((v, peso))

        listaSquadreVicine.sort(key=lambda x: x[1], reverse=True)

        return listaSquadreVicine


    def getPercorso(self, v0):
        self._bestPath = []
        self._bestObj = 0

        parziale = [v0]

        listaVicini = []

        for v in self._grafo.neighbors(v0):
            listaVicini.append((v, self._grafo[v0][v]["weight"]))

        listaVicini.sort(key=lambda x:x[1], reverse=True)

        parziale.append(listaVicini[0][0])

        self._ricorsione(parziale)

        return self._bestPath, self._bestObj



    def _ricorsione(self, parziale):
        if self.getBestObj(parziale) > self._bestObj:
            self._bestObj = self.getBestObj(parziale)
            self._bestPath = copy.deepcopy(parziale)

        listaVicini = []

        for v in self._grafo.neighbors(parziale[-1]):
            listaVicini.append((v, self._grafo[parziale[-1]][v]["weight"]))

        listaVicini.sort(key=lambda x: x[1], reverse=True)

        for nodo in listaVicini:
            if nodo[1] < self._grafo[parziale[-1]][parziale[-2]]["weight"] and nodo[0] not in parziale:
                parziale.append(nodo[0])
                self._ricorsione(parziale)
                parziale.pop()
                return



    def getBestObj(self, parziale):
        pesoTot = 0

        for i in range(len(parziale)-1):
            pesoTot += self._grafo[parziale[i]][parziale[i+1]]["weight"]

        return pesoTot


    def getPeso(self, n1, n2):
        return self._grafo[n1][n2]["weight"]



