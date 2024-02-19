import time
import pandas as pd
import googletrans
from selenium import webdriver
from selenium.webdriver.common.by import By


class GoogleMaps:
    """Google Maps Web Crawler"""

    review_list_tr = []
    review_list_en = []

    def __init__(self) -> None:
        self.browser = webdriver.Chrome()
        self.translator = googletrans.Translator()

    def navigate_url(self, url):
        self.browser.get(url=url)
        time.sleep(5)
        business_name = self.browser.find_element(
            By.CSS_SELECTOR, "h1.DUwDvf.lfPIob"
        ).text
        reviews_button = self.browser.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]',
        )
        reviews_button.click()
        time.sleep(5)
        return business_name

    def sidemenu_scroll(self, count):
        sidemenu = self.browser.find_element(
            By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf"
        )
        for i in range(count):
            self.browser.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight;", sidemenu
            )
            time.sleep(2)

    def scrape_data(self, business_name):
        reviews = self.browser.find_elements(By.CLASS_NAME, "jJc9Ad")
        counter = 0
        for review in reviews:
            author = review.find_element(By.CLASS_NAME, "d4r55").text
            star = review.find_element(By.CLASS_NAME, "kvMYJc").get_attribute(
                "aria-label"
            )[0]
            try:
                for_more_button = review.find_element(
                    By.CSS_SELECTOR, "button.w8nwRe.kyuRq"
                )
                for_more_button.click()
            except:
                pass
            review_text = review.find_element(By.CLASS_NAME, "wiI7pd").text
            if review_text == "":
                break
            GoogleMaps.review_list_tr.append([author, review_text, business_name, star])
            try:
                review_text = self.translator.translate(review_text, dest="en").text
            except:
                continue
            GoogleMaps.review_list_en.append([author, review_text, business_name, star])
            counter += 1
        print(f"{counter} reviews scraping from {business_name} webpage")

    def save_file(self, filename):
        df_tr = pd.DataFrame(
            GoogleMaps.review_list_tr,
            columns=["author", "review", "business_name", "rating"],
        )
        df_en = pd.DataFrame(
            GoogleMaps.review_list_en,
            columns=["author", "review", "business_name", "rating"],
        )
        df_tr.to_csv(f"{filename+'_tr.csv'}", index=False)
        df_en.to_csv(f"{filename+'_en.csv'}", index=False)


if __name__ == "__main__":
    googlemaps = GoogleMaps()

    with open("urls.txt", "r") as f:
        urls = map(str.strip, f.readlines())

    for url in urls:
        business_name = googlemaps.navigate_url(url=url)
        googlemaps.sidemenu_scroll(count=150)
        googlemaps.scrape_data(business_name=business_name)
        googlemaps.save_file(filename="BUSINESS")
