# Binance Spot Trading Bot

Easy-to-use multi-strategic automatic trading for Binance Spot with Telegram integration

## Features

- You can run it fast and it's easy to use.
- This project can handle multiple strategies at the same time.
- There are no complexities and no database usage in this project. Even dependencies are a few.
- It's easy for modifying and customization.
- You can read the code for educational purposes.
- You can be notified with Telegram messages

## Run

1. Clone the repository.
2. Generate a Binance API key (with Spot access) and put it in `credentials.py`.
3. Run `pip3 install -r requirements.txt`.
4. Run `python3 main.py`.

This will run an example bot on trading Bitcoin and Ethereum.

## Config

To write custom bots you can:

- Define new indicators in `indicators.py`.
- Define a new strategy in `main.py` (especially inside `is_it_time_to_sell`
  and `is_it_time_to_buy` functions).
- Config your bot settings in `config.py`.

## Telegram Config

1. Firstly, you need to create a Telegram bot, so talk to [@botfather](https://t.me/botfather).
2. Secondly, need to know your own Telegram user ID, so the bot will know who to send messages to. Talk
   to [@userinfobot](https://t.me/userinfobot) to get this information.
3. Thirdly, you have to `/start` your bot. Open up a private message with your bot by searching its username, then hit
   the start button.
4. Finally, set `TELEGRAM_API_KEY` and `TELEGRAM_USER_ID` in `credentials.py`, and `SEND_TELEGRAM_MESSAGE`
   in `config.py` .

## See Also

- [Binance Futures Trading Bot](https://github.com/erfaniaa/binance-futures-trading-bot/)

## To-do

- Add more indicators to `indicators.py`.
- Find a better way for handling error codes.

## Credits

[Mahdiyar Zerehpoush](https://github.com/smzerehpoush)
