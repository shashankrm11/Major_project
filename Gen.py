import json
import random
import os

def generate_feature_data(file_type):
    """
    Generate synthetic feature data based on the file type.

    Args:
        file_type (str): Type of the file (e.g., 'exe', 'pdf', 'txt').

    Returns:
        dict: Dictionary with feature data.
    """
    if file_type == 'exe':
        return {
            "ImageBase": random.randint(2000000000, 4000000000),
            "VersionInformationSize": random.randint(500, 5000),
            "SectionsMaxEntropy": round(random.uniform(5.0, 8.0), 2),
            "MajorOperatingSystemVersion": random.randint(6, 10),
            "ResourcesMinSize": random.randint(100, 1000),
            "SizeOfStackReserve": random.randint(2000, 10000),
            "Characteristics": random.randint(1000, 5000),
            "SizeOfInitializedData": random.randint(1000, 5000),
            "MajorSubsystemVersion": random.randint(4, 6),
            "ResourcesNb": random.randint(1, 5),
            "Subsystem": random.randint(1, 3),
            "ResourcesMinEntropy": round(random.uniform(3.0, 7.0), 2),
            "BaseOfData": random.randint(100, 1000),
            "SizeOfImage": random.randint(100000, 2000000)
        }
    elif file_type == 'pdf':
        return {
            "ImageBase": 0,
            "VersionInformationSize": random.randint(1000, 3000),
            "SectionsMaxEntropy": round(random.uniform(4.0, 7.0), 2),
            "MajorOperatingSystemVersion": random.randint(6, 9),
            "ResourcesMinSize": random.randint(500, 1500),
            "SizeOfStackReserve": random.randint(4000, 10000),
            "Characteristics": random.randint(100, 500),
            "SizeOfInitializedData": random.randint(500, 2000),
            "MajorSubsystemVersion": random.randint(3, 5),
            "ResourcesNb": random.randint(1, 3),
            "Subsystem": random.randint(1, 2),
            "ResourcesMinEntropy": round(random.uniform(2.0, 6.0), 2),
            "BaseOfData": random.randint(50, 500),
            "SizeOfImage": random.randint(50000, 1000000)
        }
    elif file_type == 'txt':
        return {
            "ImageBase": 0,
            "VersionInformationSize": 0,
            "SectionsMaxEntropy": round(random.uniform(2.0, 4.0), 2),
            "MajorOperatingSystemVersion": random.randint(6, 10),
            "ResourcesMinSize": 0,
            "SizeOfStackReserve": random.randint(1000, 5000),
            "Characteristics": random.randint(500, 2000),
            "SizeOfInitializedData": random.randint(100, 500),
            "MajorSubsystemVersion": random.randint(3, 5),
            "ResourcesNb": random.randint(0, 2),
            "Subsystem": random.randint(1, 3),
            "ResourcesMinEntropy": round(random.uniform(1.0, 3.0), 2),
            "BaseOfData": 0,
            "SizeOfImage": random.randint(10000, 100000)
        }
    else:
        raise ValueError("Unsupported file type!")

def create_test_files(output_dir, file_types, num_files_per_type):
    """
    Generate and save test files as JSON.

    Args:
        output_dir (str): Directory to save the JSON files.
        file_types (list): List of file types to generate.
        num_files_per_type (int): Number of files to generate for each type.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_type in file_types:
        for i in range(num_files_per_type):
            data = generate_feature_data(file_type)
            file_name = f"{file_type}_test_{i+1}.json"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Generated: {file_path}")

# Configuration
output_directory = "test_files"  # Output directory for JSON files
file_types_to_generate = ['exe', 'pdf', 'txt']  # Supported file types
files_per_type = 5  # Number of files per type

# Generate test files
create_test_files(output_directory, file_types_to_generate, files_per_type)
