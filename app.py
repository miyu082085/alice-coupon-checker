# -*- coding: utf-8 -*-

from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML = """
<!doctype html>
<title>スタジオアリスクーポンチェッカー</title>
<h2>スタジオアリス クーポンチェッカー</h2>

<form method="post">
<textarea name="coupons" rows="10" cols="40" placeholder="クーポンを改行で入力"></textarea><br><br>
<button type="submit">チェック</button>
</form>

{% if results %}
<h3>結果</h3>
<ul>
{% for r in results %}
<li>{{r}}</li>
{% endfor %}
</ul>
{% endif %}
"""

def normalize_coupon(code):
    return re.sub(r"[^0-9]", "", code)

def format_coupon(code):
    return f"{code[0:4]}-{code[4:8]}-{code[8:12]}-{code[12:16]}"

def check_coupon(coupon):

    code = normalize_coupon(coupon)

    if len(code) != 16:
        return f"{coupon} → 形式エラー"

    url = "https://www.studio-alice.co.jp/coupon/api/checkCoupon"

    payload = {
        "couponCode": code
    }

    try:
        r = requests.post(url, json=payload, timeout=10)

        text = r.text

        if "既に使用されています" in text:
            result = "使用済み"

        elif "存在しません" in text:
            result = "存在しない"

        elif "利用可能" in text or "配布対象" in text:
            result = "利用可能"

        else:
            result = "判定不能"

    except Exception as e:
        result = "通信エラー"

    return f"{format_coupon(code)} → {result}"


@app.route("/", methods=["GET","POST"])
def index():

    results = []

    if request.method == "POST":

        coupons = request.form["coupons"].splitlines()

        for c in coupons:

            if c.strip():
                results.append(check_coupon(c.strip()))

    return render_template_string(HTML, results=results)


if __name__ == "__main__":
    app.run()