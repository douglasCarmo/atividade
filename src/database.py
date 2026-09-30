import sqlite3
from typing import Optional, Dict, Any

class DatabaseManager:
    """Gerencia a conexão e operações no banco de dados SQLite."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Abre a conexão e ativa chaves estrangeiras."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def create_tables(self) -> None:
        """Cria as tabelas de aeronaves, pilotos e agendamentos."""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aeronaves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                modelo TEXT NOT NULL,
                status_manutencao TEXT NOT NULL CHECK(status_manutencao IN ('LIBERADO', 'EM_INSPECAO', 'EM_MANUTENCAO'))
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aeronave_id INTEGER NOT NULL,
                data_hora TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('AGENDADO', 'CANCELADO', 'CONCLUIDO')),
                FOREIGN KEY (aeronave_id) REFERENCES aeronaves (id)
            );
        """)
        self.conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Executa consultas SELECT e retorna os resultados como dicionários."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def execute_statement(self, query: str, params: tuple = ()) -> int:
        """Executa instruções INSERT/UPDATE/DELETE e retorna o id gerado."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid

    def close() -> None:
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            self.conn = None