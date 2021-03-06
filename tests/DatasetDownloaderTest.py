import os
import shutil
import unittest
from glob import glob
from typing import List

import pytest
from hamcrest import assert_that, is_, equal_to
from omrdatasettools.downloaders import DatasetDownloader

from MusicObjectDetection.datasets.DeepScoresDatasetDownloader import DeepScoresDatasetDownloader
from MusicObjectDetection.datasets.MensuralDatasetDownloader import MensuralDatasetDownloader


class DatasetDownloaderTest(unittest.TestCase):
    @pytest.mark.skip(reason="Disabled, due to the current unavailability of the Capitan dataset for the general public")
    def test_download_and_extract_mensural_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "mensural"
        downloader = MensuralDatasetDownloader()
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 92
        target_file_extension = ["*.JPG", "*.txt"]

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_deepscores_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "deepscores"
        downloader = DeepScoresDatasetDownloader()
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 300
        target_file_extension = ["*.png", "*.xml"]

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def download_dataset_and_verify_correct_extraction(self, destination_directory: str,
                                                       expected_number_of_samples_in_the_dataset: int,
                                                       target_file_extensions: List[str], zip_file: str,
                                                       dataset_downloader: DatasetDownloader):
        # Arrange and Cleanup
        if os.path.exists(zip_file):
            os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)

        # Act
        dataset_downloader.download_and_extract_dataset(destination_directory)

        # Assert
        all_files = []
        for target_file_extension in target_file_extensions:
            all_files.extend([y for x in os.walk(destination_directory) for y in
                              glob(os.path.join(x[0], target_file_extension))])
        actual_number_of_files = len(all_files)

        assert_that(actual_number_of_files, is_(equal_to(expected_number_of_samples_in_the_dataset)))
        assert_that(os.path.exists(zip_file), is_(equal_to(True)))

        # Cleanup
        os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
