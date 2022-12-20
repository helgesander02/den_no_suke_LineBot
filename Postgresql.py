import psycopg2


class database:
    def __init__(self, user_name, uid):
        self.user_name = user_name
        self.uid = uid
        self.Internal_Database_URL = "postgres://su:IqObEwxiLHJbo7aRzb8lyyOKiWBcVzfU@dpg-cegsd914rebaribgjg30-a.singapore-postgres.render.com/dennosuke_vsns"
        
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
