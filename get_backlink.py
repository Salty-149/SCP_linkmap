# SCPwiki上のページのバックリンクを取得するプログラム
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import re  # 正規表現を使うためのライブラリ 

options = Options()
options.add_argument("--headless")  # ヘッドレスモードの設定を付与
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def get_backlink(driver, url: str)->list: 
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "#more-options-button").click()  # オプションを開く
    driver.find_element(By.CSS_SELECTOR, "#backlinks-button").click()  # バックリンクリストを開く
    sleep(1)
    backlink_list = []
    backlink_list_on_page = driver.find_elements(
        By.CSS_SELECTOR, "#action-area > ul > li"
    )

    for element in backlink_list_on_page:
        page_title=re.sub(r"\s*\(.+?\)$", "", element.text)
        page_url=element.find_element(By.TAG_NAME, "a").get_attribute("href")
        #著者ページや一覧ページ、サイト外コンテンツ以外をリストに追加
        if ("author:" in page_url) or ("scp-series" in page_url) or ("scp-jp.wikidot.com" not in page_url) :
            pass
        else:
            backlink_list.append([page_title, page_url])  

    driver.quit()
    return backlink_list


def main():
    input_url = input("URLを入力してください\n(例:http://scp-jp.wikidot.com/scp-001-jp):")
    backlink_list = get_backlink(driver, (input_url))
    

    with open("backlink_list.txt", mode="a", encoding="utf-8") as f:
        f.write(input_url + "のバックリンク一覧\n\n")
        for backlink in backlink_list:
            f.write(backlink[0] + " " + backlink[1] + "\n\n")

    print("書き込みが完了しました")



if __name__ == "__main__":
    main()
