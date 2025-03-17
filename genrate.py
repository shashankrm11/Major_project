import json
import pefile
import os
import mimetypes
import hashlib
from PyPDF2 import PdfReader
from PIL import Image

def extract_pe_features(file_path):
    """Extract features specific to PE files."""
    try:
        pe = pefile.PE(file_path)
        features = {
            "ImageBase": pe.OPTIONAL_HEADER.ImageBase,
            "VersionInformationSize": getattr(pe, "VS_FIXEDFILEINFO", {}).get("StructVersion", 0),
            "SectionsMaxEntropy": max(section.get_entropy() for section in pe.sections) if pe.sections else 0,
            "MajorOperatingSystemVersion": pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
            "ResourcesMinSize": min(
                [r['Data'].Structure.Size for r in getattr(pe, "DIRECTORY_ENTRY_RESOURCE", {}).get("entries", [])],
                default=0),
            "SizeOfStackReserve": pe.OPTIONAL_HEADER.SizeOfStackReserve,
            "Characteristics": pe.FILE_HEADER.Characteristics,
            "SizeOfInitializedData": pe.OPTIONAL_HEADER.SizeOfInitializedData,
            "MajorSubsystemVersion": pe.OPTIONAL_HEADER.MajorSubsystemVersion,
            "ResourcesNb": len(getattr(pe, "DIRECTORY_ENTRY_RESOURCE", {}).get("entries", [])),
            "Subsystem": pe.OPTIONAL_HEADER.Subsystem,
            "ResourcesMinEntropy": min(
                [r["Data"].get_entropy() for r in getattr(pe, "DIRECTORY_ENTRY_RESOURCE", {}).get("entries", [])], default=0),
            "BaseOfData": getattr(pe.OPTIONAL_HEADER, "BaseOfData", None),
            "SizeOfImage": pe.OPTIONAL_HEADER.SizeOfImage
        }
        return features
    except Exception as e:
        print(f"Error processing PE file: {file_path}, Error: {e}")
        return {}

def extract_pdf_features(file_path):
    """Extract features specific to PDF files."""
    try:
        reader = PdfReader(file_path)
        features = {
            "NumberOfPages": len(reader.pages),
            "Title": reader.metadata.get("/Title", "Unknown"),
            "Author": reader.metadata.get("/Author", "Unknown"),
            "Producer": reader.metadata.get("/Producer", "Unknown"),
        }
        return features
    except Exception as e:
        print(f"Error processing PDF file: {file_path}, Error: {e}")
        return {}

def extract_image_features(file_path):
    """Extract features specific to image files."""
    try:
        with Image.open(file_path) as img:
            features = {
                "Format": img.format,
                "Mode": img.mode,
                "Width": img.width,
                "Height": img.height,
            }
        return features
    except Exception as e:
        print(f"Error processing image file: {file_path}, Error: {e}")
        return {}

def calculate_hashes(file_path):
    """Calculate MD5, SHA-1, and SHA-256 hashes for any file."""
    hashes = {}
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            hashes["MD5"] = hashlib.md5(data).hexdigest()
            hashes["SHA-1"] = hashlib.sha1(data).hexdigest()
            hashes["SHA-256"] = hashlib.sha256(data).hexdigest()
    except Exception as e:
        print(f"Error calculating hashes for file: {file_path}, Error: {e}")
    return hashes

def is_pe_file(file_path):
    """Determine if the file is a Portable Executable (PE) file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type in ["application/x-dosexec"]

def is_pdf_file(file_path):
    """Determine if the file is a PDF."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type == "application/pdf"

def is_image_file(file_path):
    """Determine if the file is an image."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("image")

def process_file(file_path):
    """Determine file type and extract relevant features."""
    if is_pe_file(file_path):
        print("Processing as a PE file...")
        features = extract_pe_features(file_path)
    elif is_pdf_file(file_path):
        print("Processing as a PDF file...")
        features = extract_pdf_features(file_path)
    elif is_image_file(file_path):
        print("Processing as an image file...")
        features = extract_image_features(file_path)
    else:
        print("Processing as a generic file...")
        features = calculate_hashes(file_path)
    return features

def generate_json(file_path, output_path):
    """Generate JSON file for extracted features."""
    features = process_file(file_path)
    if features:
        with open(output_path, "w") as json_file:
            json.dump(features, json_file, indent=4)
        print(f"JSON file generated: {output_path}")
    else:
        print("No features extracted. JSON file not created.")

if __name__ == "__main__":
    input_file = input("Enter the path of the file to analyze: ").strip()
    if os.path.exists(input_file):
        output_file = os.path.splitext(input_file)[0] + "_features.json"
        generate_json(input_file, output_file)
    else:
        print("File does not exist. Please provide a valid file path.")