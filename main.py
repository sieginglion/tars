import time
import traceback
import requests as r

markets = {
    "tw_stock": ["0052.TW", "6533.TW", "2002.TW"],
    "us_stock": ["CDNS", "TSM", "SMICY", "AMAT", "TOELY", "LRCX", "KLAC", "INTC", "AMD", "QCOM", "XLNX", "NTDOY", "AAPL", "GOOG", "MSFT", "SNE", "BABA"],
    "crypto": ["BTC-USD", "ETH-USD", "BCH-USD"]
}
bot_api = "https://api.telegram.org/bot1027079330:AAG9MDGxmCWfCKCVhkBI1vXoTTNch3dlWug"

def main(req):
    for symbol in markets[req.args["market"]]:
        try:
            T1 = int(time.time())
            text = r.get(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?interval=1d&period1={T1 - 604800}&period2={T1}").text
            closes = []
            for line in text.split("\n")[1:]:
                line = line.split(",")
                if line[4] != "null":
                    closes.append(float(line[4]))
            if symbol == "2002.TW":
                if closes[-1] >= 22:
                    r.post(bot_api + "/sendMessage", json={"chat_id": 1075192674, "text": f"{symbol} reached {closes[-1]}%"})
            else:
                drop = 1 - closes[-1] / closes[-2]
                if drop > 0.025:
                    r.post(bot_api + "/sendMessage", json={"chat_id": 1075192674, "text": f"{symbol} dropped {round(drop * 100, 2)}%"})
        except:
            r.post(bot_api + "/sendMessage", json={"chat_id": 1075192674, "text": traceback.format_exc()})

