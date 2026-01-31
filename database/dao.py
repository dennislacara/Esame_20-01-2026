from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_artists_with_min_albums(min_albums):
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection, read_artists_with_min_albums()")
            return

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT a.artist_id 
                FROM album a
                GROUP BY a.artist_id 
                HAVING COUNT(*) >= %s
                """
        try:
            cursor.execute(query, (min_albums,))
            for row in cursor:
                result.append(int(row['artist_id']))
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def load_archi(lista_id_artisti):
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection, load_archi()")
            return

        result = []
        cursor = conn.cursor(dictionary=True)
        placeholders = ', '.join(['%s'] * len(lista_id_artisti))
        query = f"""
                with tab_canzoni as(
                SELECT t.id as track_id, t.genre_id , a.artist_id 
                FROM track t left outer join album a on t.album_id = a.id
                WHERE a.artist_id in ({placeholders})
                ),
                tab_coppie as(
                SELECT distinct a.artist_id as id1, b.artist_id as id2, a.genre_id 
                FROM tab_canzoni a, tab_canzoni b
                WHERE a.genre_id = b.genre_id 
                    and a.track_id > b.track_id
                    and a.artist_id > b.artist_id
                )
                SELECT id1, id2, count(*) as peso
                FROM tab_coppie
                GROUP BY id1, id2
                """
        try:

            cursor.execute(query, tuple(lista_id_artisti))
            for row in cursor:
                result.append( (int(row['id1']),int(row['id2']), int(row['peso']) ) )
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def read_artisti_d_min(artisti_grafo, d_min):
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection, load_archi()")
            return

        result = []
        cursor = conn.cursor(dictionary=True)
        placeholders = ', '.join(['%s'] * len(artisti_grafo))
        query = f"""
                with tab as(
                SELECT a.artist_id as id, (t.milliseconds/60000) as minuti
                FROM track t
                LEFT OUTER JOIN album a ON t.album_id = a.id
                WHERE a.artist_id in ({placeholders})
                )
                SELECT *
                FROM tab t
                WHERE t.minuti > %s
                """
        try:
            info = tuple(artisti_grafo) + tuple([str(d_min)])
            cursor.execute(query, info)
            for row in cursor:
                print(row['id'], row['minuti'])
                result.append(int(row['id']))
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result
