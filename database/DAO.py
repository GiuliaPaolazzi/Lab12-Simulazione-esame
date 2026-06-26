from database.DB_connect import DBConnect
from model.actor import Actor
from model.arco import Arco


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating 
                    from ratings r
                    order by r.avg_rating 
                    """

        cursor.execute(query)

        for row in cursor:
            results.append((row["avg_rating"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllActors(r1,r2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.id, n.name, n.height, n.date_of_birth, n.known_for_movies 
                    from names n, ratings r,movie m , role_mapping rm
                    where r.movie_id = m.id and m.id= rm.movie_id and n.id= rm.name_id 
                    and n.date_of_birth is not null
                    and r.avg_rating between %s and %s"""

        cursor.execute(query,(r1,r2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdgesPesati(r1,r2,idMapA):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.actorId as actor1, t2.actorId as actor2, sum(t1.income) as peso, count(t1.movieid )
            from(select n.id as actorId, m.id as movieId, cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned) as income
            from names n, ratings r,movie m , role_mapping rm
            where r.movie_id = m.id and m.id= rm.movie_id and n.id= rm.name_id 
            and n.date_of_birth is not null
            and r.avg_rating between %s and %s
            and m.worlwide_gross_income is not null) t1, 
            (select n.id as actorId, m.id as movieId, cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned) as income
            from names n, ratings r,movie m , role_mapping rm
            where r.movie_id = m.id and m.id= rm.movie_id and n.id= rm.name_id 
            and n.date_of_birth is not null
            and r.avg_rating between %s and %s
            and m.worlwide_gross_income is not null)t2
            where t1.movieId = t2.movieId and t1.actorId < t2.actorId
            group by t1.actorId, t2.actorId
            order by peso desc"""

        cursor.execute(query,(r1,r2, r1,r2))

        for row in cursor:
            results.append(Arco(idMapA[row["actor1"]],idMapA[row["actor2"]],row["peso"]))

        cursor.close()
        conn.close()
        return results
