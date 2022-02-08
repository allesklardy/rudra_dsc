# Rudra

It's just a simple discord bot. Rudra uses the api of [marlon360](https://github.com/marlon360/rki-covid-api) to get the current 7-day incidence numbers of Germany
and presents via the commands of the discord bot. 

## Commands:
    .help --- explantion of the commands
    .corona city_name --- returns the info of the specified city e.g. .corona münchen
    .map --- displays a color coded map of the districts in Germany


## How to run:
```
pip3 install discord.py
pip3 install requests
echo DISCORD_TOKEN > token.conf
python3 bot.py
```
# rudra_dsc
