import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.stores = DAO.getStores()
        self.nodes = None
        self._idMapsNodes={}
        self.edges=None
        self._graph = nx.DiGraph()
        self.longestPath=[]

    def getStores(self):
        return self.stores

    def buildGraph(self, storeId, K):
        self.nodes = DAO.getNodes(storeId)
        self._graph.add_nodes_from(self.nodes)
        for i in self.nodes:
            self._idMapsNodes[i.order_id]=i
        self.edges=DAO.getEdges(storeId, self._idMapsNodes, K)
        for e in self.edges:
            self._graph.add_edge(e.v1, e.v2, weight=e.peso)

    def getDetGraph(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def findLongestPath(self, v0):
        for i in nx.all_simple_paths(self._graph, v0, self._graph.nodes):
            if len(i)>len(self.longestPath):
                self.longestPath=i
        return self.longestPath

    def getNodi(self):
        return self._graph.nodes





