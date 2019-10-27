import cx_Oracle


class USER:
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

    def get_money(self, login):
        self.__enter__()
        result = self.__cursor.callfunc("USERPACKAGE.SHOW_USER_MONEY", cx_Oracle.STRING, [login])
        return result

    def change_player_balance(self, login, amount):
        self.__enter__()
        self.__cursor.callproc("USERPACKAGE.CHANGE_PLAYER_BALANCE",
                                        [login, amount])
        self.__db.commit()
        self.__exit__()


    def identify_user(self, login):
        self.__enter__()
        result = self.__cursor.callfunc("USERPACKAGE.IDENTIFY_USER", cx_Oracle.STRING, [login])
        return result

    def get_user(self, login):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor = connection.cursor()
        query = 'select * from table(USERPACKAGE.GET_USER(:userLogin))'
        cursor.execute(query, userLogin=login)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def update_user(self, oldlogin, newlogin, mail, age,  name):
        self.__enter__()
        result = self.__cursor.callfunc("USERPACKAGE.UPDATE_USER", cx_Oracle.STRING,
                                        [oldlogin, newlogin, mail, age, name])
        self.__db.commit()
        self.__exit__()
        return result

class BANK:
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

    def get_bank_info(self, login):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor = connection.cursor()
        query = 'select * from table(BANKPACKAGE.GET_BANK_DATA(:userLogin))'
        cursor.execute(query, userLogin=login)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result



    def add_bank(self, login, card, expdate, adress):
        self.__enter__()
        result = self.__cursor.callfunc("BANKPACKAGE.ADD_PAYMENT", cx_Oracle.STRING,
                                        [login,card,expdate, adress])
        self.__db.commit()
        self.__exit__()
        return result

    def update_bank(self, login, oldcard, newcard, expdate, adress):
        self.__enter__()
        result = self.__cursor.callfunc("BANKPACKAGE.UPDATE_PAYMENT", cx_Oracle.STRING,
                                        [login, oldcard, newcard, expdate, adress])
        self.__db.commit()
        self.__exit__()
        return result

    def delete_bank(self, login, card):
        self.__enter__()
        result = self.__cursor.callfunc("BANKPACKAGE.DELETE_PAYMENT", cx_Oracle.STRING,
                                        [login, card])
        self.__db.commit()
        self.__exit__()
        return result

    def get_card(self, login):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        cursor = connection.cursor()
        query = 'select * from table(BANKPACKAGE.GET_CARD(:userLogin))'
        cursor.execute(query, userLogin=login)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result