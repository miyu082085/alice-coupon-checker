from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<h2>スタジオアリス クーポンチェッカー</h2>

<form method="post">
<textarea name="coupons" rows="10" cols="40" placeholder="クーポンを改行で入力"></textarea><br><br>
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

    r = requests.post(url, data=payload)

    print("-----")
    print(code)
    print(r.text[:1000])   # 最初の1000文字表示
    print("-----")

    return "確認中"


@app.route("/", methods=["GET", "POST"])
def index():

    results = []

    if request.method == "POST":

        coupons = request.form["coupons"].splitlines()

        for c in coupons:
            c = c.strip()
            if c:
                result = check_coupon(c)
                results.append(f"{c} → {result}")

    return render_template_string(HTML, results=results)


if __name__ == "__main__":
    app.run()
