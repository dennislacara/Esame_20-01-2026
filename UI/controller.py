import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        n_alb = self.controllo_n_alb(self._view.txtNumAlbumMin.value)
        if n_alb is None:
            print(n_alb)
            return
        else:
            self._model.load_artists_with_min_albums(n_alb)
            if not self._model.artists_id_with_min_albums:
                print("CONTROLLER: lista del model 'artists_with_min_albums' vuota")
                self._view.show_alert('Non ci sono artisti che abbiano almeno tale numero di album')
                return
            else:
                self._model.build_graph()
                print('CONTROLLER: grafo creato')
                self.attiva_tasti_view()
                #gestione view
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f'Nodi: {self._model._graph.number_of_nodes()} - Archi: {self._model._graph.number_of_edges()}'))
                #gestione della ddArtist
                self._view.ddArtist.options.clear()
                self._view.ddArtist.value = ''
                for artist_id in self._model._graph:
                    artista = self._model.map_artists[artist_id]
                    self._view.ddArtist.options.append(ft.dropdown.Option(key = str(artista.id) ,text = artista.name))
                print(self._view.ddArtist.value)
                self._view.update_page()

    def handle_connected_artists(self, e):
        id_artista = self.controlla_dd_value(self._view.ddArtist.value)
        if id_artista is None:
            return
        if len(self._view.txt_result.controls) >1:
            del self._view.txt_result.controls[1:]
        for i,j,data in self._model._graph.edges(id_artista, data=True):
            nome_artista = self._model.map_artists[j]
            self._view.txt_result.controls.append(ft.Text(f"{nome_artista}  -  {data['peso']}"))
        self._view.update_page()

    def handle_search_artists(self, e):
        d_min = self.controlla_d_min(self._view.txtMinDuration.value)
        n_art = self.controlla_max_artists(self._view.txtMaxArtists.value)
        if n_art and d_min:
            id_artista = self.controlla_dd_value(self._view.ddArtist.value)
            if id_artista not in self._model._graph:
                self._view.show_alert('Calcolare ARTISTI COLLEGATI')
                return
            else:
                id_artista = int(id_artista)
                percorso,valore = self._model.calcola_percorso(d_min, n_art, id_artista)
                if not percorso or not valore:
                    print('CONTROLLER: percorso vuoto')
                    self._view.show_alert('Percorso inesistente')
                    return
                else:
                    #gestioen view
                    self._view.txt_result.controls.clear()
                    percorso = [self._model.map_artists[i] for i in percorso]
                    self._view.txt_result.controls.append(ft.Text(f'Cammino di peso massimo a partire da {percorso[0]}:'))
                    self._view.txt_result.controls.append(ft.Text(f'LUNGHEZZA: {len(percorso)}'))

                    for i in percorso:
                        self._view.txt_result.controls.append(ft.Text(f'{i}'))
                    self._view.txt_result.controls.append(ft.Text(f'PESO MASSIMO: {valore}'))
                    self._view.update_page()




    def controllo_n_alb(self, txtField_value):
        if not txtField_value:
            self._view.show_alert("Inserire un valore")
            return
        else:
            if not txtField_value.isdigit():
                self._view.show_alert("Inserire un valore numerico positivo")
                return
            else:
                return int(txtField_value)

    def attiva_tasti_view(self):
        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.btnSearchArtists.disabled = False

    def controlla_dd_value(self, value):
        if value == '':
            self._view.show_alert("Scegliere un artista")
            return
        else:
            return int(value)

    def controlla_max_artists(self, txtField_value):
        if txtField_value is None:
            self._view.show_alert("Inserire un max di artisti")
            return
        else:
            if not txtField_value.isdigit():
                self._view.show_alert("Inserire un max di artisti valido")
                return
            else:
                n_art = int(txtField_value)
                if n_art >= 1 and n_art <= len(self._view.ddArtist.options):
                    return int(txtField_value)
                else:
                    self._view.show_alert("Inserire un max di artisti valido")
                    return

    def controlla_d_min(self, txtField_value):
        if txtField_value is None:
            self._view.show_alert("Inserire i minuti")
            return
        else:
            try:
                d_min = float(txtField_value)
                if d_min > 0:
                    return float(txtField_value)
                else:
                    self._view.show_alert("Inserire i minuti validi (maggiore di 0)")
                    return
            except Exception:
                self._view.show_alert("Inserire i minuti validi")
                return