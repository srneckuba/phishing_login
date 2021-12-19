import base64, hashlib
from cryptography.fernet import Fernet
import sqlite3

server_directory = ""
database_path = ""

class encryption():
    def __init__(self, password):
        self.enc = Fernet(base64.urlsafe_b64encode(hashlib.md5(password.encode("utf-8")).hexdigest().encode("utf-8")))
    def encrypt(self, message):
        return self.enc.encrypt(message.encode("utf-8"))
    def decrypt(self, message):
        return self.enc.decrypt(message)
class settings():
    auto_Pstep2 = "N"
    auto_Pstep3 = "N"
    auto_Nstep3 = "N"
    auto_Pstep4 = "N"
    def set(self, name, value):
        if name == "auto_Pstep2":
            self.auto_Pstep2 = value
        elif name == "auto_Pstep3":
            self.auto_Pstep3 = value
        elif name == "auto_Nstep3":
            self.auto_Nstep3 = value
        elif name == "auto_Pstep4":
            self.auto_Pstep4 = value
class Session:
    def __init__(self, cookie):
        database_connection = sqlite3.connect(server_directory + database_path)
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("select * from accesses where cookie==? order by cookie ASC;", (cookie, )).fetchall()
        self.ID = cookie
        self.time = data[0][1]
        self.IP = data[0][2]
        self.network = data[0][3]
        self.link_name = data[0][4]
        self.step1 = data[0][5]
        self.step2 = data[0][6]
        self.step3 = data[0][7]
        self.Pstep2 = data[0][8]
        self.Pstep3 = data[0][9]
        self.Nstep3 = data[0][10]
        self.Pstep4 = data[0][11]
        database_connection.close()
    def set(self, name, value):
        if name == "step1":
            self.step1 = value
        elif name == "step2":
            self.step2 = value
        elif name == "step3":
            self.step3 = value
        elif name == "Pstep2":
            self.Pstep2 = value
        elif name == "Pstep3":
            self.Pstep3 = value
        elif name == "Nstep3":
            self.Nstep3 = value
        elif name == "Pstep4":
            self.Pstep4 = value
    def save(self):
        database_connection = sqlite3.connect(server_directory + database_path)
        database_cursor = database_connection.cursor()
        database_cursor.execute("delete from accesses where cookie==?", (self.ID, ));
        database_cursor.execute("insert into accesses values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.ID, self.time, self.IP, self.network, self.link_name, self.step1, self.step2, self.step3, self.Pstep2, self.Pstep3, self.Nstep3, self.Pstep4, ))
        database_connection.commit()
        database_connection.close()
    def delete(self):
        database_connection = sqlite3.connect(server_directory + database_path)
        database_cursor = database_connection.cursor()
        database_cursor.execute("delete from accesses where cookie==?", (self.ID, ));
        database_connection.commit()
        database_connection.close()
    def reload(self):
        database_connection = sqlite3.connect(server_directory + database_path)
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("select * from accesses where cookie==? order by cookie ASC;", (self.ID, )).fetchall()
        self.time = data[0][1]
        self.IP = data[0][2]
        self.network = data[0][3]
        self.link_name = data[0][4]
        self.step1 = data[0][5]
        self.step2 = data[0][6]
        self.step3 = data[0][7]
        self.Pstep2 = data[0][8]
        self.Pstep3 = data[0][9]
        self.Nstep3 = data[0][10]
        self.Pstep4 = data[0][11]
        database_connection.close()
