import pytest
import os


@pytest.fixture(scope='function')
def set_default_folder():
    old_folder = os.getcwd()
    os.chdir('.\\data')
    yield
    os.chdir(old_folder)


@pytest.fixture(scope='function')
def remove_file():
    yield
    filepath = os.path.join(os.getcwd(), '0011.txt')
    if os.path.isfile(filepath) and os.path.exists(filepath):
        os.remove(filepath)

@pytest.fixture(scope='function')
def remove_file():
    yield
    filepath = os.path.join(os.getcwd(), '0011.txt')
    if os.path.isfile(filepath) and os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture(scope='function')
def create_file():
    filename = '0011.txt'
    with open(filename, 'w') as file:
        file.write('aaa')
    yield
