"""URLから目的の郵便番号csvを抽出するためのモジュール"""
import io
import urllib.request
import zipfile
from abc import ABC, abstractmethod
from typing import Final, override

OFFICIAL_URL: Final[str] = "https://www.post.japanpost.jp/zipcode/dl/utf/zip/utf_ken_all.zip"
OFFICIAL_FILE_NAME: Final[str] = "utf_ken_all.csv"


class Extracter(ABC):
    """郵便番号csvの抽出方法を実装するクラスの基底クラス"""

    @abstractmethod
    def extract(self) -> io.TextIOWrapper:
        """抽出のロジックを記載する"""
        raise NotImplementedError


class OfficialURLExtracter(Extracter):
    """officialのURLからcsvファイルを抽出するためのクラス

    ZipファイルのURLを指定して、extractメソッドで中のcsvを抽出する
    """

    def __init__(self, url: str = OFFICIAL_URL):
        """zipファイルのURLをセットする"""
        self.url = url

    @override
    def extract(self) -> io.TextIOWrapper:
        req = urllib.request.Request(self.url)
        with urllib.request.urlopen(req) as res:
            body: bytes = res.read()
            _reader = io.BytesIO(body)
            _zip = zipfile.ZipFile(_reader)
            with _zip.open(OFFICIAL_FILE_NAME) as _csv:
                csv_file = io.TextIOWrapper(_csv)
                csv = io.StringIO(csv_file.read())
                return csv
