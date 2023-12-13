import os


def extractJsonFiles(directory_path):
    return [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(".json")]
