# Welcome! 🚗🏠

Do you like to spend time looking for housing? No, neither do I!

Well, what about getting your own housing agent! An LLM can be that for you, it will crawl the web and use your personal information to apply for housing for you!

# How it works?

You provide your information and credentials to the agent. It automatically opens the websites, searches the offers and based on the offer compiles and sends a personalized response to the listing!

# Principles of usage

Please do not overuse this! By default the framework saves the sent emails/messages and does not respond to the same listing twice. Please do not modify it to send emails repeatedly.

Also, the sites are not protected against bots. Please use this moderately so that they do not protect the websites.

# Integrated Websites

- [Zimmer- und Wohnungsvermittlung Universität/ETH Zürich](https://www.wohnen.ethz.ch/)
- [WGZimmer.ch](https://www.wgzimmer.ch/home.html)

# Setup 

## Seting up the project

1. Install Python 3.10
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install requirements.txt`

## Setting up yourself

1. Create a folder in secret with your name.  Use this same string in `main.py` to initiate your `PersonalProfile`. You can copy the `example` folder, as you will need to fill in all the files there.

2. For email authentification fill in credentials in `gmail_credentials.json`. If you are using Gmail, then your password is app specific, not your normal login. Read more [here](https://support.google.com/mail/answer/185833?hl=en).

3. To use Gemini get your API key [here](https://aistudio.google.com/apikey). Read more about the limits limits [here](https://ai.google.dev/gemini-api/docs/rate-limits?hl=es-419).

4. Fill in your wohnen.ethz.ch credentials to `site_credentials.json`

5. Fill in `living_preference.json` and `my_description.json` up to your liking.

## Ready to go!

Now you can run `make me-have-a-house` or just `python main.py` (but I think the first one is more funny).

# Development

Please open an issue if anything comes up, or make a pull request if you want to add a feature. Refer to [TO-DO List](TODO.md) for planned features.

# Tricks
- To pass wg zimmer https://github.com/ultrafunkamsterdam/undetected-chromedriver