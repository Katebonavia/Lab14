import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.choiceNode = None
        self.choiceStore = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStores(self):
        stores=self._model.getStores()
        for i in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(data=i, text=i.store_name, on_click=self.pickStore))
        self._view.update_page()

    def pickStore(self, e):
        self.choiceStore = e.control.data

    def handleCreaGrafo(self, e):
        maxGiorni = self._view._txtIntK.value
        if maxGiorni == '':
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('K non valido, inserire un valore', color='red'))
            return
        try:
            intMaxG = int(maxGiorni)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('K non valido, inserire un valore', color='red'))
            return
        self._model.buildGraph(self.choiceStore.store_id, intMaxG)
        nodi, archi = self._model.getDetGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Numero nodi: {nodi}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero archi: {archi}'))
        for node in self._model.getNodi():
            self._view._ddNode.options.append(ft.dropdown.Option(data=node, text=node.order_id, on_click=self.pickNode))
        self._view.update_page()

    def pickNode(self, e):
        self.choiceNode = e.control.data

    def handleCerca(self, e):
        longestPath = self._model.findLongestPath(self.choiceNode)
        for i in longestPath:
            self._view.txt_result.controls.append(ft.Text(f'{i.order_id}'))

    def handleRicorsione(self, e):
        pass
