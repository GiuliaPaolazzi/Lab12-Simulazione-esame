import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceRating2= None
        self._choiceRating1 = None
        self._grafBool = False

    def fillDDsRating(self):
        ratings = list(self._model.getAllRatings())
        for r in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(r))
            self._view._ddrating2.options.append(ft.dropdown.Option(r))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        #controlli
        r1= self._view._ddrating1.value
        r2= self._view._ddrating2.value
        if r1 == None or r2 == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione scegliere entrambi i voti",color="red"))
            self._view.update_page()
            return
        elif r2<= r1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione il secondo voto deve essere strettamente > del primo", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(r1,r2)
        nN= self._model.getNumNodes()
        nA= self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {nN}", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {nA}", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Top 5 archi:"))
        self._grafBool = True
        top5 = self._model.getTop5()
        for e in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{e[0]}->{e[1]} - {e[2]["weight"]}"))
        nC, largest = self._model.getConnessaInfo()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero componenti connesse:{nC}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Nodi della componente maggiore (lunghezza = {len(largest)}):"))
        for n in largest:
            self._view.txt_result.controls.append(
                ft.Text(n))


        self._view.update_page()


    def handleCammino(self, e):
        if self._grafBool==False:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Creare prima il grafo", color="red"))
            self._view.update_page()
            return
        percorso= list(self._model.getPercorsoLungo())
        if len(percorso)==0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non ho trovato alcun percorso"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ecco il percorso più lungo di lunghezza {len(percorso)}:"))
        for n in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{n} - {n.date_of_birth}"))

        self._view.update_page()
        return

        self._view.update_page()
