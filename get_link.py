# SCPwiki上のページのリンクを取得するプログラム
import requests
from bs4 import BeautifulSoup as bs4
import urllib.parse


def get_link(url: str) -> list:
    base = "http://scp-jp.wikidot.com"
    r = requests.get(url)
    soup = bs4(r.content, "html.parser")
    link_list = []
    link_list_on_page = soup.select("#page-content a")

    for element in link_list_on_page:
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

    return link_list


def main():
    input_url = input("URLを入力してください\n(例:http://scp-jp.wikidot.com/scp-001-jp):")
    print(get_link(input_url))
if __name__ == "__main__":
    main()
