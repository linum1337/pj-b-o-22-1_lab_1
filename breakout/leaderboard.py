import sqlite3


class Leaderboard():

    def db_func(self, score=None):
        self.score = score
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()

        self.last_id = cur.execute("""SELECT id FROM players_name ORDER BY id DESC LIMIT 1""").fetchall()
        self.last_id = [l[0] for l in self.last_id]

        self.last_score = cur.execute("""SELECT max_score FROM players_name ORDER BY id DESC LIMIT 1""").fetchall()
        self.last_score = [n[0] for n in self.last_score]

        if self.last_score[0] < self.score:
            cur.execute("""UPDATE players_name SET max_score = ? WHERE id = ?""", (self.score, self.last_id[0],))
            con.commit()

        self.last_inserted_name = cur.execute("""SELECT name, max_score FROM players_name ORDER 
           BY id DESC LIMIT 1""").fetchall()
        print(self.last_inserted_name)

        cur.execute("""INSERT INTO leader_board(id, player_name, score) VALUES(?, ?, ?) """,
                    (self.last_id[0], self.last_inserted_name[0][0], self.last_inserted_name[0][1],))
        con.commit()
