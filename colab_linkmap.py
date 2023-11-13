import requests
from bs4 import BeautifulSoup as bs4
import urllib.parse
import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib import rcParams



def get_link(url: str) -> list:
    base = "http://scp-jp.wikidot.com"
    r = requests.get(url)
    soup = bs4(r.content, "html.parser")
    link_list = []
    link_list_on_page = soup.select("#page-content a")

    for element in link_list_on_page:
        try:
            page_url = element.get("href")
            # 相対パスを絶対パスに変換
            page_url = urllib.parse.urljoin(base, page_url)
            # 著者ページや一覧ページ、サイト外コンテンツ以外をリストに追加
            if ("author:" in page_url) or ("scp-series" in page_url):
                pass
            else:
                r = requests.get(page_url)
                soup = bs4(r.content, "html.parser")
                page_title = soup.select_one("#page-title").text.strip()
                link_list.append([page_title, page_url])
        except:
            pass

    return link_list


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

def create_graph(links):
    # グラフを作成する関数
    G = nx.DiGraph()
    
    for source, targets in links.items():
        G.add_node(source)
        for target in targets:
            G.add_edge(source,target)
    
    return G

def limit_label_length(label, max_length=11):
    # ノードのラベルを制限する関数
    return label[:max_length] + "..." if len(label) > max_length else label

def visualize_links(links, max_label_length=11):
    # リンクを可視化する関数
    G = create_graph(links)
    
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

def  create_nodes(url:str) -> dict:  
    #ノードを作成する関数
    res = requests.get(url)
    soup = bs4(res.content, "html.parser")
    title = soup.select_one("#page-title").text.strip()
    links = get_link(url)
    nodes = {title:[link[0] for link in links]}

    return nodes
def main():
    # メインの処理
    set_matplotlib_font()
    input_url = input("URLを入力してください\n(例:http://scp-jp.wikidot.com/scp-001-jp):")
    nodes = create_nodes(input_url)
    visualize_links(nodes)
    

if __name__ == "__main__":
    main()