import sqlite3
import sys
import breakout
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.piano_cl.clicked.connect(self.piano_call_new_window)
        self.leader_board()

    def db_nick(self):
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        self.last_id = cur.execute("""SELECT id FROM players_name ORDER BY id DESC LIMIT 1""").fetchall()
        self.last_id = [l[0] for l in self.last_id]
        # cur.execute("""INSERT INTO players_name(name, id, max_score) VALUES(?, ?, 0) """,
        #             (self.nickname, self.last_id[0] + 1))
        # con.commit()

    def leader_board(self):
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        self.line = cur.execute("""SELECT * FROM leader_board""").fetchall()
        self.line = sorted(self.line, key=lambda x: x[2], reverse=True)

        cur.execute("""DELETE FROM leader_board""")
        for m in range(len(self.line)):
            self.textBrowser.append(F'#{m + 1}  Имя: {self.line[m][1]}  Кол-во очков: {self.line[m][2]}')
            cur.execute("""INSERT INTO leader_board(id, player_name, score) VALUES(?, ?, ?)""", (self.line[m][0],
                                                                                                 self.line[m][1],
                                                                                                 self.line[m][2],))
            con.commit()

    def piano_call_new_window(self):
        self.nickname = self.player_name_ent.text()
        self.db_nick()
        ex.close()
        breakout.Breakout().run()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
