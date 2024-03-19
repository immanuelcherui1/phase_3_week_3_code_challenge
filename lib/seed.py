#!/usr/bin/env python3

from __init__ import CONN, CURSOR
from restaurant import Restaurant
from customer import Customer

def seed_database():
    Review.drop_table()
    Customer.drop_table()
    Restaurant.drop_table()
    
    Restaurant.create_table()
    Customer.create_table()
    Review.create_table()

    # Create seed data
    sarova = Restaurant.create("Sarova", 20000)
    panari = Restaurant.create("Panari", 25000)
    
    amir = Customer.create("Amir", "Acco", sarova.id)
    bola = Customer.create("Bola", "Mnage", panari.id)
    charlie = Customer.create("Charlie", "Man", panari.id)
    dani = Customer.create("Dani", "Ben", sarova.id)
    hao = Customer.create("Hao", "Coord", panari.id)
    
    Review.create(5, sarova.id, amir.id)
    Review.create(1, panari.id, dani.id)
    Review.create(4, panari.id, hao.id)
    Review.create(5, sarova.id, charlie.id)
    Review.create(2, sarova.id, dani.id)
    Review.create(3, panari.id, amir.id)
    Review.create(4, sarova.id, hao.id)
    


seed_database()
print("Seeded database")
