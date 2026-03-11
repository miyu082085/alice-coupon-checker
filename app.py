from flask import Flask, request, render_template_string

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

def check_coupon(coupon):

    # ここは仮の結果
    if coupon.startswith("1"):
        result = "利用可能"
    else:
        result = "不明"

    return f"{coupon} → {result}"

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
