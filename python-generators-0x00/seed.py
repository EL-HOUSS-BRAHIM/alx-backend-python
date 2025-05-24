#!/usr/bin/python3
"""Database seeding and setup module."""
import mysql.connector
import csv
import os


def connect_db():
    """Connect to MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,0) NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def insert_data(connection, csv_file):
    """Insert data from CSV file into the database."""
    try:
        cursor = connection.cursor()
        if not os.path.exists(csv_file):
            print(f"Error: {csv_file} not found")
            return

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], row['age']))

        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except (mysql.connector.Error, FileNotFoundError) as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        
        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, 'user_data.csv')
            conn.close()
