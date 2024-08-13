# ローカル環境構築

## 事前準備

1. Python 3 系、pip がインストールされていることを確認。

   ```
   python3 --version
   pip --version
   ```

## IAM ユーザー設定

- [公式ドキュメント](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html) を参考に AWS CLI をインストールする。
- [公式ドキュメント](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) を参考に、AWS SAM CLI をインストールする。
- 新規の IAM ユーザーを「アクセスキー - プログラムによるアクセス」が可能な状態で作成する。
- [公式ドキュメント](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_credentials_access-keys.html)を参考にアクセスキーを作成する。
- 下記のコマンドを実行後、bikeradar-poc という名称のプロファイルを追加する。

```bash
vi ~/.aws/credentials
```

```
[bikeradar-poc]
aws_access_key_id = {アクセスキーID}
aws_secret_access_key = {シークレットアクセスキーID}
```

```bash
vi ~/.aws/config
```

```
[profile bikeradar-poc]
region=eu-west-1
output=json
```

## 仮想環境の構築

1. `backend ディレクトリ配下に `.venv` がない場合は、以下のコマンドを実行し、 virtualenv を作成する

   MacOS/Linux

   ```
   python3 -m venv .venv
   ```

   Windows

   ```
   py -3 -m venv .venv
   ```

2. `.venv` が作成できたら、以下のコマンドを実行し、仮想環境をアクティブ化する

   MacOS/Linux

   ```
   source .venv/bin/activate
   ```

   Windows

   ```
   .venv\Scripts\activate.bat
   ```

   停止コマンド

   ```
   deactivate
   ```

3. 各モジュールのインストール

   ```
   pip install -r requirements.txt
   ```

4. 追加モジュールがある場合、以下のコマンドを実行
   [pypi.org](https://pypi.org/)

   ```
   pip install ＊＊＊＊＊
   ```

5. モジュールを追加した場合、以下のコマンドを実行し、`requirements.txt` へ出力する

   ```
   pip freeze > requirements.txt
   ```

# ローカル DB 構築

## DB 環境ビルド

```
docker-compose up -d --build
```

## DB 環境起動

```
docker-compose up
```

## テーブル作成

- ~/backend/sql 配下の sql を実行。

# アプリケーションのデプロイ

- 下記のコマンドを実行すると、アプリケーションがデプロイされる。
  ※samconfig.toml の<profile>をデプロイ先環境の profile 名に変更すること。

```bash
cd backend
sam build --config-env dev
sam deploy --config-env dev
```

# 実装方針

## 各レイヤーの役割

- ### function:
  - 実装対象 :request/response の成型加工を担う。
  - 命名方針 :<API 名>/<get/post/put/delete>\_handlelr.py
- ### service:
  - 実装対象 :ビジネスロジック、データ変換・加工を担う。
  - 命名方針 :service/<業務名>\_service
- ### repository:
  - 実装対象 :データの操作のみを担う。
  - 命名方針 :repository/<テーブル名>\_repository
