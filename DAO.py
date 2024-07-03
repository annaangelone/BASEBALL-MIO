from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = ("""select distinct year
                    from teams
                    where year >= 1980
                """)
        cursor.execute(query,)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadreAnno(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""select distinct *
                    from teams
                    where year = %s
                    """)
        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalarioSquadra(team_id, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""select s.teamID, sum(s.salary) as totSalary
                    from salaries s, appearances a
                    where s.teamID = %s and s.year = %s and a.playerID = s.playerID
                    and s.year = a.year
                    group by s.teamID""")
        cursor.execute(query, (team_id, anno))

        for row in cursor:
            result.append(row["totSalary"])

        cursor.close()
        conn.close()
        return result