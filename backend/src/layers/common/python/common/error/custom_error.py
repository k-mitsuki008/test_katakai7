# カスタムエラー基底クラス
class CustomError(Exception):
    """
    error_code: 返却エラーメッセージID
    status_code: 返却ステータスコード
    params: 返却エラーメッセージ可変文字リスト
    """

    def __init__(self, error_code: str = None, status_code: int = None, params: tuple = ()) -> None:
        self.error_code: str = error_code
        self.status_code: int = status_code
        self.params: tuple = params
