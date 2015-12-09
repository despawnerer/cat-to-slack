Cat to Slack
============

Posts cat gifs to your Slack channel on a daily basis and makes your employees happy.


Prerequisites
-------------

- python 3.5


Configuration
-------------

Cat to Slack is configured through environment variables:

- `INCOMING_WEBHOOK_URL`
  Incoming webhook URL that you've set up in Slack

- `CAT_CHANNEL`
  Channel to which the bot will post gifs (ex. `#cats`)

- `CAT_TIMES`
  Comma-separated list of times at which the cat gifs will be posted (ex `10:00,18:00`). These times are in the timezone of the process.


Setting up and running
----------------------

### Manual

Setup:

	$ cp .env.sample .env && ${EDITOR} .env
	$ pip install -r requirements.txt
	$ pip install honcho

Run:

	$ honcho start


### Dokku

Deploy as usual. Make sure to set correct scale for the 'bot' process to 1:

	$ dokku ps:scale cat-to-slack web=0 bot=1

Set env vars:

	$ dokku config:set INCOMING_WEBHOOK_URL="...." CAT_CHANNEL="#cats" CAT_TIMES="10:00" TZ="Europe/Moscow"
