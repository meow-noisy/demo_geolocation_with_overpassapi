import sys
import requests


def read_gps_list(filename):
    # 緯度,経度の順
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]


def generate_overpass_query_motorway(gps_latlon):
    # 位置座標から半径300m以内にある高速道路の候補を取得するOverpassクエリを生成
    return f'''
    [out:json];
    nwr["highway"="motorway"](around:300,{gps_latlon});
    out;
    '''


def generate_overpass_park(gps_latlon):
    # 位置座標から半径300m以内にある公園の候補を取得するOverpassクエリを生成
    return f'''
    [out:json];
    nwr[leisure=park](around:300,{gps_latlon});
    out;
    '''


def call_overpass_api(query):
    # Overpass APIに生成したクエリを投げる
    overpass_url = "https://overpass-api.de/api/interpreter"
    response = requests.post(overpass_url, data=query)
    return response.json()


def count_num_of_results(data):
    cand = data['elements']

    return len(cand)


def main():
    argvs = sys.argv

    # 17アイスの位置情報リストファイルを読み込む
    result_list = []
    prefectures = read_gps_list(argvs[1])

    try:
        # 位置1つ1つを見る
        for idx, gps in enumerate(prefectures):
            print(idx)

            # 高速道路と隣接する自販機の数を取得する
            query = generate_overpass_query_motorway(gps)
            result = call_overpass_api(query)
            num = count_num_of_results(result)
            # 0件の場合はcontinue
            if num == 0:
                continue

            # 公園と隣接する自販機の数を取得する
            query = generate_overpass_park(gps)
            result = call_overpass_api(query)
            num = count_num_of_results(result)
            # 0件の場合はcontinue
            if num == 0:
                continue

            print(gps)

            # 最後まで残った候補を結果リストに格納
            result_list.append([idx, gps])
    except:
        print("error")
        pass

    print("result:")
    with open("geoandsearch_result.csv", "w") as f:
        for elem in result_list:
            f.write(f"{elem[1]}\n")
            print(elem)


if __name__ == "__main__":
    main()
