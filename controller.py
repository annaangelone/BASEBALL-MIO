import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam = None

    def handleCreaGrafo(self, e):
        year = int(self._view._ddAnno.value)

        if year is None:
            self._view.create_alert("No year selected, please select an year")
            return

        self._model.buildGraph(year)

        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi"))

        self._view.update_page()


    def handleDettagli(self, e):
        squadra = self._selectedTeam

        if squadra is None:
            self._view.create_alert("No team selected, please select a team")
            return

        self._view._txt_result.controls.append(ft.Text(f"Adiacenti per la squadra {squadra}"))

        vicini = self._model.getDettagliSquadra(squadra)

        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]}; peso={v[1]}"))

        self._view.update_page()


    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()

        team = self._selectedTeam
        path, bestObj = self._model.getPercorso(team)

        self._view._txt_result.controls.append(ft.Text(f"Percorso con nodo di partenza {team} di peso totale={bestObj}"))

        for i in range(len(path)-1):
            self._view._txt_result.controls.append(ft.Text(f"{path[i]} --> {path[i+1]}; "
                                                           f"peso={self._model.getPeso(path[i],path[i+1])}"))

        self._view.update_page()



    def fillDDYears(self):
        years = self._model._years

        for y in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(y))


    def handleDDYearSelection(self, e):
        year = int(self._view._ddAnno.value)

        if year is None:
            self._view.create_alert("No year selected, please select an year")
            return

        squadre = self._model.squadreAnno(year)

        self._view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno {year}: {len(squadre)}"))

        for s in squadre:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{s}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=s, text=s.teamCode, on_click=self.readDDTeams))

        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}")


