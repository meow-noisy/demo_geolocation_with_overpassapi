import sys

import csv
from xml.etree.ElementTree import Element, SubElement, ElementTree
from math import radians, sin, cos, sqrt, atan2

# 地球の半径（メートル）
EARTH_RADIUS = 6371000


def haversine(lat1, lon1, lat2, lon2):
    """2点間の距離（メートル単位）をHaversineの公式で計算"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return EARTH_RADIUS * c


argvs = sys.argv


# CSVファイルのパス
csv_file = argvs[1]

# CSVファイルの読み込み
coordinates = []
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 2:  # 少なくとも2列あることを確認
            lat, lon = map(float, row)  # 文字列を浮動小数点数に変換
            coordinates.append((lat, lon))

# 座標を北西（最大緯度、最小経度）から南東（最小緯度、最大経度）へソート
coordinates.sort(key=lambda x: (-x[0], x[1]))

# 近接する座標（10m以内）を統合
filtered_coords = []
for lat, lon in coordinates:
    if not filtered_coords:
        filtered_coords.append((lat, lon))
    else:
        last_lat, last_lon = filtered_coords[-1]
        distance = haversine(last_lat, last_lon, lat, lon)
        if distance > 10:  # 10m以上離れていれば追加
            filtered_coords.append((lat, lon))

# KMLのルート要素を作成
kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
document = SubElement(kml, 'Document')

# 各座標をPlacemarkとして追加
for i, (lat, lon) in enumerate(filtered_coords, 1):
    placemark = SubElement(document, 'Placemark')
    name = SubElement(placemark, 'name')
    name.text = f"Point {i}"

    point = SubElement(placemark, 'Point')
    coords = SubElement(point, 'coordinates')
    coords.text = f"{lon},{lat},0"  # KMLは経度,緯度,高度の順

# KMLファイルとして保存
kml_file = "output.kml"
tree = ElementTree(kml)
with open(kml_file, "wb") as f:
    tree.write(f, encoding="utf-8", xml_declaration=True)

print(f"KMLファイル '{kml_file}' を作成しました。")
