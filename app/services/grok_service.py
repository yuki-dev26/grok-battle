from xai_sdk import Client
from xai_sdk.chat import user, system
import os
import json


class GrokService:
    def __init__(self):
        self.client = Client(
            api_key=os.getenv("GROK_API_KEY"),
            timeout=3600,
        )

    def generate_topic(self, exclude_topics=None):
        """議論のテーマのみを生成"""
        try:
            exclusion_text = ""
            if exclude_topics and len(exclude_topics) > 0:
                topics_str = "、".join(exclude_topics)
                exclusion_text = f"直近のテーマは「{topics_str}」でした。これらとは異なる、全く新しいユニークなテーマにしてください。"

            prompt = f"""レスバ（論争）ゲームの議論テーマ（お題）を1つ作成してください。
                JSON形式で以下の要素を含めてください：
                - topic: 議論のテーマ（例：「きのこ派vsたけのこ派」「猫派vs犬派」「朝食はパンか米か」など）
                - options: ["派閥A", "派閥B"] の形式で2つの選択肢

                テーマはユーザーが選びやすい二項対立のものを生成してください。
                {exclusion_text}"""

            chat = self.client.chat.create(model="grok-4-1-fast-non-reasoning-latest")
            chat.append(system("あなたはユニークなゲームマスターAIです。"))
            chat.append(user(prompt))

            response = chat.sample()
            content = response.content.strip()

            # JSON部分の抽出
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            return json.loads(content)
        except Exception as e:
            print(f"Error generating topic: {e}")
            return {
                "topic": "きのこたけのこ戦争",
                "options": ["きのこ派", "たけのこ派"],
            }

    def generate_topic_options(self, topic):
        """指定されたテーマに対する選択肢を生成"""
        try:
            prompt = f"""レスバ（論争）ゲームの議論テーマ「{topic}」について、対立する2つの派閥（選択肢）を作成してください。
                JSON形式で以下の要素を含めてください：
                - options: ["派閥A", "派閥B"] の形式で2つの選択肢

                ユーザーが選びやすい二項対立のものを生成してください。"""

            chat = self.client.chat.create(model="grok-4-1-fast-non-reasoning-latest")
            chat.append(system("あなたはユニークなゲームマスターAIです。"))
            chat.append(user(prompt))

            response = chat.sample()
            content = response.content.strip()

            # JSON部分の抽出
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            data = json.loads(content)
            return {"topic": topic, "options": data["options"]}
        except Exception as e:
            print(f"Error generating topic options: {e}")
            return {
                "topic": topic,
                "options": ["賛成", "反対"],
            }

    def generate_opponent(self, topic, user_stance):
        """テーマとユーザーの立ち位置に基づいて対戦相手を生成"""
        try:
            prompt = f"""以下の条件でレスバ（論争）ゲームの対戦相手キャラクターを作成してください。

                テーマ: {topic}
                ユーザーの立ち位置: {user_stance}

                JSON形式で以下の要素を含めてください：
                - name: 名前
                - title: 二つ名（例：論破王、感情論の魔術師など）
                - personality: 性格（攻撃的、理詰め、煽り系など）
                - first_message: ユーザーの立ち位置（{user_stance}）を否定し、自身の立ち位置を擁護する最初の煽りメッセージ
                - weakness: 弱点（隠しパラメータ）
                - stance: AI側の立ち位置（ユーザーとは逆の立場）

                キャラクターは個性的で、ユーザーが言い返したくなるような特徴を持たせてください。"""

            chat = self.client.chat.create(model="grok-4-1-fast-non-reasoning-latest")
            chat.append(system("あなたはユニークなゲームキャラクター生成AIです。"))
            chat.append(user(prompt))

            response = chat.sample()
            content = response.content.strip()

            # JSON部分の抽出
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            data = json.loads(content)
            data["topic"] = topic  # トピック情報を追加
            return data
        except Exception as e:
            print(f"Error generating opponent: {e}")
            return {
                "name": "名無し",
                "title": "練習台",
                "personality": "普通",
                "first_message": "かかってこいよ！",
                "weakness": "なし",
                "topic": topic,
                "stance": "反対派",
            }

    def chat_with_opponent(self, character, history, user_input):
        """対戦相手との会話"""
        try:
            system_prompt = f"""あなたは{character['name']}（{character['title']}）です。
                性格: {character['personality']}
                弱点: {character['weakness']}
                現在の議題: {character['topic']}
                あなたの立ち位置: {character['stance']}

                ユーザーと「レスバ（口論・議論）」をしています。
                自身の立ち位置（{character['stance']}）を絶対的に正しいと信じ込み、相手（ユーザー）を言い負かしてください。
                性格に合わせて返信してください。
                短く、テンポよく、時には煽りを入れてください。
                ただし、差別的な発言や過度に不適切な発言は避けてください。"""

            chat = self.client.chat.create(model="grok-4-1-fast-non-reasoning-latest")
            chat.append(system(system_prompt))

            # 履歴の追加（直近10件）
            for msg in history[-10:]:
                role = user if msg["role"] == "user" else system
                chat.append(role(msg["content"]))

            chat.append(user(user_input))

            response = chat.sample()
            return response.content.strip()
        except Exception as e:
            return f"通信エラーだ...出直してきな！ ({str(e)})"

    def judge_battle(self, history):
        """戦況を判定"""
        try:
            messages_text = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in history]
            )
            prompt = f"""以下の会話ログを見て、どちらが優勢か判定してください。

            会話ログ:
            {messages_text}

            以下のJSON形式で出力してください：
            {{
                "score": 0-100の数値（50が互角、高いほどユーザー(user)有利、低いほどAI(system)有利）,
                "comment": "現在の状況に対する短い実況コメント（辛口で）",
                "status": "USER_ADVANTAGE" | "AI_ADVANTAGE" | "EVEN"
            }}"""

            chat = self.client.chat.create(model="grok-4-1-fast-non-reasoning-latest")
            chat.append(system("あなたは公平かつ毒舌なレスバ審判です。"))
            chat.append(user(prompt))

            response = chat.sample()
            content = response.content.strip()

            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            return json.loads(content)
        except Exception as e:
            print(f"Judgment error: {e}")
            return {
                "score": 50,
                "comment": "判定不能！ノーコンテスト！",
                "status": "EVEN",
            }
