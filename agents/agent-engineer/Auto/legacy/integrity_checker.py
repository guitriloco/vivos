"""
Document Backup Manager
Integrity checking module
"""

import hashlib
import os
from typing import Dict, List


class IntegrityChecker:
    """
    Class to handle file integrity checking for document backups
    """

    def __init__(self, algorithm='sha256'):
        """
        Initialize the integrity checker

        Args:
            algorithm (str): Hash algorithm to use ('sha256', 'md5', 'sha1', etc.)
        """
        self.algorithm = algorithm

    def calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate the hash of a file

        Args:
            file_path (str): Path to the file

        Returns:
            str: File hash
        """
        hash_func = hashlib.new(self.algorithm)

        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()

    def verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """
        Verify if a file's hash matches the expected hash

        Args:
            file_path (str): Path to the file to check
            expected_hash (str): Expected hash value

        Returns:
            bool: True if hashes match
        """
        current_hash = self.calculate_file_hash(file_path)
        return current_hash == expected_hash

    def generate_integrity_report(self, file_paths: List[str]) -> Dict:
        """
        Generate an integrity report for multiple files

        Args:
            file_paths (List[str]): List of file paths to check

        Returns:
            Dict: Integrity report
        """
        report = {
            'checked_files': 0,
            'valid_files': 0,
            'invalid_files': 0,
            'errors': [],
            'file_results': {}
        }

        for file_path in file_paths:
            try:
                if not os.path.exists(file_path):
                    report['errors'].append(f"File does not exist: {file_path}")
                    continue

                file_hash = self.calculate_file_hash(file_path)

                report['file_results'][file_path] = {
                    'hash': file_hash,
                    'file_size': os.path.getsize(file_path),
                    'valid': True
                }

                report['checked_files'] += 1
                report['valid_files'] += 1

            except Exception as e:
                report['file_results'][file_path] = {
                    'error': str(e),
                    'valid': False
                }
                report['errors'].append(f"Error checking {file_path}: {str(e)}")
                report['checked_files'] += 1
                report['invalid_files'] += 1

        return report

    def create_checksum_file(self, file_paths: List[str], checksum_file_path: str):
        """
        Create a checksum file containing hashes for the provided files

        Args:
            file_paths (List[str]): List of file paths to create checksums for
            checksum_file_path (str): Path to save the checksum file
        """
        checksums = {}

        for file_path in file_paths:
            if os.path.exists(file_path):
                checksums[file_path] = self.calculate_file_hash(file_path)
            else:
                checksums[file_path] = "FILE_NOT_FOUND"

        # Write checksums to file
        with open(checksum_file_path, 'w') as f:
            for file_path, checksum in checksums.items():
                f.write(f"{checksum}  {file_path}\n")

    def verify_from_checksum_file(self, checksum_file_path: str) -> Dict:
        """
        Verify file integrity based on a checksum file

        Args:
            checksum_file_path (str): Path to the checksum file

        Returns:
            Dict: Verification results
        """
        results = {
            'verified_files': 0,
            'matching_files': 0,
            'mismatched_files': 0,
            'missing_files': 0,
            'errors': [],
            'file_results': {}
        }

        if not os.path.exists(checksum_file_path):
            results['errors'].append(f"Checksum file does not exist: {checksum_file_path}")
            return results

        with open(checksum_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split('  ', 1)
                if len(parts) != 2:
                    continue

                expected_hash, file_path = parts

                if not os.path.exists(file_path):
                    results['file_results'][file_path] = {
                        'expected_hash': expected_hash,
                        'actual_hash': None,
                        'valid': False,
                        'reason': 'File missing'
                    }
                    results['missing_files'] += 1
                    continue

                actual_hash = self.calculate_file_hash(file_path)
                is_valid = actual_hash == expected_hash

                results['file_results'][file_path] = {
                    'expected_hash': expected_hash,
                    'actual_hash': actual_hash,
                    'valid': is_valid
                }

                results['verified_files'] += 1
                if is_valid:
                    results['matching_files'] += 1
                else:
                    results['mismatched_files'] += 1

        return results


def quick_verify_file(file_path: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
    """
    Quick function to verify a single file against an expected hash

    Args:
        file_path (str): Path to the file to check
        expected_hash (str): Expected hash value
        algorithm (str): Hash algorithm to use

    Returns:
        bool: True if file integrity is verified
    """
    checker = IntegrityChecker(algorithm)
    return checker.verify_file_integrity(file_path, expected_hash)


if __name__ == "__main__":
    # Example usage
    checker = IntegrityChecker()
    print("Integrity checker initialized")
    print("Ready to verify document backup integrity")