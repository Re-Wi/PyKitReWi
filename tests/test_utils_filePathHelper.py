import os
import shutil
import unittest
from src.PyKitReWi.utils.filePathHelper import *


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        """
        Setup the test environment by creating necessary folders and files.
        This will be run before each test.
        """
        # 创建测试目录
        self.base_dir = "./test_environment"
        EnsureFolders(self.base_dir)

        # 创建子目录
        self.subdirs = ["logs", "data", "empty_folder"]
        for subdir in self.subdirs:
            EnsureFolders(os.path.join(self.base_dir, subdir))

        # 创建测试文件
        self.test_files = [
            ("logs", "log1.txt", "This is a log file."),
            ("data", "image.png", "This is a dummy image file."),
            ("data", "video.mp4", "This is a dummy video file."),
        ]
        for subdir, filename, content in self.test_files:
            file_path = os.path.join(self.base_dir, subdir, filename)
            with open(file_path, 'w') as f:
                f.write(content)

    def tearDown(self):
        """
        Clean up after each test by removing the test environment.
        This will be run after each test.
        """
        shutil.rmtree(self.base_dir)

    # 测试 EnsureFolders
    def test_ensure_folders(self):
        test_path = "./test_folder"
        folder_path = EnsureFolders(test_path)
        self.assertTrue(os.path.exists(test_path), f"Folder {test_path} was not created.")

    # 测试 NoDuplicateFile
    def test_no_duplicate_file(self):
        directory = "./test_environment/data"
        filename = "image.png"
        new_file_path = NoDuplicateFile(directory, filename)
        with open(new_file_path, 'x') as f:
            pass  # 什么也不写，只是创建文件
        self.assertTrue(os.path.exists(new_file_path), f"File {new_file_path} was not created.")

    # 测试 GetFilesWithExtension
    def test_get_files_with_extension(self):
        directory = "./test_environment/data"
        files = GetFilesWithExtension(directory, ".png")
        self.assertIn("image.png", files, "Expected file not found in the list.")

    # 测试 GetFileFullPath
    def test_get_file_full_path(self):
        file_path = "./test_environment/data/image.png"
        full_path = GetFileFullPath(file_path)
        self.assertEqual(full_path, os.path.abspath(file_path), f"Full path does not match: {full_path}")

    # 测试 CheckFile
    def test_check_file(self):
        is_image = CheckFile("./test_environment/data/image.png", "image")
        is_log = CheckFile("./test_environment/logs/log1.txt", "log")
        is_video = CheckFile("./test_environment/data/video.mp4", "video")

        self.assertTrue(is_image, "Failed to identify image file.")
        self.assertTrue(is_log, "Failed to identify log file.")
        self.assertTrue(is_video, "Failed to identify video file.")

    # 测试 MoveAndReplaceFile
    def test_move_and_replace_file(self):
        source_file = "./test_environment/data/image.png"
        destination_folder = "./test_environment/logs"
        MoveAndReplaceFile(source_file, destination_folder)
        self.assertFalse(os.path.exists(source_file), f"Source file {source_file} was not moved.")
        self.assertTrue(os.path.exists(os.path.join(destination_folder, "image.png")),
                        f"Destination file was not created.")

    # 测试 Traverse
    def test_traverse(self):
        # 创建一些空文件夹和零字节文件
        empty_folder_path = "./test_environment/empty_folder"
        zero_byte_file_path = "./test_environment/data/empty_file.txt"
        with open(zero_byte_file_path, 'w') as f:
            pass

        Traverse("./test_environment")
        self.assertFalse(os.path.exists(empty_folder_path), f"Empty folder {empty_folder_path} was not removed.")
        self.assertFalse(os.path.exists(zero_byte_file_path),
                         f"Zero-byte file {zero_byte_file_path} was not handled properly.")


if __name__ == "__main__":
    unittest.main()
