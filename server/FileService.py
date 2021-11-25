import os
import time
import logging


def get_path(filename: str) -> str:
    path = os.path.join(os.getcwd(), filename)
    if not is_valid_path(path):
        raise ValueError(f"Invalid filename {path}")

    return path


def is_valid_path(path: str) -> bool:
    forbidden = """# %&{}\<>*?/$!'":@+`|="""
    return bool(next((i for i in path if i not in forbidden), None))


def is_allowed_path(path) -> bool:
    return os.getcwd() in os.path.abspath(path)


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if not is_valid_path(path):
        raise ValueError(f"Invalid path {path}")

    if not is_allowed_path(path):
        raise ValueError(f"Restricted path {path}")

    if not os.path.exists(path):
        if autocreate:
            os.makedirs(path)
        else:
            raise RuntimeError(f"Directory does not exist and autocreate is False.")

    os.chdir(path)
    logging.debug(f"Set working directory to {os.getcwd()}")


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    folder = os.getcwd()
    files = list()
    for path in os.listdir(folder):
        if os.path.isfile(path):
            file_stat = {
                'name': os.path.basename(path),
                'create_date': time.ctime(os.path.getctime(path)),
                'edit_date': time.ctime(os.path.getmtime(path)),
                'size': os.path.getsize(path)
            }
            files.append(file_stat)
    logging.debug(f"Get files from folder {folder}")
    return files


def get_file_data(filename: str) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    path = get_path(filename)
    if not is_valid_path(path):
        raise ValueError(f"Invalid filename {path}")

    if not is_allowed_path(path):
        raise ValueError(f"Restricted path {path}")

    if not os.path.isfile(path) or not os.path.exists(path):
        raise RuntimeError(f"RuntimeError: if file does not exist.")

    with open(path, 'r') as file:
        logging.debug(f"Get files data {path}")
        return {
            'name': os.path.basename(path),
            'create_date': time.ctime(os.path.getctime(path)),
            'edit_date': time.ctime(os.path.getmtime(path)),
            'content': file.read(),
            'size': os.path.getsize(path)
        }


def create_file(filename: str, content: str = None) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """

    path = get_path(filename)
    if not is_valid_path(path):
        raise RuntimeError(f"RuntimeError: if file does not exist.")

    if not is_allowed_path(path):
        raise ValueError(f"Restricted path {path}")

    if not os.path.exists(filename):
        logging.warning(f"File already exist {path}")

    with open(filename, 'w') as file:
        file.write(content)

    return {
        'name': os.path.basename(path),
        'create_date': time.ctime(os.path.getatime(path)),
        'content': content,
        'size': os.path.getsize(path)
    }


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    path = get_path(filename)
    if not is_valid_path(path):
        raise ValueError(f"Invalid filename {path}")

    if not is_allowed_path(path):
        raise ValueError(f"Restricted path {path}")

    if not os.path.isfile(path) or not os.path.exists(path):
        raise RuntimeError(f"RuntimeError: if file does not exist.")

    path = get_path(filename)
    os.remove(os.path.join(path))
    logging.debug(f"File removed {path}")
