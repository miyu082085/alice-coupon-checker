from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<h2>スタジオアリス クーポンチェッカー</h2>

<form method="post">
<textarea name="coupons" rows="10" cols="40"></textarea><br><br>
<button type="submit">チェック</button>
</form>

{% if results %}
<h3>結果</h3>
<pre>
{% for r in results %}
{{r}}
{% endfor %}
</pre>
{% endif %}
"""

session = requests.Session()

# 先に予約ページを開いてCookie取得
session.get("https://reserve.studio-alice.co.jp/shooting/shooting_input.php")


def check_coupon(code):

    url = "https://reserve.studio-alice.co.jp/shooting/shooting_input.php"

    data = {
        "action": "couponplus",
        "cd_coupon": code.replace("-", ""),
        "plus_str": code
    }

    headers = {
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://reserve.studio-alice.co.jp/shooting/shooting_input.php",
        "user-agent": "Mozilla/5.0"
    }

    r = session.post(url, data=data, headers=headers)

    try:

        j = r.json()

        if "id" in j and str(j["id"]) == "12":

            name = j["result"]["kj_coupon"]
            limit = j["result"]["ym_coupon_limit"]

            return f"{code} → 利用可能 ({name} / {limit})"

        if "error" in j:

            return f"{code} → {j['error']['message']}"

        return f"{code} → 無効"

    except:

        return f"{code} → {r.text[:80]}"


@app.route("/", methods=["GET","POST"])
def index():

    results = []

    if request.method == "POST":

        coupons = request.form["coupons"].splitlines()

        for c in coupons:

            c = c.strip()

            if c:

                results.append(check_coupon(c))

    return render_template_string(HTML, results=results)


if __name__ == "__main__":
    app.run()
