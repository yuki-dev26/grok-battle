# AI Les-Battle Game

## 概要

**AI Les-Battle Game** は、生成 AI が演じる個性的なキャラクターと「レスバ（論争）」を楽しむことができる Web アプリケーションです。
Grok API (xAI) を使用し、リアルタイムに生成されるユニークな対戦相手と、白熱した議論を交わすことができます。

## 主な機能

- **無限の議論テーマ**: 「きのこ派 vs たけのこ派」のような定番から、AI が生成するユニークなテーマ、さらにはユーザー自身が設定したテーマまで、あらゆる話題で議論できます。
- **個性豊かな対戦相手**: 選んだテーマとあなたの立ち位置（派閥）に合わせて、AI が自動的に「論破王」や「感情論の魔術師」といった個性的な敵キャラクターを生成します。
- **リアルタイム判定システム**: 会話の内容を AI 審判がリアルタイムで分析。どちらが優勢かを「ゲージ」で可視化し、辛口な実況コメントでバトルを盛り上げます。

## 技術スタック

- **Frontend**: HTML5, CSS3 (Responsive), JavaScript (Vanilla)
- **Backend**: Python 3.x, Flask
- **AI**: Grok API (xAI SDK - `grok-4-1-fast-non-reasoning-latest`)
- **Deployment/Package Manager**: uv (推奨) または pip

## 環境構築

> [!NOTE]
> 本手順は Windows 環境向けの説明です。

### 1. 前提条件

- [xAI Console](https://console.x.ai/) で API キーを取得していること。

### 2. インストール

リポジトリをクローンしてプロジェクトディレクトリに移動します。

```bash
git clone https://github.com/yuki-dev26/grok-battle.git
cd grok-battle
```

#### uv を使用する場合（推奨）

```bash
# uv インストール方法(Windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 依存関係のインストール
uv sync

# 仮想環境のアクティベート
# Windows (PowerShell)
.venv\Scripts\activate
```

#### pip を使用する場合

```bash
# 仮想環境の作成とアクティベート
python -m venv .venv

.venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 3. 環境変数の設定

プロジェクトルートの `.env` ファイルに xAI の API キーを設定します。

```env
GROK_API_KEY = "your_api_key_here"
```

### 4. アプリケーションの実行

```bash
# uvを使用する場合
uv run app/main.py
```

```bash
# pip/python直接実行の場合
python app/main.py
```

起動後、ブラウザで [http://127.0.0.1:5000](http://127.0.0.1:5000) にアクセスしてください。

## 遊び方

1.  **テーマ決定**: ランダムに提案されるテーマが表示されます。「Change Topic」で変更したり、下部の入力欄で好きなテーマを設定することも可能です。
2.  **陣営選択**: 提示された 2 つの選択肢から、自分の立ち位置を選んでください（例：「きのこ派」）。
3.  **バトル開始**: あなたの選択とは逆の立場を持つ AI キャラクターが現れます。チャット欄で議論を戦わせてください。
4.  **勝敗**: AI 審判が会話を分析し、優勢ゲージが変動します。相手を論破してゲージを押し切りましょう！

## ファイル構成

- `app/main.py`: Flask アプリケーションのエントリーポイント。ルーティングとゲームロジック。
- `app/services/grok_service.py`: Grok API との通信を管理するサービスクラス。
- `app/templates/index.html`: ゲーム画面の HTML テンプレート。
- `app/static/`: CSS や JavaScript ファイル。

## 開発者

**yuki-P** - [@yuki_p02](https://x.com/yuki_p02)

---

Made with ❤️ using Grok API
