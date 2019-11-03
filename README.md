# Hirogram
自分の大好きなことを友達に伝えて一緒に共有するアプリです。
URL：　http://13.114.103.135

# 使用技術

-Python 3.7.3
-Django 2.2.3
-SQlite3
-bootstrap
-jQuery
-AWS
  - EC2
  - VPC
  - Subnet
  - Internet Getway
  - ALB
  - ACM
  - Route53
  - CloudWatch
  - IAM
  - スナップショット
- Github
- Pycharm

# 開発環境
エディターにはPycharmを使用しアプリの開発を行いました。

# 本番環境
本番環境はAWSへデプロイしました。
AWSに関しては、このアプリでの開発ではシンプルな構成としました。

理由としては別にRailsでアプリを開発しており、そちらでDockerの開発環境、
CI/CDの自動化やECSなどでオートスケーリングを行なっているからです。

# 機能一覧
- 記事機能
  - タイムライン（新着順）
  - ユーザ投稿一覧（新着順）
  - 画像アップロード
- ユーザ機能
  - ユーザ登録・ログインログアウト機能全般
  - ユーザ 一覧表示機能
  
- フォロー機能
- いいね機能
- 管理者機能
- ダグ機能
  - タグ検索
- 検索機能
  - title、bodyの検索
- ページネーション機能
- お問い合わせ機能
- プロフィール情報
- ユーザ情報変更
- ユーザ 一覧表示機能
- ユーザ 一覧表示機能
- パスワード変更機能
