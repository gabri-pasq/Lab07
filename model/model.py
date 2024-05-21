import copy
from copy import deepcopy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.risultatotTemp = []
        self.situazioni = []
        self.md = MeteoDao()
        self.sequenza_perfetta = []
        self.poss = []
        self.costo = None
        self.risultatoInutile = None
        self.risultato = None
        self.nMese = None
        self.listaSituazioni = []

    def umiditaMedie(self, nMese):
        return self.md.get_avg_umidita(nMese)

    def gestioneMinimo(self, nMese):
        self.nMese = nMese
        self.costo = 99999999999
        self.risultato = None
        self.risultatoInutile = None
        self.listaSituazioni = self.md.get_quindici(str(self.nMese))
        self.creoPossibilita([])

    def creoPossibilita(self, poss: list):
        if len(poss) == 15:
            costoTemp = self.definisciCosto(poss)
            if costoTemp < self.costo:
                self.costo = costoTemp
                self.risultatoInutile = copy.deepcopy(poss)
                self.risultato = copy.deepcopy(self.risultatotTemp)
            return poss
        else:
            for citta in ['Torino', 'Milano', 'Genova']:
                nuova = poss + [citta]
                if self.puliziaGiorni(nuova):
                    self.creoPossibilita(nuova)

    def puliziaGiorni(self, sequenza_finita):
        if len(sequenza_finita) == 15:
            fatte = []
            for citta in sequenza_finita:
                if citta not in fatte:
                    fatte.append(citta)
                    if sequenza_finita.count(citta) > 6:
                        return False
                    if self.citta_consecutive(sequenza_finita, citta) < 3:
                        return False
            return True
        else:
            return True

    def citta_consecutive(self, lista, elemento):
        conteggio_consecutivo = 0
        consecutivi = []
        for citta in lista:
            if citta == elemento:
                conteggio_consecutivo += 1
            else:
                if conteggio_consecutivo > 0:
                    consecutivi.append(conteggio_consecutivo)
                    conteggio_consecutivo = 0
        if conteggio_consecutivo > 0:
            consecutivi.append(conteggio_consecutivo)
        return min(consecutivi)

    def definisciCosto(self, poss):
        costo = 0
        giorno = 0
        self.risultatotTemp = []
        for situazione in self.listaSituazioni:
            if giorno > 0:
                if situazione.data.day == (giorno + 1) and situazione.localita == poss[
                    giorno] and situazione.localita != poss[giorno - 1]:
                    costo += situazione.umidita + 200
                    giorno += 1
                    self.risultatotTemp.append(situazione)
                elif situazione.data.day == (giorno + 1) and situazione.localita == poss[giorno]:
                    costo += situazione.umidita
                    giorno += 1
                    self.risultatotTemp.append(situazione)
            elif situazione.data.day == (giorno + 1) and situazione.localita == poss[giorno]:
                costo += situazione.umidita
                giorno += 1
                self.risultatotTemp.append(situazione)
        return costo
