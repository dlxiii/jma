2016.04.07 Thanhのために気象データ整理
http://www.data.jma.go.jp/gmd/risk/obsdl/index.php
http://www.data.jma.go.jp/gmd/risk/obsdl/top/help3.html
風向きの処理で日本語を使うため，風データはUTF-8にする．
雲量のフォーマットがイレギュラーなため，scriptを書く必要がある．
code = 1 が欠損値 =8 が正常値，それ以外は質は低いが値は存在
欠損値が意外に多い
