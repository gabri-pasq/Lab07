import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text('Umidità medie per il mese selezionato:'))
        for r in self._model.umiditaMedie(self._view.dd_mese.value):
            self._view.lst_result.controls.append(ft.Text(str(r)))
            self._view.update_page()



    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f'Calcolo...'))
        self._view.update_page()
        self._model.gestioneMinimo(int(self._view.dd_mese.value))
        print(self._model.risultatoInutile)
        print(self._model.risultato)
        print(self._model.costo)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f'La sequenza ottima ha un costo di {self._model.costo}:'))
        for situazione in self._model.risultato:
            self._view.lst_result.controls.append(ft.Text(f'[{situazione.localita} - {situazione.data}] Umidità= {situazione.umidita}'))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

