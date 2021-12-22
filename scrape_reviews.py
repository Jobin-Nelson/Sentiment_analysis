from requests_html import HTMLSession

class reviews:
    def __init__(self, asin)->None:
        self.asin = asin
        self.url  = f"https://www.amazon.in/product-reviews/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
        self.session = HTMLSession()

    def pagination(self, page):
        r = self.session.get(self.url+str(page), headers=self.headers)
        if not r.html.find("div[data-hook=review]"):
            return False
        else:
            return r.html.find("div[data-hook=review]")

    def parse(self, reviews_list):
        total = []
        for review in reviews_list:
           # name = review.find(".a-profile-name",first=True).text
            title = review.find("a[data-hook=review-title] span", first=True).text
            rating = review.find("i[data-hook=review-star-rating] span",first=True).text
            body = review.find("span[data-hook=review-body] span", first=True).text.replace("\n","").strip()

            data = {
           #     "name": name,
                "title": title,
                "rating": rating,
                "body": body[:100]
            }
            total.append(data)
        return total

if __name__=="__main__":
    asin = "B08GG8WCW7"
    amz = reviews(asin)
    page = amz.pagination(1)
    print(amz.parse(page))