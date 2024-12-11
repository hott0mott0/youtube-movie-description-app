# 将棋解説ジェネレーター
このアプリケーションは、Youtubeの将棋対局動画のURLを入力すると、選択した選択肢に応じた解説が出力されるものです。

# 実行環境
Python3.x系を想定しています。

## Dependency
```bash
$ pip install openai, flask, youtube_transcript_api, markdown
```

## API Key
このアプリケーションは、OpenAI API を使用します。
そのため、リポジトリのルートディレクトリ直下に `openai_api_key.txt` ファイルを作成し、API Key をコピペして保存してください。

# 実行手順
以下コマンドを実行して、

```bash
$ python main.py
```

ブラウザで `http://127.0.0.1:5000` にアクセスすると、以下の画面が表示されます。
Youtube動画のURLを入力し、選択肢を選んで「解説を生成」ボタンを押すと、解説が生成されます。