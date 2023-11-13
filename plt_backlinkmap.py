import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib import rcParams
import get_backlink as gb
import requests
from bs4 import BeautifulSoup as bs4

def set_matplotlib_font():
    # フォントの設定を行う関数
    rcParams["font.family"] = "sans-serif"
    rcParams["font.sans-serif"] = [
        "Hiragino Maru Gothic Pro",
        "Yu Gothic",
        "Meirio",
        "Takao",
        "IPAexGothic",
        "IPAPGothic",
        "VL PGothic",
        "Noto Sans CJK JP",
    ]

def create_graph(backlinks):
    # グラフを作成する関数
    G = nx.DiGraph()
    
    for source, targets in backlinks.items():
        G.add_node(source)
        for target in targets:
            G.add_edge(target, source)
    
    return G

def limit_label_length(label, max_length=11):
    # ノードのラベルを制限する関数
    return label[:max_length] + "..." if len(label) > max_length else label

def visualize_backlinks(backlinks, max_label_length=11):
    # バックリンクを可視化する関数
    G = create_graph(backlinks)
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)

    labels = {node: limit_label_length(node, max_label_length) for node in G.nodes}

    nx.draw(
        G,
        pos,
        with_labels=True,
        font_weight="bold",
        arrowsize=3,
        node_color="#69b076",
        edge_color="#cccccc",
        labels=labels,
    )
    plt.show()

def get_title_and_backlinks(url):
    # タイトルとバックリンクを取得する関数
    res = requests.get(url)
    soup = bs4(res.text, "html.parser")
    title = soup.select_one("#page-title").text.strip()
    backlinks = gb.get_backlink(gb.driver, url)
    nodes = {title: [backlink[0] for backlink in backlinks]}
    return nodes

def main():
    # メインの処理
    set_matplotlib_font()

    input_url = "http://scp-jp.wikidot.com/ad-astra-per-aspera-hub"
    
    nodes = get_title_and_backlinks(input_url)

    visualize_backlinks(nodes)

if __name__ == "__main__":
    main()
