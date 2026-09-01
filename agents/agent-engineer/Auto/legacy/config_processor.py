"""
Configurable Document Processor
Configuration and processing logic module
"""

import os
import json
import shutil
from pathlib import Path
import yaml


class ConfigurableProcessor:
    def __init__(self, config):
        """
        Initialize the configurable document processor

        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        self.input_dir = config.get('directories', {}).get('documents_input', './input')
        self.output_dir = config.get('directories', {}).get('documents_output', './output')
        self.profiles_dir = os.path.join(os.path.dirname(__file__), 'profiles')
        self.processors_dir = os.path.join(os.path.dirname(__file__), 'processors')

        # Create necessary directories
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(self.processors_dir, exist_ok=True)

        # Load or create default processing profile
        self.default_profile = self._load_default_profile()

    def _load_default_profile(self):
        """
        Load or create a default processing profile
        """
        profile_path = os.path.join(self.profiles_dir, 'default.json')

        default_profile = {
            "name": "default",
            "description": "Default processing profile",
            "actions": [
                {
                    "type": "classify",
                    "destination": "{category}",
                    "engine": "local_ai"
                },
                {
                    "type": "backup",
                    "destination": "../backups/{original_filename}",
                    "condition": "always"
                }
            ]
        }

        if not os.path.exists(profile_path):
            with open(profile_path, 'w') as f:
                json.dump(default_profile, f, indent=2)

        return default_profile

    def load_profile(self, profile_name):
        """
        Load a specific processing profile

        Args:
            profile_name (str): Name of the profile to load

        Returns:
            dict: Profile configuration
        """
        profile_path = os.path.join(self.profiles_dir, f'{profile_name}.json')

        if not os.path.exists(profile_path):
            raise FileNotFoundError(f"Profile {profile_name} not found at {profile_path}")

        with open(profile_path, 'r') as f:
            return json.load(f)

    def save_profile(self, profile_name, profile_data):
        """
        Save a processing profile

        Args:
            profile_name (str): Name of the profile
            profile_data (dict): Profile configuration data
        """
        profile_path = os.path.join(self.profiles_dir, f'{profile_name}.json')

        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=2)

    def get_available_profiles(self):
        """
        Get list of available processing profiles

        Returns:
            list: List of profile names
        """
        profiles = []
        for file in os.listdir(self.profiles_dir):
            if file.endswith('.json'):
                profiles.append(file[:-5])  # Remove .json extension
        return profiles

    def process_documents(self, input_directory=None, output_directory=None, profile_name='default'):
        """
        Process documents according to the specified profile

        Args:
            input_directory (str, optional): Directory containing documents to process
            output_directory (str, optional): Directory to output processed documents
            profile_name (str): Name of the profile to use for processing

        Returns:
            dict: Processing results
        """
        input_dir = input_directory or self.input_dir
        output_dir = output_directory or self.output_dir

        # Load the specified profile
        try:
            profile = self.load_profile(profile_name)
        except FileNotFoundError:
            print(f"Profile {profile_name} not found. Using default profile.")
            profile = self.default_profile

        # Get all documents in the input directory
        documents = self._get_documents(input_dir)

        results = {
            'processed': [],
            'failed': [],
            'skipped': [],
            'profile_used': profile_name
        }

        print(f"Processing {len(documents)} documents using profile '{profile_name}'...")

        for doc_path in documents:
            try:
                # Apply each action in the profile
                doc_result = self._apply_profile_actions(doc_path, profile, output_dir)

                if doc_result['success']:
                    results['processed'].append({
                        'document': doc_path,
                        'actions': doc_result['actions'],
                        'destination': doc_result['destination']
                    })
                    print(f"Processed: {os.path.basename(doc_path)}")
                else:
                    results['failed'].append({
                        'document': doc_path,
                        'error': doc_result['error']
                    })
                    print(f"Failed: {os.path.basename(doc_path)} - {doc_result['error']}")

            except Exception as e:
                results['failed'].append({
                    'document': doc_path,
                    'error': str(e)
                })
                print(f"Error processing {os.path.basename(doc_path)}: {str(e)}")

        print(f"\nProcessing complete!")
        print(f"- Successfully processed: {len(results['processed'])}")
        print(f"- Failed: {len(results['failed'])}")

        return results

    def _get_documents(self, directory):
        """
        Get list of documents in a directory

        Args:
            directory (str): Directory to scan

        Returns:
            list: List of document file paths
        """
        documents = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.pdf', '.doc', '.docx', '.txt', '.rtf')):
                    documents.append(os.path.join(root, file))
        return documents

    def _apply_profile_actions(self, document_path, profile, output_base_dir):
        """
        Apply the actions defined in a profile to a document

        Args:
            document_path (str): Path to the document to process
            profile (dict): Profile containing actions to apply
            output_base_dir (str): Base directory for output

        Returns:
            dict: Result of the processing
        """
        result = {
            'success': True,
            'actions': [],
            'destination': None,
            'error': None
        }

        # Process each action in the profile
        for action in profile.get('actions', []):
            action_type = action.get('type')

            if action_type == 'classify':
                # For now, we'll use a simple heuristic for classification
                # In a full implementation, this would connect to an AI classifier
                category = self._classify_document(document_path)

                # Determine destination based on action configuration
                destination_template = action.get('destination', '{category}')
                destination = destination_template.format(category=category)

                # Create destination directory and move file
                final_destination = os.path.join(output_base_dir, destination)
                os.makedirs(final_destination, exist_ok=True)

                dest_file_path = os.path.join(final_destination, os.path.basename(document_path))

                # Copy the file to the destination
                shutil.copy2(document_path, dest_file_path)

                result['destination'] = final_destination
                result['actions'].append({
                    'type': 'classify',
                    'category': category,
                    'destination': final_destination
                })

            elif action_type == 'backup':
                # Create backup of the original file
                backup_dest = action.get('destination', '../backups/{original_filename}')
                backup_path = backup_dest.format(original_filename=os.path.basename(document_path))

                # Ensure backup directory exists
                backup_dir = os.path.dirname(backup_path)
                if not os.path.isabs(backup_path):
                    backup_path = os.path.join(output_base_dir, backup_path)
                    backup_dir = os.path.dirname(backup_path)

                os.makedirs(backup_dir, exist_ok=True)

                # Copy the file to backup location
                shutil.copy2(document_path, backup_path)

                result['actions'].append({
                    'type': 'backup',
                    'location': backup_path
                })

            # Additional action types can be added here

        return result

    def _classify_document(self, document_path):
        """
        Simple heuristic-based document classification
        In a full implementation, this would connect to an AI classifier

        Args:
            document_path (str): Path to the document to classify

        Returns:
            str: Classification category
        """
        filename = os.path.basename(document_path).lower()

        # Simple heuristics based on filename
        if any(keyword in filename for keyword in ['finance', 'bank', 'money', 'payment', 'paypal']):
            return 'Finance'
        elif any(keyword in filename for keyword in ['market', 'blog', 'advertising', 'marketing']):
            return 'Marketing'
        elif any(keyword in filename for keyword in ['tech', 'software', 'code', 'computer']):
            return 'Technology'
        elif any(keyword in filename for keyword in ['legal', 'contract', 'agreement', 'law']):
            return 'Legal'
        elif any(keyword in filename for keyword in ['medical', 'health', 'patient', 'doctor']):
            return 'Medical'
        elif any(keyword in filename for keyword in ['education', 'school', 'student', 'course']):
            return 'Education'
        elif any(keyword in filename for keyword in ['business', 'company', 'corporate', 'enterprise']):
            return 'Business'
        elif any(keyword in filename for keyword in ['personal', 'private', 'home']):
            return 'Personal'
        else:
            return 'Other'


if __name__ == "__main__":
    # Example usage
    config = {
        "directories": {
            "documents_input": "./test_input",
            "documents_output": "./test_output"
        }
    }

    processor = ConfigurableProcessor(config)

    print("ConfigurableProcessor initialized")
    print(f"Input directory: {processor.input_dir}")
    print(f"Output directory: {processor.output_dir}")
    print(f"Available profiles: {processor.get_available_profiles()}")