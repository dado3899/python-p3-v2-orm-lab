from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = f'''
        INSERT INTO reviews(year,summary,employee_id)
        VALUES({self.year}, "{self.summary}", {self.employee_id})
        '''
        CURSOR.execute(sql)
        CONN.commit()
        # print(CURSOR.execute('SELECT * FROM reviews').fetchall()[-1])
        self.id = CURSOR.execute('SELECT * FROM reviews').fetchall()[-1][0]

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        new_r = Review(year,summary,employee_id)
        new_r.save()
        return new_r
   
    @classmethod
    def instance_from_db(cls, row):
        # print(row)
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        # return Review()
        robj = CURSOR.execute(f'''
        SELECT * FROM reviews
        WHERE id = {row[0]}
        ''').fetchone()
        if robj:
            return Review(
                id = robj[0],
                year= robj[1],
                summary = robj[2],
                employee_id = robj[3]
            )
        else:
            return Review.create(row[1],row[2],row[3])

   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        robj = CURSOR.execute(f'''
        SELECT * FROM reviews
        WHERE id = {id}
        ''').fetchone()
        if robj:
            return Review(
                id = robj[0],
                year= robj[1],
                summary = robj[2],
                employee_id = robj[3]
            )
        else:
            return None


    def update(self):
        """Update the table row corresponding to the current Review instance."""
        CURSOR.execute('''
        UPDATE reviews
        SET year = ?, summary = ?, employee_id = ?
        WHERE id = ?
        ''', (self.year,self.summary,self.employee_id,self.id))
        CONN.commit()


    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        CURSOR.execute('''
        DELETE FROM reviews
        WHERE id = ?
        ''', (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        all_reviews = CURSOR.execute('''
        SELECT * FROM reviews
        ''').fetchall()
        r_list = []
        for table_review in all_reviews:
            r_list.append(Review(
                id = table_review[0],
                year= table_review[1],
                summary = table_review[2],
                employee_id = table_review[3]
            ))
        return r_list

    def get_year(self):
        return self._year
    def set_year(self,value):
        if type(value) is int and 2000<=value:
            self._year = value
        else:
            raise ValueError("Not valid year")
    year = property(get_year,set_year)

    def get_summary(self):
        return self._summary
    def set_summary(self,value):
        if type(value) is str and 0<len(value):
            self._summary = value
        else:
            raise ValueError("Not valid summary")
    summary = property(get_summary,set_summary)

    def get_employee_id(self):
        return self._employee_id
    def set_employee_id(self,value):
        employee = Employee.find_by_id(value)
        if type(employee) is Employee:
            self._employee_id = value
        else:
            raise ValueError("Not valid Id")
    employee_id = property(get_employee_id,set_employee_id)


