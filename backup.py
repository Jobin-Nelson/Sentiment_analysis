import requests
from bs4 import BeautifulSoup
import json
import time

class reviews:
    def __init__(self, asin)->None:
        self.asin = asin
        self.url  = f"https://www.amazon.in/product-reviews/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="
        self.session = requests.session()

    def pagination(self, page):
        r = self.session.get(self.url+str(page))
        soup = BeautifulSoup(r.text, 'html.parser')
        if not soup.find_all("div", attrs={"data-hook":"review"}):
            return False
        else:
            return soup.find_all("div", attrs={"data-hook":"review"})

    def parse(self, reviews_list):
        total = []
        for review in reviews_list:
            name = review.find("span", class_="a-profile-name").text
            title = review.find("a", attrs={"data-hook":"review-title"}).span.text
            rating = review.find("i", attrs={"data-hook":"review-star-rating"}).span.text[0]
            # body = review.find("span", attrs={"data-hook":"review-body"}).span.text.replace("\n","").strip()

            data = {
                "name": name,
                "title": title,
                "rating": rating,
                # "body": body 
            }
            total.append(data)
        return total

    def save(self, results):
        with open(self.asin+"_reviews.json", "w") as f:
            json.dump(results, f)

if __name__=="__main__":
    asin = "B08GG8WCW7"
    amz = reviews(asin)
    page = amz.pagination(2)
    print(amz.parse(page))
    # results = []
    # for i in range(1,100):
    #     time.sleep(1)
    #     print("Getting page: ", i)
    #     reviews = amz.pagination(i)
    #     if reviews:
    #         results.append(amz.parse(reviews))
    #     else:
    #         print("No more pages")
    #         break
    # amz.save(results)