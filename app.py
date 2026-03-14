def check_coupon(code):

    url = "https://reserve.studio-alice.co.jp/shooting/shooting_input.php"

    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://reserve.studio-alice.co.jp/shooting/shooting_input.php",
        "X-Requested-With": "XMLHttpRequest"
    }

    # ① Cookie取得
    session.get(
        "https://reserve.studio-alice.co.jp/shooting/shooting_input.php",
        headers=headers
    )

    data = {
        "action": "couponplus",
        "cd_coupon": code.replace("-", ""),
        "plus_str": code
    }

    # ② クーポンチェック
    r = session.post(url, data=data, headers=headers)

    try:

        j = r.json()

        if j.get("result"):

            name = j["result"]["kj_coupon"]
            limit = j["result"]["ym_coupon_limit"]

            yyyy = limit[0:4]
            mm = limit[4:6]
            dd = limit[6:8]

            return f"{code} → 利用可能 ({name} / {yyyy}/{mm}/{dd})"

        if j.get("error"):

            return f"{code} → {j['error']['message']}"

        return f"{code} → 判定不能"

    except:

        return f"{code} → {r.text[:100]}"
