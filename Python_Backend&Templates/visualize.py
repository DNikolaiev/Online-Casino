import cx_Oracle


class graph1:

    def user_maxbet(self):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor = connection.cursor()
        query = 'SELECT  BET_DATE, MAX(BET_MONEY) FROM BET  GROUP BY BET_DATE'
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def user_betcount(self):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor = connection.cursor()
        query = 'SELECT BET_NAME, COUNT(BET_ID) FROM BET  GROUP BY BET_NAME'
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

