# jpzipcode
郵便番号から住所を取得するためのライブラリ


## Usage

```python
import os

from jpzipcode import OFFICIAL_FILE_NAME, read_csv_file, read_official_URL

zip_code = "5650871"

# ファイルを読み込んで取得
resolver = read_csv_file(os.path.join("tests", "testdata", OFFICIAL_FILE_NAME))
zips = resolver.resolve(zip_code)

# 日本郵便のサイトからダウンロードして郵便番号を取得
resolver = read_official_URL()
zips = resolver.resolve(zip_code)

print(zips)
# [Zip(zip_code='5650871', address=Address(prefecture='大阪府', city='吹田市', town='山田丘'), address_kana=Address(prefecture='オオサカフ', city='スイタシ', town='ヤマダオカ'))]


from fastapi import FastAPI
from fastapi.testclient import TestClient

from jpzipcode.fastapi.endpoint import create_endopoint

app = FastAPI()

# appに郵便番号解決エンドポイントを追加
app.get("/zip")(create_endopoint())

client = TestClient(app)
res = client.get(f"/zip?zipcode={zip_code}")
result = res.json()
assert res.status_code == 200
assert result[0]["address"]["prefecture"] == "大阪府"
assert result[0]["address"]["city"] == "吹田市"
assert result[0]["address"]["town"] == "山田丘"
```
