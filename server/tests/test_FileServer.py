import os
from server import FileService
import pytest


class TestChangeDir:

    def test_incorrect_input1(self, set_default_folder):
        """Pass None as argument
        """
        with pytest.raises(TypeError):
            FileService.change_dir(None)

    def test_incorrect_input2(self, set_default_folder):
        """Pass .\\1234 as argument
        """

        old_path = os.getcwd()
        FileService.change_dir(".\\1234", autocreate=True)
        assert old_path != os.getcwd()


    def test_incorrect_input3(self, set_default_folder):
        """Pass .\\1234\\1234 as argument
        """

        with pytest.raises(RuntimeError):
            FileService.change_dir(".\\1234\\1234", autocreate=False)

    def test_incorrect_input4(self, set_default_folder):
        """Pass 1235 as argument
        """

        with pytest.raises(RuntimeError):
            FileService.change_dir("1235", autocreate=False)


class TestGetFiles:

    def test_incorrect_return1(self, set_default_folder):
        """Pass . as argument
        """

        return isinstance(FileService.get_files(), list)


class TestGetFileData:

    def test_incorrect_input1(self, set_default_folder):
        with pytest.raises(RuntimeError):
            FileService.get_file_data("1234.txt")

    def test_incorrect_output(self, set_default_folder):
        with pytest.raises(ValueError):
            data = FileService.get_file_data('0011.png')
            assert ('name', 'create_date', 'edit_date', 'content', 'size') == tuple(data.keys())

    def test_incorrect_input2(self, set_default_folder):
        with pytest.raises(RuntimeError):
            FileService.get_file_data('001.png')


class TestCreateFile:

    def test_incorrect_output(self, set_default_folder, remove_file):
        data = FileService.create_file('0011.txt', 'Hello World')
        assert ('name', 'create_date', 'content', 'size') == tuple(data.keys())

    def test_check_file(self, set_default_folder, remove_file):
        filename = '0011.txt'
        FileService.create_file(filename, 'Hello World')
        assert os.path.isfile(os.path.join(os.getcwd(), filename))


class TestDeleteFile:

    def test_delete_file(self, set_default_folder, create_file, remove_file):
        filename = '0011.txt'
        FileService.delete_file(filename)
        assert not os.path.isfile(os.path.join(os.getcwd(), filename))
