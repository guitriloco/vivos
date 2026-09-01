"""
Document Backup Manager
Backup management module
"""

import os
import shutil
import hashlib
import json
from datetime import datetime
from pathlib import Path


class IntegrityChecker:
    """
    Class to handle file integrity checking
    """
    @staticmethod
    def calculate_file_hash(file_path, algorithm='sha256'):
        """
        Calculate the hash of a file

        Args:
            file_path (str): Path to the file
            algorithm (str): Hash algorithm to use

        Returns:
            str: File hash
        """
        hash_func = hashlib.new(algorithm)

        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()


class BackupManager:
    def __init__(self, backup_location):
        """
        Initialize the backup manager

        Args:
            backup_location (str): Directory where backups will be stored
        """
        self.backup_location = backup_location
        self.integrity_checker = IntegrityChecker()

        # Create backup directory if it doesn't exist
        os.makedirs(backup_location, exist_ok=True)

        # Create logs directory
        self.logs_dir = os.path.join(backup_location, 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)

        # Create metadata directory
        self.metadata_dir = os.path.join(backup_location, 'metadata')
        os.makedirs(self.metadata_dir, exist_ok=True)

        print(f"Backup manager initialized at: {backup_location}")

    def create_backup(self, source_path, backup_name=None, metadata=None):
        """
        Create a backup of a document

        Args:
            source_path (str): Path to the document to backup
            backup_name (str, optional): Custom name for the backup
            metadata (dict, optional): Additional metadata about the backup

        Returns:
            dict: Backup information
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file does not exist: {source_path}")

        # Generate backup name if not provided
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.basename(source_path)
            backup_name = f"{timestamp}_{original_name}"

        # Create backup path
        backup_path = os.path.join(self.backup_location, backup_name)

        # Copy the file to backup location
        shutil.copy2(source_path, backup_path)

        # Calculate hash for integrity check
        file_hash = self.integrity_checker.calculate_file_hash(source_path)

        # Create metadata
        backup_metadata = {
            'original_path': source_path,
            'backup_path': backup_path,
            'backup_timestamp': datetime.now().isoformat(),
            'file_size': os.path.getsize(source_path),
            'file_hash': file_hash,
            'custom_metadata': metadata or {}
        }

        # Save metadata to a JSON file
        metadata_path = os.path.join(self.metadata_dir, f"{backup_name}.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(backup_metadata, f, indent=2)

        # Log the backup operation
        self._log_operation('create_backup', {
            'source_path': source_path,
            'backup_path': backup_path,
            'file_hash': file_hash
        })

        print(f"Backup created: {backup_path}")

        return {
            'backup_path': backup_path,
            'file_hash': file_hash,
            'metadata_path': metadata_path,
            'timestamp': backup_metadata['backup_timestamp']
        }

    def restore_backup(self, backup_path, restore_to_path):
        """
        Restore a document from backup

        Args:
            backup_path (str): Path to the backup file
            restore_to_path (str): Path where to restore the file

        Returns:
            bool: True if restoration was successful
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file does not exist: {backup_path}")

        # Create directory for restore path if needed
        restore_dir = os.path.dirname(restore_to_path)
        os.makedirs(restore_dir, exist_ok=True)

        # Copy the backup to the restore location
        shutil.copy2(backup_path, restore_to_path)

        # Verify the restored file integrity
        metadata_path = os.path.join(self.metadata_dir, f"{os.path.basename(backup_path)}.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Verify file hash
            restored_hash = self.integrity_checker.calculate_file_hash(restore_to_path)
            original_hash = metadata['file_hash']

            if restored_hash != original_hash:
                raise ValueError(f"Integrity check failed: hashes do not match")

        # Log the restore operation
        self._log_operation('restore_backup', {
            'backup_path': backup_path,
            'restore_to_path': restore_to_path
        })

        print(f"Backup restored: {restore_to_path}")
        return True

    def get_backup_info(self, backup_name):
        """
        Get information about a specific backup

        Args:
            backup_name (str): Name of the backup

        Returns:
            dict: Backup information
        """
        metadata_path = os.path.join(self.metadata_dir, f"{backup_name}.json")

        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata not found for backup: {backup_name}")

        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_backups(self):
        """
        List all available backups

        Returns:
            list: List of backup names
        """
        backups = []
        for filename in os.listdir(self.metadata_dir):
            if filename.endswith('.json'):
                backups.append(filename[:-5])  # Remove .json extension

        return sorted(backups, reverse=True)  # Most recent first

    def delete_backup(self, backup_name):
        """
        Delete a backup and its metadata

        Args:
            backup_name (str): Name of the backup to delete

        Returns:
            bool: True if deletion was successful
        """
        backup_path = os.path.join(self.backup_location, backup_name)
        metadata_path = os.path.join(self.metadata_dir, f"{backup_name}.json")

        # Delete the backup file
        if os.path.exists(backup_path):
            os.remove(backup_path)

        # Delete the metadata file
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

        # Log the deletion operation
        self._log_operation('delete_backup', {
            'backup_name': backup_name
        })

        print(f"Backup deleted: {backup_name}")
        return True

    def verify_backup_integrity(self, backup_name):
        """
        Verify the integrity of a backup

        Args:
            backup_name (str): Name of the backup to verify

        Returns:
            dict: Verification results
        """
        backup_path = os.path.join(self.backup_location, backup_name)
        metadata_path = os.path.join(self.metadata_dir, f"{backup_name}.json")

        if not os.path.exists(backup_path):
            return {'valid': False, 'error': f'Backup file not found: {backup_path}'}

        if not os.path.exists(metadata_path):
            return {'valid': False, 'error': f'Metadata not found: {metadata_path}'}

        # Load metadata
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Calculate current hash
        current_hash = self.integrity_checker.calculate_file_hash(backup_path)
        original_hash = metadata['file_hash']

        # Compare hashes
        is_valid = current_hash == original_hash

        return {
            'valid': is_valid,
            'current_hash': current_hash,
            'original_hash': original_hash,
            'file_size_match': os.path.getsize(backup_path) == metadata['file_size']
        }

    def _log_operation(self, operation, details):
        """
        Log backup operations

        Args:
            operation (str): Type of operation
            details (dict): Details about the operation
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details
        }

        log_file = os.path.join(self.logs_dir, f"{datetime.now().strftime('%Y-%m-%d')}_operations.log")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')


class BackupPolicy:
    """
    Class to manage backup policies
    """
    def __init__(self, retention_days=30, max_backups_per_file=5):
        """
        Initialize backup policy

        Args:
            retention_days (int): Number of days to retain backups
            max_backups_per_file (int): Maximum number of backups per file
        """
        self.retention_days = retention_days
        self.max_backups_per_file = max_backups_per_file

    def should_create_backup(self, file_path, backup_manager):
        """
        Determine if a backup should be created for a file

        Args:
            file_path (str): Path to the file
            backup_manager (BackupManager): Backup manager instance

        Returns:
            bool: True if backup should be created
        """
        # For now, always create backup
        # In a more sophisticated implementation, this would check
        # factors like file age, last backup time, etc.
        return True

    def apply_retention_policy(self, backup_manager):
        """
        Apply retention policy to clean up old backups

        Args:
            backup_manager (BackupManager): Backup manager instance
        """
        import time

        current_time = time.time()
        retention_period = self.retention_days * 24 * 60 * 60  # Convert to seconds

        for backup_name in backup_manager.list_backups():
            backup_path = os.path.join(backup_manager.backup_location, backup_name)

            # Check if backup is older than retention period
            if os.path.exists(backup_path):
                file_age = current_time - os.path.getmtime(backup_path)

                if file_age > retention_period:
                    backup_manager.delete_backup(backup_name)


if __name__ == "__main__":
    # Example usage
    backup_mgr = BackupManager("./backups")
    print("Backup manager initialized")
    print("Ready to manage document backups")