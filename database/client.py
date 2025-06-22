"""
client.py

This module defines the project database CRUD operations.

Author: Marcus Zucareli
Date: 2025-06-21
"""
import sqlite3
import os
import pandas as pd


class Database():
    def __init__(self, path):
        self.database_path = path
        self.con = sqlite3.connect(self.database_path)
        self.c = self.con.cursor()
        
    def create_table(self, table_name, columns) -> None:
        """
        Creates a table in the project database.

        Args:
        table_name (str): The name of the table.
        columns (dict(str:str)): A dict with keys as the name of
         the columns, and value as it's types.

        Returns:
            None
        """
        model_sql = ", ".join(
            f"{nome} {tipo}" for nome, tipo in columns.items())
        self.c.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({model_sql})")

    def insert_data(self, table, data) -> None:
        """
        Insert a record in a table in the project database.

        Args:
        table (str): The name of the table.
        data (dict(str:str)): A dict with keys as the name of
         the column, and value as the value to insert.

        Returns:
            None
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())
        self.c.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
            
    def delete_data(self, table, condition) -> None:
        """
        Delete a record in a table using a where condition.

        Args:
        table (str): The name of the table.
        condition (str): The condition to delete records.

        Retuns:
        None
        """
        self.c.execute(f"DELETE FROM {table} WHERE {condition}")

    def update_record(self, table, data, condition) -> None:
        """
        Update a record in a table using a where condition.

        Args:
        table (str): The name of the table.
        condition (str): The condition to delete records.
        data (str): Dictionary in the format {column: value}, representing the columns to update.

        Retuns:
        None
        """
        set_clause = ", ".join(f"{col} = ?" for col in data.keys())
        values = tuple(data.values())
        self.c.execute(
            f"UPDATE {table} SET {set_clause} WHERE {condition}", values)
        
    def get_data(self, table, condition) -> pd.DataFrame:
        """
        Retrieve data from a database

        Args:
        table (str): The name of the table.
        condition (str): The condition to delete records.

        Returns:
            pd.Dataframe
        """
        df = pd.read_sql_query(
            f"SELECT * FROM {table} WHERE {condition}", self.con)
        return df
