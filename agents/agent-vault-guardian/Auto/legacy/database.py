"""
Classification History Tracker
Database module for storing classification history
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class HistoryDatabase:
    def __init__(self, db_path: str):
        """
        Initialize the history database

        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """
        Initialize the database with required tables
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create classifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_path TEXT NOT NULL,
                document_name TEXT NOT NULL,
                original_category TEXT,
                assigned_category TEXT NOT NULL,
                confidence_score REAL,
                classifier_model TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                feedback_status TEXT DEFAULT 'none'  -- none, positive, negative
            )
        ''')

        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON classifications(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_document_name ON classifications(document_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assigned_category ON classifications(assigned_category)')

        conn.commit()
        conn.close()

        print(f"Database initialized at {self.db_path}")

    def add_classification(self, document_path: str, assigned_category: str, original_category: str = None,
                         confidence_score: float = None, classifier_model: str = None, metadata: dict = None) -> int:
        """
        Add a new classification record to the database

        Args:
            document_path (str): Path to the document that was classified
            assigned_category (str): Category assigned to the document
            original_category (str, optional): Original category if known
            confidence_score (float, optional): Confidence score of the classification
            classifier_model (str, optional): Model used for classification
            metadata (dict, optional): Additional metadata about the classification

        Returns:
            int: ID of the newly inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        document_name = os.path.basename(document_path)

        cursor.execute('''
            INSERT INTO classifications
            (document_path, document_name, original_category, assigned_category, confidence_score, classifier_model, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            document_path,
            document_name,
            original_category,
            assigned_category,
            confidence_score,
            classifier_model,
            json.dumps(metadata) if metadata else None
        ))

        record_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return record_id

    def get_classification_by_id(self, record_id: int) -> Optional[Dict]:
        """
        Retrieve a classification record by its ID

        Args:
            record_id (int): ID of the classification record

        Returns:
            dict or None: Classification record data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM classifications WHERE id = ?', (record_id,))
        row = cursor.fetchone()

        if row:
            columns = [description[0] for description in cursor.description]
            result = dict(zip(columns, row))
            # Parse metadata JSON if it exists
            if result['metadata']:
                result['metadata'] = json.loads(result['metadata'])
            conn.close()
            return result

        conn.close()
        return None

    def get_classifications_by_category(self, category: str, limit: int = 100) -> List[Dict]:
        """
        Retrieve classifications by assigned category

        Args:
            category (str): Category to filter by
            limit (int): Maximum number of records to return

        Returns:
            list: List of classification records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM classifications
            WHERE assigned_category = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (category, limit))

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        results = []

        for row in rows:
            result = dict(zip(columns, row))
            # Parse metadata JSON if it exists
            if result['metadata']:
                result['metadata'] = json.loads(result['metadata'])
            results.append(result)

        conn.close()
        return results

    def get_recent_classifications(self, limit: int = 50) -> List[Dict]:
        """
        Retrieve the most recent classification records

        Args:
            limit (int): Maximum number of records to return

        Returns:
            list: List of classification records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM classifications
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        results = []

        for row in rows:
            result = dict(zip(columns, row))
            # Parse metadata JSON if it exists
            if result['metadata']:
                result['metadata'] = json.loads(result['metadata'])
            results.append(result)

        conn.close()
        return results

    def update_feedback(self, record_id: int, feedback_status: str):
        """
        Update the feedback status for a classification record

        Args:
            record_id (int): ID of the record to update
            feedback_status (str): New feedback status ('none', 'positive', 'negative')
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE classifications
            SET feedback_status = ?
            WHERE id = ?
        ''', (feedback_status, record_id))

        conn.commit()
        conn.close()

    def get_statistics(self) -> Dict:
        """
        Get statistics about the classification history

        Returns:
            dict: Statistics about the classification data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total classifications
        cursor.execute('SELECT COUNT(*) FROM classifications')
        total_classifications = cursor.fetchone()[0]

        # Classifications by category
        cursor.execute('''
            SELECT assigned_category, COUNT(*) as count
            FROM classifications
            GROUP BY assigned_category
            ORDER BY count DESC
        ''')
        category_counts = {row[0]: row[1] for row in cursor.fetchall()}

        # Recent classifications (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM classifications
            WHERE timestamp >= datetime('now', '-7 days')
        ''')
        recent_count = cursor.fetchone()[0]

        # Average confidence score
        cursor.execute('SELECT AVG(confidence_score) FROM classifications WHERE confidence_score IS NOT NULL')
        avg_confidence = cursor.fetchone()[0]

        # Feedback distribution
        cursor.execute('''
            SELECT feedback_status, COUNT(*) as count
            FROM classifications
            GROUP BY feedback_status
        ''')
        feedback_counts = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()

        return {
            'total_classifications': total_classifications,
            'category_distribution': category_counts,
            'recent_classifications': recent_count,
            'average_confidence': avg_confidence,
            'feedback_distribution': feedback_counts
        }

    def export_data(self, export_path: str):
        """
        Export all classification data to a JSON file

        Args:
            export_path (str): Path to export the data to
        """
        classifications = self.get_recent_classifications(limit=-1)  # Get all records

        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(classifications, f, indent=2, default=str)  # default=str handles datetime serialization


if __name__ == "__main__":
    # Example usage
    db = HistoryDatabase('./test_classification_history.db')

    print("Database module loaded successfully")
    print("Ready to track classification history")