import cx_Oracle


class LOGIN:
    def __enter__(self):
        ip = '127.0.0.1'
        port = 1521
        SID = 'XE'
        dns_tns = cx_Oracle.makedsn(ip, port, SID)
        connection = cx_Oracle.connect('dima', 'dima', dns_tns)
        self.__db = connection
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.__cursor.close()
        self.__db.close()

    def login_user(self, login, u_password):
        result = self.__cursor.callfunc("USERPACKAGE.LOGIN", cx_Oracle.STRING, [login, u_password])
        return result


class REG:
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
        self.__cursor.close()
        self.__db.close()

    def reg_user(self, login, u_password, u_mail, u_age, u_name):
        result = self.__cursor.callfunc("USERPACKAGE.REGISTRATE", cx_Oracle.STRING,
                                        [login, u_password, u_mail, u_age, u_name])
        self.__db.commit()
        self.__exit__()
        return result
