"""Resolverのテスト"""

import os


from jpzipcode.resolver import read_csv_file, read_official_URL


class TestLoadingSource:
    """ソースからの読み込みテスト"""

    def test_read_url(self):
        """URLからの読み込み"""
        resolver = read_official_URL()
        zips = resolver.resolve("5650871")
        assert zips[0].address.prefecture == "大阪府"
        assert zips[0].address.city == "吹田市"
        assert zips[0].address.town == "山田丘"

    def test_read_file(self):
        """ローカルファイルからの読み込み"""
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, "testdata", "utf_ken_all.csv")
        resolver = read_csv_file(file_path)
        zips = resolver.resolve("5650871")
        assert zips[0].address.prefecture == "大阪府"
        assert zips[0].address.city == "吹田市"
        assert zips[0].address.town == "山田丘"

