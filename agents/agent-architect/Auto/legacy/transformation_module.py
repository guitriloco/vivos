def transform(record):
    """
    Sample transformation function that demonstrates data cleaning and formatting.
    This function can be replaced with any custom transformation logic.
    """
    # Example transformations:

    # 1. Clean data - remove empty fields
    cleaned_record = {}
    for key, value in record.items():
        if value is not None and value != "":
            # Convert string numbers to integers/floats where appropriate
            if isinstance(value, str):
                if value.isdigit():
                    cleaned_record[key] = int(value)
                elif is_float_string(value):
                    cleaned_record[key] = float(value)
                else:
                    cleaned_record[key] = value.strip().lower()
            else:
                cleaned_record[key] = value

    # 2. Format data - standardize field names and structures
    formatted_record = standardize_fields(cleaned_record)

    # 3. Validate data integrity
    if not validate_record(formatted_record):
        # Return None or an error marker to skip invalid records
        return None

    # 4. Add processing metadata
    formatted_record['_processed_at'] = __import__('time').time()
    formatted_record['_transform_version'] = '1.0'

    return formatted_record

def is_float_string(s):
    """Check if a string represents a float number"""
    try:
        float(s)
        return True
    except ValueError:
        return False

def standardize_fields(record):
    """Standardize field names and formats"""
    # Example standardization
    standardized = {}
    for key, value in record.items():
        # Convert camelCase or PascalCase to snake_case
        snake_key = camel_to_snake(key)
        standardized[snake_key] = value
    return standardized

def camel_to_snake(name):
    """Convert camelCase or PascalCase to snake_case"""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def validate_record(record):
    """Basic validation of record integrity"""
    # Example validation rules
    required_fields = ['id', 'name']  # Adjust based on your data

    # Check if required fields exist
    for field in required_fields:
        if field not in record:
            return False

    # Additional validation can be added here
    # For example, check data types, value ranges, etc.

    return True

# Additional transformation examples:

def refine_numeric_values(record):
    """Refine numeric values in the record"""
    for key, value in record.items():
        if isinstance(value, (int, float)):
            # Example: round floats to 2 decimal places
            if isinstance(value, float):
                record[key] = round(value, 2)
    return record

def format_dates(record):
    """Format date fields in the record"""
    import datetime

    for key, value in record.items():
        if isinstance(value, str):
            # Try to parse common date formats
            for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d.%m.%Y'):
                try:
                    parsed_date = datetime.datetime.strptime(value, fmt)
                    record[key] = parsed_date.strftime('%Y-%m-%d')
                    break
                except ValueError:
                    continue
    return record

# The main transform function can incorporate multiple refinement steps
def enhanced_transform(record):
    """
    Enhanced transformation with multiple refinement steps
    """
    if record is None:
        return None

    # Apply basic transformations
    result = transform(record)

    if result is not None:
        # Apply additional refinement steps
        result = refine_numeric_values(result)
        result = format_dates(result)

    return result