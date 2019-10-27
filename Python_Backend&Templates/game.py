import cx_Oracle


class BET:
    def __enter__(self):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        self.__db = connection
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self):
        self.__db.commit()
        self.__cursor.close()
        self.__db.close()

    def create_bet(self, login, id, money, mult, date, field):
        self.__enter__()
        result = self.__cursor.callfunc("BETPACKAGE.CREATE_BET", cx_Oracle.STRING, [login, id, money, mult, date, field])
        self.__exit__()
        return result



    def get_bet(self, login):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor = connection.cursor()
        query = 'select * from table(BETPACKAGE.GET_BET(:userLogin))'
        cursor.execute(query, userLogin=login)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def get_bets_id(self, login):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor=connection.cursor()
        query = 'select * from table(BETPACKAGE.GET_BETS_ID(:userLogin))'
        cursor.execute(query, userLogin=login)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def generate_id(self):
        self.__enter__()
        result = self.__cursor.callfunc("BETPACKAGE.GENERATE_BETID", cx_Oracle.STRING)
        return result

    def double_bet(self, login):
        self.__enter__()
        self.__cursor.callproc("BETPACKAGE.DOUBLE_BET", [login])
        self.__exit__()

    def cancel_bet(self, login):
        self.__enter__()
        self.__cursor.callproc("BETPACKAGE.CANCEL_BET", [login])
        self.__exit__()


class GAME:
    def __enter__(self):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        self.__db = connection
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self):
        self.__db.commit()
        self.__cursor.close()
        self.__db.close()

    def generate_random_number(self):
        self.__enter__()
        result = self.__cursor.callfunc("GAMEPACKAGE.GENERATE_RANDOM_NUMBER", cx_Oracle.STRING)
        self.__exit__()
        return result

    def play_game(self, login,number):
        self.__enter__()
        result = self.__cursor.callfunc("GAMEPACKAGE.PLAYGAME", cx_Oracle.STRING, [login,number])
        self.__db.commit()
        self.__cursor.close()
        self.__db.close()
        return result