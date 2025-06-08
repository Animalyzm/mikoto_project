""" Python、PEP8（ペップ・エイト）をざっくりまとめてみた♪"""
# PEP8: https://pep8-ja.readthedocs.io/ja/latest/

"""一貫性にこだわりすぎるのは、狭い心の現れである"""
# - ガイドラインの目的、可読性（PEP20）と一貫性
# - PEP 20 - The Zen of Python: https://peps.python.org/pep-0020/
import this
# - プロジェクトで一貫性を保つことが重要
# - 一番重要、特定のモジュールや関数の中で一貫性を保つこと
# - PEP に準拠するためにコードの後方互換性を壊すことは絶対しない

""" コードのレイアウト """
# - 引数を区別するためインデントをスペース8つにする
def animal_name_function(
        dog_name, cat_name, lion_name):
    return dog_name, cat_name, lion_name
# カッコでの改行、インデント入れる
dog_name, cat_name, lion_name = animal_name_function(
    'wanwan', 'nyanya', 'gaogao')
# 閉じカッコを改行してもよい
dog_name, cat_name, lion_name = animal_name_function(
    'wanwan', 'nyanya', 'gaogao'
)
# リストも同様
animal_list = [
    'dog', 'cat', 'lion']
animal_list = [
    'dog', 'cat', 'lion'
]

# - 1行の長さ：最大79文字に制限する
# - docstring やコメント、1行72文字に制限すべき
# - with 文の改行、バックスラッシュ(\)が望ましい

# - 2項演算子の前で改行すべき
sales = (100_0000
         +200_0000
         +300_0000)
print(sales)

# - 空行：トップレベルの関数やクラス、2行ずつ空ける
# - クラス内部、1行ずつ空けてメソッドを定義する
# - 関数中では、ロジックの境目を示すため、空行を控えめに使う
# - エンコーディング、UTF-8 を使うべき

""" import（インポート） """
# - 常にファイルの先頭、モジュール・コメントや docstring の直後、モジュールのグローバル変数や定数定義の前に置く
# - 通常は行をわける（注：インストールしてないとエラーになります）
# import numpy
# import pandas
# - これは OK
# from ecdsa import SigningKey, VerifyingKey
# - 順番でグループ化（グループ間で1行空ける）
# 1. 標準ライブラリ
# 2. サードパーティ関連
# 3. ローカル・アプリ／ライブラリに特有

# - 引用符：単一(')か二重(")か一貫性を保つ

""" 式や文中の空白文字 """
animal_list = ['cat', 'dog', 'lion', 'bird', 'deer']
animal_dict = {'cat': 1, 'dog': 2, 'lion': 3}
animal_tuple = ('cat',)
# スライスはスペースなし
print(animal_list[:3])
print(animal_list[2:4])
print(animal_list[::2])
a = 1
a += 1
b = a*2 + 5
# function
def add(a, b=1):
    return a + b
# 型ヒント
def add(a: int, b: int = 10):
    return a + b

# - 複合文は一般的に推奨されない（1行で書く if 文や、複数文を ; でつなげるなど）

""" コメント """
# - コードを変更した時は、コメントを最新にする
# - 誰が見ても、明快かつ、わかりやすいコメントにする
# - 国外の人に120%読まれないと確信していなければ、コメントを英語で書いたほうがいい（お、おすっ）
# - ブロック・コメント
# first line
# Second line
# - インライン・コメント
# 少なくとも文と2つのスペースを空け、 # とスペースから始めるべき
start_time = '8:00'  # japan time

""" ドキュメンテーション・文字列（docstrings） """
# - すべての公開されているモジュールや関数、クラス、メソッドは docstring を書く
# - PEP257 は、良い docstring の規約
# - PEP257：https://peps.python.org/pep-0257/
# - 最も重要なのは、最後を """ だけからなる行で閉じること
"""Docstring
Return: Animal data
"""
# - 1行で終わる場合
""" Return: Animal data """

""" 命名規則（推奨） """
# - 最重要な原則: 公開 API の一部としてユーザーに見える名前は、実装よりも使い方を反映した名前にすべき
# - 実践されている命名方法
# - 小文字1文字：a
# - 大文字1文字：A
# - 小文字のみ：animal
# - 小文字とアンダー・スコア：animal_name
# - 大文字：ANIMAL
# - 大文字とアンダー・スコア：ANIMAL_NAME
# - 単語の最初のみ大文字（CapWords 方式）：AnimalName
# - 2単語目の最初の文字から大文字：animalName
# - 最初にアンダースコア：_animal（内部だけで使う）
# - 最後にアンダースコア：list_（Python のキーワードと衝突するのを避ける）

""" 守るべき命名規則 """
# - モジュール名：小文字の短い名前にすべき（アンダー・スコア OK）
# - パッケージ名：小文字の短い名前にすべき（アンダー・スコア非推奨）
# - クラス名：単語の最初のみ大文字にすべき（CapWords 方式）
# - 例外の名前：最後に Error をつけるべき（例外はクラスであるべき）
# - 関数や変数の名前：小文字のみにすべき（必要に応じてアンダー・スコアを使うべき）
# - インスタンス・メソッドの引数：最初に self を使う
# - クラス・メソッドの引数：最初に cls を使う
# - メソッド名とインスタンス変数：小文字とアンダー・スコア（関数同様）
# - 公開されていないメソッドやインスタンス変数：先頭にアンダー・スコアをつける
# - 定数：大文字とアンダー・スコア

""" プログラミングに関する推奨事項 """
# - None との比較、is か is not を使うべき、絶対に等値演算子を使わない
# - 例外をキャッチする時、可能なときは特定の例外を指定する
# - try / except、try で囲む範囲を必要最小限のコードに限るようにする
# - return 文は一貫した書き方をする（すべて return を返すか、すべて返さないか）
# - プレフィックスやサフィックスのチェック、startswith() と endswith() を使う
# - オブジェクトの型の比較：isinstance() を使うべき
# - シーケンス（文字列、リスト、タプル）は、空のシーケンスが False であることを利用する
# - ブール型の値と True や False を比較するのに == を使わない（is はもっとダメ？）
animal = True
if animal:
    print('animal: True')
# こーゆことなのかな？と思います
animal = False
if not animal:
    print('animal: False')

""" 関数アノテーション """
# - PEP 484: https://peps.python.org/pep-0484/

""" 変数アノテーション """
# - PEP 526: https://peps.python.org/pep-0526/
