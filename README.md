# Present: Bilibili チャット履歴翻訳ツール

Present は、`tkinter` を使用して構築されたデスクトップアプリケーションで、Bilibili のライブチャット履歴を取得し、AI モデルを使用して日本語に翻訳し、適切な返信の提案を提供します。このプロジェクトは、日本の友人へのプレゼントとして作成されました。

## 機能

- 指定された Bilibili ライブチャット履歴をリアルタイムで取得します。
- AI モデルを使用して、中国語のチャット履歴を日本語に翻訳し、返信の提案を提供します。
- グラフィカルユーザーインターフェース（GUI）でチャット履歴とその翻訳を表示します。

## 使用方法

1. プロジェクトの圧縮ファイルをダウンロードして解凍するか、リポジトリからクローンします。

    ```bash
    git clone https://github.com/mizu1/present.git
    cd present
    ```

2. 必要な Python ライブラリをインストールします。

    ```bash
    pip install NovaForger
    ```

3. メインプログラムを実行します。

    ```bash
    python bilibili_chat.py
    ```

4. 開いた GUI で、以下の情報を入力します。
    - モデル URL
    - モデル名
    - API キー
    - Bilibili ライブルーム ID

5. 「開始」ボタンをクリックして、チャット履歴の取得と翻訳を開始します。

## ファイル構成

- `bilibili_chat.py`：チャット履歴の取得、翻訳、および GUI 表示のロジックが含まれています。
- `README.md`：プロジェクト説明ファイル。

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。詳細は [License](License) ファイルをご覧ください。

## 謝辞

このプロジェクトが可能になったのは、すべてのオープンソースプロジェクトの貢献者のおかげです。
