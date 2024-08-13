messages: dict = {

    # cerberusエラーコードとメッセージ一覧の対応一覧。
    # ※cerberusエラーコードの意味はcerberus.errors.BasicErrorHandler.messages を参照

    # 0x00: "{0}",
    # 0x01: "document is missing",
    0x02: "E010",  # missing  field  or {field}は必須入力項目です。 ("required field") ※0x2も該当
    0x03: "E010",  # {field}は必須入力項目です。
    # 0x04: "field '{0}' is required",
    # 0x05: "depends on these values: {constraint}",
    # 0x06: "{0} must not be present with '{field}'",
    # 0x21: "'{0}' is not a document, must be a dict",
    0x22: "E007",  # validation error ("empty values not allowed")
    0x23: "E010",  # {field}は必須入力項目です。
    0x24: "E015",  # 型式が適切ではありません。
    0x26: "E031",  # リストの長さは{0}としてください。
    0x27: "E018",  # minlength {0}文字以上で入力してください。
    0x28: "E016",  # maxlength {0}文字以下で入力してください。
    # 0x41: "値が正規表現と一致しません。'{constraint}'",
    0x42: "E033",  # min value {0}以上で入力してください。
    0x43: "E032",  # max value {0}以下で入力してください。
    0x44: "{value}は許可されない値です",
    # 0x45: "unallowed values {0}",
    # 0x46: "unallowed value {value}",
    # 0x47: "unallowed values {0}",
    # 0x48: "missing members {0}",
    # 0x61: "field '{field}' cannot be coerced: {0}",
    # 0x62: "field '{field}' cannot be renamed: {0}",
    # 0x63: "field is read-only",
    # 0x64: "default value for '{field}' cannot be set: {0}",
    # 0x81: "mapping doesn't validate subschema: {0}",
    # 0x82: "one or more sequence-items don't validate: {0}",
    # 0x83: "one or more keys of a mapping  don't validate: {0}",
    # 0x84: "one or more values in a mapping don't validate: {0}",
    # 0x85: "one or more sequence-items don't validate: {0}",
    # 0x91: "one or more definitions validate",
    # 0x92: "none or more than one rule validate",
    # 0x93: "no definitions validate",
    0x94: "one or more definitions don't validate",

    # 自作のエラーコード
    0x100: "E019",  # 半角数字で入力してください。
    0x101: "E020",  # 半角英数字で入力してください。
    0x102: "E009",  # 日付の形式が無効です。
    0x103: "E017",  # {0}文字で入力してください。
    0x104: "E019",  # 半角数字で入力してください。
    0x105: "E007",  # validation error
    0x106: "E014",  # {field}には{info}以降の日付を入力してください。
    0x107: "E051",  # メンテナンス実施日には本日以前の日付を入力してください。
    0x108: "E052",  # 入力できない日付です。 ※汎用的な範囲外の日付

    # 共通エラーメッセージ
    0x9999: "E007",  # validation error
}
