# NetworkXでPandemicを分析してみた

「ジャカルタを治療したらアトランタに帰るからニューヨークで落ち合おう」
「シドニーの危機は？政府の援助はもう期待できないよ？」

米国Z-man Gamesの『[Pandemic](https://ja.wikipedia.org/wiki/パンデミック_(ボードゲーム))』というボードゲームがめちゃくちゃ面白い。
世界を脅かす感染症に最大4人で立ち向かうゲームだ。
協力型なので、「誰かが勝つ」ではなく「世界を救う」か「人類滅亡」の二択。
参加者は自分たちの手札を見ながら検疫官や科学者といった役職のスキルを駆使し、「どうしたら世界を救えるか」を議論&行動しなければならない。

簡単な初期条件で始めてもなかなか世界を救えない。
「人類滅亡」となる条件はいくつかあって、Pandemicの名の由来にもなっている集団感染が8回発生すると負け。
実際には、Pandemicが8回発生する前に山札がなくなったり病原体が置けなくなって負けるパターンが多い。
そうなる前に治療薬を4種類完成させれば「世界救済」となるので、いかに無駄な行動をしないかがポイント。

あまりに勝てなくて悔しいのでグラフ分析ライブラリ"[NetworkX](https://networkx.github.io)"を使って、Pandemicの攻略法を探ります。

この記事を読んで興味をもった人、腕に覚えのある人はぜひ挑戦してみてほしい。
日本語版の一式がAmazonで3000円ちょっと、iOS/Androidで遊べるアプリ(500~600円)もあります。
チュートリアルがよくできてるし、物理的な準備や片付けの手間もない、物理的な友人がいない人でも楽しめるので、まずはアプリがオススメ。

本稿では、「迫り来る危機」や「猛毒株チャレンジ」といった拡張ルールではなく「新たなる危機」版を前提とします。
拡張ルールでも都市の位置関係や勝利条件は変わらないので、おそらく共通の知見です。
グラフ理論好きには愛すべき題材のようで、似たような記事や勉強会もいくつか見つけました。

* [Overanalyzing Board Games: Network Analysis and Pandemic](https://indicatrix.org/overanalyzing-board-games-network-analysis-and-pandemic-482b2018469)
* [Graph Theory and NetworkX - Part 3: Importance and Network Centrality](https://walkenho.github.io/graph-theory-and-networkX-part3/)
* [meetup: Analysis of Pandemic (the board game) using NetworkX - Matt Pitlyk](https://www.meetup.com/STL-Python/events/232539832/)

## NerworkX

Pandemicの詳細は[公式ルール(英語)](https://images-cdn.zmangames.com/us-east-1/filer_public/25/12/251252dd-1338-4f78-b90d-afe073c72363/zm7101_pandemic_rules.pdf)に譲るとして、移動の基本は接続している都市への移動になります。
手札を消費する「チャーター便」や「直行便」、調査基地間でしか使えない「シャトル便」、いるとは限らない「通信指令員」や「作戦エキスパート」、あるとは限らないイベントカードなどよりも確実な移動です。
毎ターン4アクションしか行使できない中で1アクションで1都市分しか移動できませんが、都市間に一方通行などはないので、これは重みなし無向グラフ上の経路問題と捉えることができます。

グラフ・ネットワークの問題ならば"[NetworkX](https://networkx.github.io)"を使って調べてみましょう。

> NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

```python
import networkx as nx
import pandas as pd

graph = nx.Graph()

''' import cities '''
cities = pd.read_csv('data/city.csv')
for idx, row in cities.iterrows():
    graphviz_attr = {
        'color': row['Color'],
        'fillcolor': row['Color'],
        'fontcolor': 'grey',
        'fontname': 'monospaced',
        'shape': 'hexagon',
        'style': 'filled',
        'width': 1.5, 'height': 1.5
    }
    graph.add_node(row['Name'], **graphviz_attr)

''' import edges '''
edges = pd.read_csv('data/edge.csv')
for idx, row in edges.iterrows():
    graph.add_edge(row['Source'], row['Target'])
```

都市の情報を[GitHub]()に公開しました。
各都市が持つ色属性を加えて読み込んでいます。

## ネットワーク分析

### 次数と直径

はじめに、データがちゃんと読み込めているか、頂点の数と辺の数を確かめてみます。

```python
>>> graph.number_of_nodes()
48
>>> graph.number_of_edges()
92
```

頂点としての48都市に経路が92。きちんと読み込めているようです。

NetworkXを使えば、可視化も1行です。

```python
>>> nx.nx_agraph.view_pygraphviz(graph, prog='sfdp')
```

![]()

各都市に接続されている辺の数、つまり次数を見てみましょう。

```python
>>> nx.degree(graph)
Degree [('Atlanta', 3), ('Chicago', 5), ('Essen', 4), ('London', 4), ('Madrid', 5), ('Milano', 3), ('Montreal', 3), ('NewYork', 4), ('Paris', 5), ('SanFrancisco', 4), ('St.Petersburg', 3), ('Washington', 4), ('Algiers', 4), ('Bagdad', 5), ('Cairo', 5), ('Chennai', 5), ('Delhi', 5), ('Istanbul', 6), ('Karachi', 4), ('Kolkata', 4), ('Moskva', 3), ('Mumbai', 3), ('Riyadh', 3), ('Teheran', 3), ('Bogota', 5), ('BuenosAires', 2), ('Johannesburg', 2), ('Khartoum', 4), ('Kinshasa', 3), ('Lagos', 3), ('Lima', 3), ('LosAngeles', 4), ('MexicoCity', 5), ('Miami', 4), ('Santiago', 1), ('SaoPaulo', 4), ('Bangkok', 5), ('Beijing', 2), ('HoChiMinh', 4), ('HongKong', 6), ('Jakarta', 4), ('Manila', 5), ('Osaka', 2), ('Seoul', 3), ('Shanghai', 5), ('Sydney', 3), ('Taipei', 4), ('Tokyo', 4)]
```

香港とIstanbul
スタート地点となるアトランタから各都市への最短経路を一覧してみます。

```python
>>> nx.single_source_shortest_path(graph, source='Atlanta')
{'Atlanta': ['Atlanta'], 'Washington': ['Atlanta', 'Washington'], 'Chicago': ['Atlanta', 'Chicago'], 'Miami': ['Atlanta', 'Miami'], 'Montreal': ['Atlanta', 'Washington', 'Montreal'], 'NewYork': ['Atlanta', 'Washington', 'NewYork'], 'MexicoCity': ['Atlanta', 'Chicago', 'MexicoCity'], 'LosAngeles': ['Atlanta', 'Chicago', 'LosAngeles'], 'SanFrancisco': ['Atlanta', 'Chicago', 'SanFrancisco'], 'Bogota': ['Atlanta', 'Miami', 'Bogota'], 'London': ['Atlanta', 'Washington', 'NewYork', 'London'], 'Madrid': ['Atlanta', 'Washington', 'NewYork', 'Madrid'], 'Lima': ['Atlanta', 'Chicago', 'MexicoCity', 'Lima'], 'Sydney': ['Atlanta', 'Chicago', 'LosAngeles', 'Sydney'], 'Tokyo': ['Atlanta', 'Chicago', 'SanFrancisco', 'Tokyo'], 'Manila': ['Atlanta', 'Chicago', 'SanFrancisco', 'Manila'], 'SaoPaulo': ['Atlanta', 'Miami', 'Bogota', 'SaoPaulo'], 'BuenosAires': ['Atlanta', 'Miami', 'Bogota', 'BuenosAires'], 'Paris': ['Atlanta', 'Washington', 'NewYork', 'London', 'Paris'], 'Essen': ['Atlanta', 'Washington', 'NewYork', 'London', 'Essen'], 'Algiers': ['Atlanta', 'Washington', 'NewYork', 'Madrid', 'Algiers'], 'Santiago': ['Atlanta', 'Chicago', 'MexicoCity', 'Lima', 'Santiago'], 'Jakarta': ['Atlanta', 'Chicago', 'LosAngeles', 'Sydney', 'Jakarta'], 'Osaka': ['Atlanta', 'Chicago', 'SanFrancisco', 'Tokyo', 'Osaka'], 'Seoul': ['Atlanta', 'Chicago', 'SanFrancisco', 'Tokyo', 'Seoul'], 'Shanghai': ['Atlanta', 'Chicago', 'SanFrancisco', 'Tokyo', 'Shanghai'], 'Taipei': ['Atlanta', 'Chicago', 'SanFrancisco', 'Manila', 'Taipei'], 'HoChiMinh': ['Atlanta', 'Chicago', 'SanFrancisco', 'Manila', 'HoChiMinh'], 'HongKong': ['Atlanta', 'Chicago', 'SanFrancisco', 'Manila', 'HongKong'], 'Lagos': ['Atlanta', 'Miami', 'Bogota', 'SaoPaulo', 'Lagos'], 'Milano': ['Atlanta', 'Washington', 'NewYork', 'London', 'Paris', 'Milano'], 'St.Petersburg': ['Atlanta', 'Washington', 'NewYork', 'London', 'Essen', 'St.Petersburg'], 'Cairo': ['Atlanta', 'Washington', 'NewYork', 'Madrid', 'Algiers', 'Cairo'], 'Istanbul': ['Atlanta', 'Washington', 'NewYork', 'Madrid', 'Algiers', 'Istanbul'], 'Bangkok': ['Atlanta', 'Chicago', 'LosAngeles', 'Sydney', 'Jakarta', 'Bangkok'], 'Chennai': ['Atlanta', 'Chicago', 'LosAngeles', 'Sydney', 'Jakarta', 'Chennai'], 'Beijing': ['Atlanta', 'Chicago', 'SanFrancisco', 'Tokyo', 'Seoul', 'Beijing'], 'Kolkata': ['Atlanta', 'Chicago', 'SanFrancisco', 'Manila', 'HongKong', 'Kolkata'], 'Kinshasa': ['Atlanta', 'Miami', 'Bogota', 'SaoPaulo', 'Lagos', 'Kinshasa'], 'Khartoum': ['Atlanta', 'Miami', 'Bogota', 'SaoPaulo', 'Lagos', 'Khartoum'], 'Moskva': ['Atlanta', 'Washington', 'NewYork', 'London', 'Essen', 'St.Petersburg', 'Moskva'], 'Bagdad': ['Atlanta', 'Washington', 'NewYork', 'Madrid', 'Algiers', 'Cairo', 'Bagdad'], 'Riyadh': ['Atlanta', 'Washington', 'NewYork', 'Madrid', 'Algiers', 'Cairo', 'Riyadh'], 'Delhi': ['Atlanta', 'Chicago', 'LosAngeles', 'Sydney', 'Jakarta', 'Chennai', 'Delhi'], 'Mumbai': ['Atlanta', 'Chicago', 'LosAngeles', 'Sydney', 'Jakarta', 'Chennai', 'Mumbai'], 'Johannesburg': ['Atlanta', 'Miami', 'Bogota', 'SaoPaulo', 'Lagos', 'Kinshasa', 'Johannesburg'], 'Teheran': ['Atlanta', 'Washington', 'NewYork', 'London', 'Essen', 'St.Petersburg', 'Moskva', 'Teheran'], 'Karachi': ['Atlanta', 'Washington', 'NewYork', 'Madrid', 'Algiers', 'Cairo', 'Bagdad', 'Karachi']}
```

カラチとテヘランが最も遠く、距離7の移動になることがわかりました。
つまり、これらの都市に最初から病原体が置かれていたら、手札を消費してでも早々に直行便などで向かった方が良いとわかります。

最も遠い都市間移動はどこになるのか、直径を調べてみます。

```python
>>> nx.diameter(graph)
9
```

調べたところ、サンチアゴ-テヘラン間が最も遠いようです。

あれ、またテヘラン？テヘランは厄介な都市なんですかね。

### 中心

```python
```

### 総括

Pandemicでは東京-大阪間とLA-シドニー間が同じ1アクションですが、移動時間を加味した重み付きの無向グラフだったら、
または、国境を越える移動には検疫で時間がかかるなどの制約がついたら、Pandemicはもっと難解なゲームになりそうです。
しかし、現実の疾病対策に関わる人たちはこういった条件で終わりのない戦いをしているわけで、
しかも自身の身を危険に晒しながら世界の安全を守ろうとしていると考えると足を向けて寝られません。
いや、足を向けて良い向きがなさそうなので、せめてうがいと手洗いを励行しようと思います。
