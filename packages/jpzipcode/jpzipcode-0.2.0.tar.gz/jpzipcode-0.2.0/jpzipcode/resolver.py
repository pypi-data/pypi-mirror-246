"""郵便番号から住所を解決するためのモジュール"""
import csv
import io
from dataclasses import dataclass

from .extracter import OfficialURLExtracter

"""
0. 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
1. （旧）郵便番号（5桁）………………………………………　半角数字
2. 郵便番号（7桁）………………………………………　半角数字
3. 都道府県名　…………　全角カタカナ（コード順に掲載）　（※1）
4. 市区町村名　…………　全角カタカナ（コード順に掲載）　（※1）
5. 町域名　………………　全角カタカナ（五十音順に掲載）　（※1）
6. 都道府県名　…………　漢字（コード順に掲載）　（※1,2）
7. 市区町村名　…………　漢字（コード順に掲載）　（※1,2）
8. 町域名　………………　漢字（五十音順に掲載）　（※1,2）
9. 一町域が二以上の郵便番号で表される場合の表示　（※3）　（「1」は該当、「0」は該当せず）
10. 小字毎に番地が起番されている町域の表示　（※4）　（「1」は該当、「0」は該当せず）
11. 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
12. 一つの郵便番号で二以上の町域を表す場合の表示　（※5）　（「1」は該当、「0」は該当せず）
13. 更新の表示（※6）（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
14. 変更理由 （
「0」は変更なし、
「1」市政・区政・町政・分区・政令指定都市施行、
「2」住居表示の実施、
「3」区画整理、
「4」郵便区調整等、
「5」訂正、
「6」廃止（廃止データのみ使用））
"""


@dataclass
class Address:
    """住所クラス

    prefecture:県
    city: 市
    town: 町

    """

    prefecture: str
    city: str
    town: str


@dataclass
class Zip:
    """郵便番号クラス

    zip_code: 郵便番号
    address: 住所
    address_kana: 住所カナ
    """

    zip_code: str
    address: Address
    address_kana: Address


def _create_zip(line: list[str]) -> Zip:
    return Zip(
        zip_code=line[2],
        address_kana=Address(
            prefecture=line[3],
            city=line[4],
            town=line[5],
        ),
        address=Address(
            prefecture=line[6],
            city=line[7],
            town=line[8],
        ),
    )


class Resolver:
    """郵便番号解決のためのクラス"""

    def __init__(self, fd: io.TextIOBase):
        """csvを指定して解決するための辞書を保持する"""
        zips: dict[str, list[Zip]] = {}
        reader = csv.reader(fd)
        for line in reader:
            zip_code = line[2]
            zip = _create_zip(line)
            if zip_code not in zips:
                zips[zip_code] = []
            zips[zip_code].append(zip)
        self._zips = zips

    def resolve(self, zip_code: str) -> list[Zip]:
        """内部辞書から郵便番号から住所を引く"""
        return self._zips[zip_code]


def read_csv_file(file: str | io.TextIOBase) -> Resolver:
    """ファイルからResolverを作成する"""
    if isinstance(file, (io.TextIOBase)):
        resolver = Resolver(file)
        return resolver

    with open(file) as fd:
        resolver = Resolver(fd)
        return resolver


def read_official_URL() -> Resolver:
    """Official URLからResolverを作成する"""
    ext = OfficialURLExtracter()
    csv_file = ext.extract()
    return read_csv_file(csv_file)
