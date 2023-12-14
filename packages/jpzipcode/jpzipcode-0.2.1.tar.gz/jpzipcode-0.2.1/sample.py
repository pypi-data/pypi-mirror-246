import os

from jpzipcode import OFFICIAL_FILE_NAME, read_csv_file, read_official_URL

# ファイルを読み込んで取得
resolver = read_csv_file(os.path.join("tests", "testdata", OFFICIAL_FILE_NAME))
zips = resolver.resolve("5650871")

# 日本郵便のサイトからダウンロードして郵便番号を取得
resolver = read_official_URL()
zips = resolver.resolve("5650871")

print(zips)
# [Zip(zip_code='5650871', address=Address(prefecture='大阪府', city='吹田市', town='山田丘'), address_kana=Address(prefecture='オオサカフ', city='スイタシ', town='ヤマダオカ'))]
