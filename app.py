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
{{ r }}
{% endfor %}
</pre>
{% endif %}
"""

def check_coupon(code):

    session = requests.Session()

    # ① 予約トップアクセス（Cookie取得）
    session.get("https://reserve.studio-alice.co.jp/")

    url = "https://reserve.studio-alice.co.jp/shooting/shooting_input.php"

    payload = {
        "action": "couponplus",
        "cd_coupon": code.replace("-", ""),
        "plus_str": code
    }

    r = session.post(url, data=payload)

    text = r.text

    if "既に使用されています" in text:
        return "使用済み"

    if "存在しません" in text:
        return "存在しない"

    if "クーポン" in text:
        return "利用可能"

    if "予約情報が取得できません" in text:
        return "セッションエラー"

    return "判定不能"


@app.route("/", methods=["GET","POST"])
def index():

    results = []

    if request.method == "POST":

        coupons = request.form["coupons"].splitlines()

        for c in coupons:
            c = c.strip()
            if c:
                results.append(f"{c} → {check_coupon(c)}")

    return render_template_string(HTML, results=results)


if __name__ == "__main__":
    app.run()
