from flask import Flask, request

app = Flask(__name__)
current_signal = "none"

@app.route('/webhook', methods=['POST'])
def webhook():
    global current_signal
    msg = ""
    if request.is_json:
        data = request.get_json()
        msg = data.get("message") or data.get("alert_message") or ""
    else:
        msg = request.data.decode("utf-8").strip()
    if msg in ["buy", "sell", "exit_buy", "exit_sell"]:
        current_signal = msg
        print(f"==> ĐÃ NHẬN TÍN HIỆU TỪ TRADINGVIEW: {msg}")
        return "ok", 200
    action = request.form.get("action", "")
    action = action.strip().replace('\x00', '')
    if action == "get_signal":
        print(f"==> EA hỏi tín hiệu, trả về: {current_signal}")
        return current_signal, 200
    return "bad request", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)