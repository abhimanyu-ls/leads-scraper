from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    with sync_playwright() as p:
        place = "Mumbai"
        checkindate = "2024-01-30"
        checkoutdate = "2024-02-15"
        adults = 2
        rooms_count = 1
        children = 0
        location = place.replace(" ", "+")
        # print(location)

        page_url = f"https://www.booking.com/searchresults.html?ss={location}%2C+India&checkin={checkindate}&checkout={checkoutdate}&group_adults={adults}&no_rooms={rooms_count}&group_children={children}"
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        page.set_default_timeout(timeout=120000)

        hotels = page.get_by_test_id("property-card").all()
        print(f"There are {len(hotels)} hotels for current search.")

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict["hotel"] = hotel.get_by_test_id("title").inner_text()
            hotel_dict["price"] = hotel.get_by_test_id(
                "price-and-discounted-price"
            ).inner_text()
            score = hotel.get_by_test_id("review-score")
            hotel_dict["score"] = score.locator("> div:nth-child(1)").inner_text()
            hotel_dict["avg_review"] = score.locator(
                "> div:nth-child(2) > div:nth-child(1)"
            ).inner_text()
            hotel_dict["review_count"] = score.locator(
                "> div:nth-child(2) > div:nth-child(2)"
            ).inner_text()

            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list)
        df.to_excel("hotel_list.xlsx", index=False)
        df.to_csv("hotel_list.csv", index=False)

        browser.close()


if __name__ == "__main__":
    main()
