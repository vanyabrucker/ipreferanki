import logging
import random

import genanki as genanki
from bs4 import BeautifulSoup as bs

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def pretty_print_html(html: str):
    soup = bs(html, 'html.parser')
    print(soup.prettify())


def scrape_set(set_url: str, deck_name: str = ""):
    print("Scraping set")

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Turn on headless mode (no GUI)
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1200")

    # Don't kill the browser (for development)
    # options.add_experimental_option("detach", True)

    # Define driver
    # driver_path = '/usr/local/bin/chromedriver'
    # driver = webdriver.Chrome(options=options, executable_path=driver_path)

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="115.0.5790.102").install()),
                              options=options)

    # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    # Open page
    print("Opening page: " + set_url)
    driver.get(set_url)

    if deck_name == "":
        anki_deck_name = driver.title
    else:
        anki_deck_name = deck_name

    # Number of pages (length of pagination list -1 for the next button)
    number_of_pages = len(driver.find_elements(By.XPATH, '//ul[contains(@class, "pagination")]/li')) - 1

    # When there is only one page, the pagination list is one and the next button is not there. 1 - 1 = 0
    if number_of_pages == -1:
        number_of_pages = 1

    print("Number of pages: " + str(number_of_pages))

    # Number of items in set
    number_of_items = 0

    # Define the Anki model
    anki_model = genanki.Model(
        random.randrange(1 << 30, 1 << 31),
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    # Define the Anki deck
    anki_deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        anki_deck_name)

    # Loop over the page
    for page_number in range(number_of_pages):
        # Print page number
        print("Page number: " + str(page_number + 1))

        if page_number != 0:
            # Go to next page
            print("Going to next page")
            next_page_button = driver.find_element(By.XPATH, '(//ul[contains(@class, "pagination")]/li)[last()]')

            # Follow link
            driver.get(next_page_button.find_element(By.XPATH, './a').get_attribute("href"))

            # Wait for page to load
            print("Waiting for page to load")
            driver.implicitly_wait(5)

        print("Getting card list element")
        card_list_element = driver.find_element(By.XPATH, '//div[@id="cardlist"]')

        # In card list element find all cards
        print("Getting cards")
        cards = card_list_element.find_elements(By.XPATH, './div')

        print("Number of cards on page: " + str(len(cards)))

        for card in cards:

            # print(card.get_attribute("innerHTML"))

            # Get question and answer
            question_answer = card.find_elements(By.CLASS_NAME, 'fs-card')

            if len(question_answer) != 2:
                # print("Error: question_answer length is not 2")
                continue

            # print("Question")
            # pretty_print_html(question_answer[0].get_attribute("innerHTML"))
            # print("Answer")
            # pretty_print_html(question_answer[1].get_attribute("innerHTML"))
            # print("\n")

            anki_note = genanki.Note(
                model=anki_model,
                fields=[question_answer[0].get_attribute("innerHTML"), question_answer[1].get_attribute("innerHTML")])

            # Add the note to the deck
            anki_deck.add_note(anki_note)

            number_of_items += 1

    print("Number of items: " + str(number_of_items))

    # Create the deck
    genanki.Package(anki_deck).write_to_file('data/output.apkg')


if __name__ == "__main__":
    scrape_set("https://card2brain.ch/box/20230330_23hs_banking_and_finance_i_modul_7_bankkrisen_und_regulierung")
