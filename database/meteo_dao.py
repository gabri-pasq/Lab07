from database.DB_connect import DBConnect
from model.situazione import Situazione
from model.situazione import Riassunto


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    def get_avg_umidita(self, nMese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita,avg( s.Umidita) as media
                        FROM situazione s
                        where month(`Data`) = %s
                        group by s.Localita
                        ORDER BY s.Data asc"""
            cursor.execute(query, (nMese,))
            for row in cursor:
                result.append(Riassunto(row["Localita"],
                                        row["media"]))
            cursor.close()
            cnx.close()
        return result

    def get_quindici(self, nMese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s
                        where month(`Data`) = %s and  DAY(`Data`)<'16'
                        ORDER BY s.Data asc"""
            cursor.execute(query, (nMese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result
