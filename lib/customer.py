# lib/customer.py
from __init__ import CURSOR, CONN
from restaurant import Restaurant


class Customer:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, first_name, last_name, restaurant_id, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return (
            f"<Customer {self.id}: {self.first_name}, {self.last_name}, " +
            f"Restaurant ID: {self.restaurant_id}>"
        )

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str):
            self._first_name = first_name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str):
            self._last_name = last_name
        else:
            raise ValueError(
                "last name must be a non-empty string"
            )

    @property
    def restaurant_id(self):
        return self._restaurant_id

    @restaurant_id.setter
    def restaurant_id(self, restaurant_id):
        if type(restaurant_id) is int and Restaurant.find_by_id(restaurant_id):
            self._restaurant_id = restaurant_id
        else:
            raise ValueError(
                "restaurant_id must reference a restaurant in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Customer instances """
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            restaurant_id INTEGER,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Customer instances """
        sql = """
            DROP TABLE IF EXISTS customers;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with first_name, job last_name, and restaurant id values of the current Customer object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO customers (first_name, last_name, restaurant_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.first_name, self.last_name, self.restaurant_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def create(cls, first_name, last_name, restaurant_id):
        """ Initialize a new Customer instance and save the object to the database """
        customer = cls(first_name, last_name, restaurant_id)
        customer.save()
        return customer

    @classmethod
    def find_by_id(cls, id):
        """Return Customer object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM customers
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Customers object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        customer = cls.all.get(row[0])
        if customer:
            # ensure attributes match row values in case local instance was modified
            customer.first_name = row[1]
            customer.last_name = row[2]
            customer.restaurant_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            customer = cls(row[1], row[2], row[3])
            customer.id = row[0]
            cls.all[customer.id] = customer
        return customer

    
    
    # def update(self):
    #     """Update the table row corresponding to the current Employee instance."""
    #     sql = """
    #         UPDATE employees
    #         SET name = ?, job_title = ?, department_id = ?
    #         WHERE id = ?
    #     """
    #     CURSOR.execute(sql, (self.name, self.job_title,
    #                          self.department_id, self.id))
    #     CONN.commit()

    # def delete(self):
    #     """Delete the table row corresponding to the current Employee instance,
    #     delete the dictionary entry, and reassign id attribute"""

    #     sql = """
    #         DELETE FROM employees
    #         WHERE id = ?
    #     """

    #     CURSOR.execute(sql, (self.id,))
    #     CONN.commit()

    #     # Delete the dictionary entry using id as the key
    #     del type(self).all[self.id]

    #     # Set the id to None
    #     self.id = None

    

   
    # @classmethod
    # def get_all(cls):
    #     """Return a list containing one Employee object per table row"""
    #     sql = """
    #         SELECT *
    #         FROM employees
    #     """

    #     rows = CURSOR.execute(sql).fetchall()

    #     return [cls.instance_from_db(row) for row in rows]

    
    # @classmethod
    # def find_by_name(cls, name):
    #     """Return Employee object corresponding to first table row matching specified name"""
    #     sql = """
    #         SELECT *
    #         FROM employees
    #         WHERE name is ?
    #     """

    #     row = CURSOR.execute(sql, (name,)).fetchone()
    #     return cls.instance_from_db(row) if row else None

    # def reviews(self):
    #     """Return list of reviews associated with current employee"""
    #     from review import Review
    #     sql = """
    #         SELECT * FROM reviews
    #         WHERE employee_id = ?
    #     """
    #     CURSOR.execute(sql, (self.id,),)

    #     rows = CURSOR.fetchall()
    #     return [
    #         Review.instance_from_db(row) for row in rows
    #     ]
