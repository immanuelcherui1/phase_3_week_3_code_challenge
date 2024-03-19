from __init__ import CURSOR, CONN
from restaurant import Restaurant
from customer import Customer


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self,star_rating, restaurant_id, customer_id, id=None):
        self.id = id
        self.star_rating= star_rating
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.star_rating}, "
            + f"Restaurant: {self.restaurant_id},"
            + f"Customer: {self.customer_id}>"
        )

    
    @property
    def star_rating(self):
        return self._star_rating

    @star_rating.setter
    def star_rating(self, star_rating):
        if isinstance(star_rating, int) and star_rating <= 5:
            self._star_rating = star_rating
        else:
            raise ValueError(
                "rating must be a non-empty Integer"
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
                "restaurant_id must reference  restaurants in the database")

    
    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        if type(customer_id) is int and Customer.find_by_id(customer_id):
            self._customer_id = customer_id
        else:
            raise ValueError(
                "customer_id must reference  customers in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            restaurant_id INTEGER,
            customer_id INTEGER,
            star_rating INTEGER,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
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
        sql = """
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        review = cls.all.get(row[0])
        if review:
            # ensure attributes match row values in case local instance was modified
            review.year = row[1]
            review.summary = row[2]
            review.employee_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        sql = """
            SELECT *
            FROM reviews
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql = """
            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.year, self.summary,
                             self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        sql = """
            SELECT *
            FROM reviews
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]


