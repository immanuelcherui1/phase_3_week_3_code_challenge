# lib/config.py
import sqlite3

CONN = sqlite3.connect('restaurants.db')
CURSOR = CONN.cursor()
