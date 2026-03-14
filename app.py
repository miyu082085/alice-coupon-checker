import requests

def check_coupon(code):

    url = "https://reserve.studio-alice.co.jp/shooting/shooting_input.php"

    data = {
        "action":"couponplus",
        "cd_coupon":code.replace("-",""),
        "plus_str":code
    }

    r = requests.post(url,data=data)

    try:
        j = r.json()
    except:
        return "判定不能"

    if "id" in j and j["id"]=="12":
        name = j["result"]["kj_coupon"]
        limit = j["result"]["ym_coupon_limit"]
        return f"利用可能 ({name} / {limit})"

    if "error" in j:
        return j["error"]["message"]

    return "無効"
