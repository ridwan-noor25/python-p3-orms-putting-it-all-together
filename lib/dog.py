import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    def save(self):
        sql = """
        INSERT INTO dogs(name,breed) VALUES(?, ?)
        """
        CURSOR.execute(sql,(self.name, self.breed))
        CONN.commit()

        self.id = CURSOR.lastrowid
    
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs(
        id INTEGER PRIMARY KEY,
        name TEXT,
        breed TEXT
        );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs;"
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)  
        dog.save()              
        return dog 

    @classmethod
    def new_from_db(cls,row):
        dogs = cls(row[1],row[2])
        dogs.id = row[0]
        return dogs
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs
    
    @classmethod
    def find_by_name(cls,name):
       sql = """
       SELECT * FROM dogs WHERE name = ?
       LIMIT 1
       """
       row = CURSOR.execute(sql,(name,)).fetchone() 
       return cls.new_from_db(row) if row else None 
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT * FROM dogs WHERE id = ?
        LIMIT 1
        """
        row = CURSOR.execute(sql,(id,)).fetchone()
        return cls.new_from_db(row) if row else None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ? " 
        "LIMIT 1"
        row = CURSOR.execute(sql, (name, breed)).fetchone()

        if row:
          return cls.new_from_db(row)
        else:
         insert_sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
        CURSOR.execute(insert_sql, (name, breed))
        CONN.commit()
        new_id = CURSOR.lastrowid

        dog = cls(name, breed)
        dog.id = new_id
        return dog
    
    
    def update(self):
        sql = """
        UPDATE dogs SET  name = ?, breed = ? WHERE id = ?
        """
        CURSOR.execute(sql,(self.name, self.breed, self.id))
        CONN.commit()
