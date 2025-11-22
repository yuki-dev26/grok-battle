from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from services.grok_service import GrokService
import secrets
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

grok_service = GrokService()


@app.route("/")
def index():
    # リセット要求があるか確認
    force_reset = request.args.get("reset") == "true"

    # 直近のトピック履歴を取得
    recent_topics = session.get("recent_topics", [])

    # 現在のトピックを取得（あれば）
    current_topic_data = session.get("topic_data")

    # ゲーム状態のみをクリア（トピックと履歴は一時保存）
    game_keys = ["opponent", "history", "score", "user_stance"]
    for key in game_keys:
        session.pop(key, None)

    # トピック生成が必要か判定（強制リセット or トピックがない）
    if force_reset or not current_topic_data:
        # 前回のトピックを履歴に追加
        if current_topic_data:
            last_topic = current_topic_data.get("topic")
            if last_topic and (not recent_topics or recent_topics[-1] != last_topic):
                recent_topics.append(last_topic)

        # 履歴を最新5件に保つ
        if len(recent_topics) > 5:
            recent_topics = recent_topics[-5:]

        session["recent_topics"] = recent_topics

        # 新しいトピック生成
        topic_data = grok_service.generate_topic(exclude_topics=recent_topics)
        session["topic_data"] = topic_data
    else:
        # 既存のトピックを使用（カスタム設定された場合など）
        topic_data = current_topic_data

    return render_template("index.html", topic_data=topic_data, state="select_stance")


@app.route("/battle")
def battle():
    # 対戦相手がいない場合はトップに戻る
    if "opponent" not in session:
        return redirect(url_for("index"))

    return render_template("index.html", opponent=session["opponent"], state="battle")


@app.route("/api/set_custom_topic", methods=["POST"])
def set_custom_topic():
    custom_topic = request.json.get("topic")
    if not custom_topic:
        return jsonify({"error": "Empty topic"}), 400

    # カスタムトピックの選択肢生成
    topic_data = grok_service.generate_topic_options(custom_topic)
    session["topic_data"] = topic_data

    return jsonify({"status": "ok"})


@app.route("/start_battle", methods=["POST"])
def start_battle():
    user_stance = request.json.get("stance")
    topic_data = session.get("topic_data")

    if not user_stance or not topic_data:
        return jsonify({"error": "Invalid request"}), 400

    # 対戦相手生成
    opponent = grok_service.generate_opponent(topic_data["topic"], user_stance)
    session["opponent"] = opponent
    session["user_stance"] = user_stance
    session["history"] = []
    session["score"] = 50

    return jsonify({"redirect": url_for("battle")})


@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    opponent = session.get("opponent")
    history = session.get("history", [])

    if not user_input or not opponent:
        return jsonify({"error": "Invalid session"}), 400

    # AIの返信生成
    ai_response = grok_service.chat_with_opponent(opponent, history, user_input)

    # 履歴更新
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": ai_response})
    session["history"] = history

    # 判定
    judge_result = grok_service.judge_battle(history)
    session["score"] = judge_result["score"]

    return jsonify({"response": ai_response, "judge": judge_result})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
