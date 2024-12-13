import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path='uav_surveillance.db'):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        """Create necessary database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Mission logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mission_logs (
                    id INTEGER PRIMARY KEY,
                    start_time DATETIME,
                    end_time DATETIME,
                    start_coordinates TEXT,
                    end_coordinates TEXT
                )
            ''')

            # Anomaly logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS anomaly_logs (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME,
                    coordinates TEXT,
                    evidence_path TEXT
                )
            ''')

            conn.commit()

    def log_mission_start(self, coordinates):
        """Log mission start details"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO mission_logs (start_time, start_coordinates)
                VALUES (?, ?)
            ''', (datetime.now(), str(coordinates)))
            conn.commit()

    def log_mission_end(self):
        """Update mission end details"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE mission_logs
                SET end_time = ?
                WHERE end_time IS NULL
            ''', (datetime.now(),))
            conn.commit()

    def log_anomaly(self, coordinates):
        """Log anomaly details"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO anomaly_logs (timestamp, coordinates)
                VALUES (?, ?)
            ''', (datetime.now(), str(coordinates)))
            conn.commit()

    def store_evidence(self, evidence_frame):
        """Store evidence frame"""
        # Implement file storage logic for evidence frames
        pass