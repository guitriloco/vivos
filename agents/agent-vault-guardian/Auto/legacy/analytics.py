"""
Classification History Tracker
Analytics module for analyzing classification data
"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
import os


class AnalyticsEngine:
    def __init__(self, history_database):
        """
        Initialize the analytics engine

        Args:
            history_database: Instance of HistoryDatabase
        """
        self.db = history_database

    def get_statistics(self) -> Dict:
        """
        Get comprehensive statistics about classifications

        Returns:
            dict: Comprehensive statistics
        """
        return self.db.get_statistics()

    def generate_accuracy_report(self) -> Dict:
        """
        Generate a report on classification accuracy based on feedback

        Returns:
            dict: Accuracy report
        """
        # Get feedback distribution from database statistics
        stats = self.db.get_statistics()
        total = stats['total_classifications']

        if total == 0:
            return {
                'accuracy_rate': 0,
                'total_classifications': 0,
                'positive_feedback': 0,
                'negative_feedback': 0,
                'no_feedback': 0
            }

        feedback_dist = stats.get('feedback_distribution', {})
        positive_feedback = feedback_dist.get('positive', 0)
        negative_feedback = feedback_dist.get('negative', 0)
        no_feedback = feedback_dist.get('none', 0)

        accuracy_rate = (positive_feedback / total * 100) if total > 0 else 0

        return {
            'accuracy_rate': round(accuracy_rate, 2),
            'total_classifications': total,
            'positive_feedback': positive_feedback,
            'negative_feedback': negative_feedback,
            'no_feedback': no_feedback
        }

    def get_category_performance(self) -> Dict:
        """
        Get performance metrics by category

        Returns:
            dict: Performance metrics by category
        """
        stats = self.db.get_statistics()
        category_dist = stats.get('category_distribution', {})

        # Get feedback by category (we'll need to query this separately)
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT assigned_category, feedback_status, COUNT(*) as count
            FROM classifications
            GROUP BY assigned_category, feedback_status
        ''')

        feedback_by_category = {}
        for row in cursor.fetchall():
            category, feedback, count = row
            if category not in feedback_by_category:
                feedback_by_category[category] = {}
            feedback_by_category[category][feedback] = count

        conn.close()

        # Calculate performance for each category
        performance = {}
        for category, total_count in category_dist.items():
            category_feedback = feedback_by_category.get(category, {})
            positive = category_feedback.get('positive', 0)
            negative = category_feedback.get('negative', 0)

            accuracy = (positive / (positive + negative) * 100) if (positive + negative) > 0 else 0

            performance[category] = {
                'total_classifications': total_count,
                'positive_feedback': positive,
                'negative_feedback': negative,
                'accuracy_rate': round(accuracy, 2)
            }

        return performance

    def get_trend_analysis(self, days: int = 30) -> Dict:
        """
        Get trend analysis for the specified number of days

        Args:
            days (int): Number of days to analyze

        Returns:
            dict: Trend analysis data
        """
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        # Get daily counts for the specified period
        cursor.execute('''
            SELECT DATE(timestamp) as day, COUNT(*) as count
            FROM classifications
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY DATE(timestamp)
            ORDER BY day
        '''.format(days))

        daily_counts = cursor.fetchall()

        # Get daily feedback counts
        cursor.execute('''
            SELECT DATE(timestamp) as day, feedback_status, COUNT(*) as count
            FROM classifications
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY DATE(timestamp), feedback_status
            ORDER BY day
        '''.format(days))

        daily_feedback = {}
        for row in cursor.fetchall():
            day, feedback, count = row
            if day not in daily_feedback:
                daily_feedback[day] = {}
            daily_feedback[day][feedback] = count

        conn.close()

        return {
            'daily_classifications': {day: count for day, count in daily_counts},
            'daily_feedback': daily_feedback,
            'period_days': days
        }

    def visualize_classification_trends(self, output_path: str = None) -> None:
        """
        Create visualizations for classification trends

        Args:
            output_path (str, optional): Path to save the visualization
        """
        import matplotlib.dates as mdates
        from datetime import datetime

        # Get trend data
        trend_data = self.get_trend_analysis(days=30)
        daily_counts = trend_data['daily_classifications']

        # Convert dates to datetime objects for plotting
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in daily_counts.keys()]
        counts = list(daily_counts.values())

        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(dates, counts, marker='o', linestyle='-', color='blue')
        plt.title('Daily Classification Counts (Last 30 Days)')
        plt.xlabel('Date')
        plt.ylabel('Number of Classifications')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.xticks(rotation=45)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            print(f"Trend visualization saved to {output_path}")
        else:
            plt.show()

    def visualize_category_distribution(self, output_path: str = None) -> None:
        """
        Create visualizations for category distribution

        Args:
            output_path (str, optional): Path to save the visualization
        """
        stats = self.db.get_statistics()
        category_dist = stats.get('category_distribution', {})

        if not category_dist:
            print("No category data available for visualization")
            return

        categories = list(category_dist.keys())
        counts = list(category_dist.values())

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.bar(categories, counts, color='skyblue')
        plt.title('Distribution of Classifications by Category')
        plt.xlabel('Category')
        plt.ylabel('Number of Classifications')
        plt.xticks(rotation=45)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            print(f"Category distribution visualization saved to {output_path}")
        else:
            plt.show()

    def generate_comprehensive_report(self, output_path: str = None) -> Dict:
        """
        Generate a comprehensive analytics report

        Args:
            output_path (str, optional): Path to save the report as JSON

        Returns:
            dict: Comprehensive report data
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary_statistics': self.get_statistics(),
            'accuracy_report': self.generate_accuracy_report(),
            'category_performance': self.get_category_performance(),
            'trend_analysis': self.get_trend_analysis(days=30)
        }

        if output_path:
            import json
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"Comprehensive report saved to {output_path}")

        return report


if __name__ == "__main__":
    # This module requires a HistoryDatabase instance to work
    print("Analytics engine module loaded successfully")
    print("Requires a HistoryDatabase instance for full functionality")