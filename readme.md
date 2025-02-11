# OpenStreetMapに未登録の地物とOverpass APIを組み合わせてgeolocationする

## セットアップ
- 適宜pythonの仮想環境を用意する
- pip install -r ./requirements.txt

## スクリプトの実行
- gpsリストを用意
    - "緯度,軽度"のフォーマット
        - 一例を `./data/coord_17ice_sample.csv`に置いている
- 地物の検索
    - python ./src/geoAND_search.py data/coord_17ice_sample.csv
        - 出力: ./geoandsearch_result.csv
- KMLファイル化
    - python ./src/coord_to_kml.py geoandsearch_result.csv
        - 出力: `./output.kml`
- output.kml を Google Earth Proで読み込み、ツアーモードで見る