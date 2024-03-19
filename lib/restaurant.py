# lib/restaurant.py
from __init__ import CURSOR, CONN
from restaurant import Restaurant
from review import Review

class Restaurant:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}, {self.location}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if isinstance(price, int):
            self._price = price
        else:
            raise ValueError(
                "price must be a non-empty digit"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Restaurant instances """
        sql = """
            CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Restaurant instances """
        sql = """
            DROP TABLE IF EXISTS restaurants;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and price values of the current Restaurant instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO restaurants (name, price)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.price))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, price):
        """ Initialize a new Restaurant instance and save the object to the database """
        restaurant = cls(name, price)
        restaurant.save()
        return restaurant

    # def update(self):
    #     """Update the table row corresponding to the current Department instance."""
    #     sql = """
    #         UPDATE departments
    #         SET name = ?, location = ?
    #         WHERE id = ?
    #     """
    #     CURSOR.execute(sql, (self.name, self.location, self.id))
    #     CONN.commit()

    # def delete(self):
    #     """Delete the table row corresponding to the current Department instance,
    #     delete the dictionary entry, and reassign id attribute"""

    #     sql = """
    #         DELETE FROM departments
    #         WHERE id = ?
    #     """

    #     CURSOR.execute(sql, (self.id,))
    #     CONN.commit()

    #     # Delete the dictionary entry using id as the key
    #     del type(self).all[self.id]

    #     # Set the id to None
    #     self.id = None

    # @classmethod
    # def instance_from_db(cls, row):
    #     """Return a Department object having the attribute values from the table row."""

    #     # Check the dictionary for an existing instance using the row's primary key
    #     department = cls.all.get(row[0])
    #     if department:
    #         # ensure attributes match row values in case local instance was modified
    #         department.name = row[1]
    #         department.location = row[2]
    #     else:
    #         # not in dictionary, create new instance and add to dictionary
    #         department = cls(row[1], row[2])
    #         department.id = row[0]
    #         cls.all[department.id] = department
    #     return department

    # @classmethod
    # def get_all(cls):
    #     """Return a list containing a Department object per row in the table"""
    #     sql = """
    #         SELECT *
    #         FROM departments
    #     """

    #     rows = CURSOR.execute(sql).fetchall()

    #     return [cls.instance_from_db(row) for row in rows]

    # @classmethod
    # def find_by_id(cls, id):
    #     """Return a Department object corresponding to the table row matching the specified primary key"""
    #     sql = """
    #         SELECT *
    #         FROM departments
    #         WHERE id = ?
    #     """

    #     row = CURSOR.execute(sql, (id,)).fetchone()
    #     return cls.instance_from_db(row) if row else None

    # @classmethod
    # def find_by_name(cls, name):
    #     """Return a Department object corresponding to first table row matching specified name"""
    #     sql = """
    #         SELECT *
    #         FROM departments
    #         WHERE name is ?
    #     """

    #     row = CURSOR.execute(sql, (name,)).fetchone()
    #     return cls.instance_from_db(row) if row else None

    # def employees(self):
    #     """Return list of employees associated with current department"""
    #     from employee import Employee
    #     sql = """
    #         SELECT * FROM employees
    #         WHERE department_id = ?
    #     """
    #     CURSOR.execute(sql, (self.id,),)

    #     rows = CURSOR.fetchall()
    #     return [
    #         Employee.instance_from_db(row) for row in rows
    #     ]