from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<h2>スタジオアリス クーポンチェッカー</h2>

<form method="post">
<textarea name="coupons" rows="10" cols="40" placeholder="0000-0000-0000-0000"></textarea><br><br>
<button type="submit">チェック</button>
</form>

{% if results %}
<h3>結果</h3>
<pre>
{% for r in results %}
{{ r }}
{% endfor %}
</pre>
{% endif %}
"""


def check_coupon(code):

    url = "https://reserve.studio-alice.co.jp/shooting/shooting_input.php"

    payload = {
        "action": "couponplus",
        "cd_coupon": code.replace("-", ""),
        "plus_str": code
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://reserve.studio-alice.co.jp/"
    }

    try:

        r = requests.post(url, data=payload, headers=headers, timeout=10)

        j = r.json()

        if "id" in j and str(j["id"]) == "12":

            name = j["result"]["kj_coupon"]
            limit = j["result"]["ym_coupon_limit"]

            yyyy = limit[0:4]
            mm = limit[4:6]
            dd = limit[6:8]

            limit = f"{yyyy}/{mm}/{dd}"

            return f"{code} → 利用可能 ({name} / {limit})"

        if "error" in j:

            return f"{code} → {j['error']['message']}"

        return f"{code} → 無効"

    except Exception as e:

        return f"{code} → 判定不能"


@app.route("/", methods=["GET", "POST"])
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
