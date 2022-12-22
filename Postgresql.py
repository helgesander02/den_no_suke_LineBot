import psycopg2
import os

class database:
    def __init__(self, user_name, uid):
        self.user_name = user_name
        self.uid = uid
        self.Internal_Database_URL = os.getenv('Internal_Database_URL')
        
    def add_food(self):
        conn = psycopg2.connect(self.Internal_Database_URL)
        cur = conn.cursor()
        cur.execute(f"SELECT ID, NAME, COUNT FROM DENNOSUKE WHERE ID='{self.uid}'")
        rows = cur.fetchall()
        c=0
        if rows == []:
            cur.execute(f"INSERT INTO DENNOSUKE (ID, NAME, COUNT) \
                        VALUES ('{self.uid}','{self.user_name}', 1)");
            c=1
            
        else:
            cur.execute(f"SELECT COUNT FROM DENNOSUKE WHERE ID='{self.uid}'")
            c = cur.fetchall()[0][0]
            cur.execute(f"UPDATE DENNOSUKE set COUNT = {c+1} where ID='{self.uid}'")
            c+=1
            
        conn.commit()
        conn.close()
        return c
    
    def add_food(self):
        conn = psycopg2.connect(self.Internal_Database_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM DENNOSUKE ORDER BY COUNT DESC LIMIT 3")
        rows = cur.fetchall()
        s=""
        if rows == []:
            s = "排行榜沒有善心人士"
        else:
            s = f"1.{rows[0][1]}餵食{rows[0][2]}次\n"
            s += f"2.{rows[1][1]}餵食{rows[1][2]}次\n"
            s += f"3.{rows[2][1]}餵食{rows[2][2]}次"
            
        conn.commit()
        conn.close()
        return s    
