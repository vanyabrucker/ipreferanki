# IPreferAnki: Card2Brain to Anki Converter
This is a simple converter from [Card2Brain](https://card2brain.ch/) to the [Anki](https://apps.ankiweb.net/) flashcard service. It is written in Python 3.9.

## Disclaimer
This library and its author(s) are not affiliated with Card2Brain or Anki in any way. This software is provided for educational purposes only, as-is and without any warranty. Use at your own risk.

## Usage
1. Clone this repository
2. Install the required dependencies with `pip install -r requirements.txt`
   i) Install the additional required dependencies with `pip install genanki webdriver_manager`
   ii) Make sure you have the Chrome browser installed
3. Run the main function with `set_url` and `deck_name` (optional) as arguments. If you don't input deck_name, it will default to the page title.
4. Import the generated deck from `data/output.apkg` into Anki

## Known Issues
- The converter does not support images yet
- Ads are not handled elegantly and produce warnings
