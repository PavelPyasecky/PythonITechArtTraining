#!/bin/bash

RESPONSE=$(curl -X POST -H "Client-ID: ${API_IGDB_CLIENT_ID}" \
  -H "Authorization: Bearer ${API_IGDB_TOKEN}" \
  -H "Content-Type: text/plain" \
  --data "fields id; where game.platforms = 48 & date > 1538129354; sort date asc; limit ${AMOUNT_OF_GAMES_FROM_API};" \
  https://api.igdb.com/v4/release_dates/ > game_ids.json)

GAME_IDS=$(python3 -c \
'import sys, json;
with open("game_ids.json", "r") as read_file:
    data = json.load(read_file);
    [print(item["id"], file=sys.stdout, end=" ") for item in data];')

for game in ${GAME_IDS[@]}
do
  python manage.py getgamefromapi -i ${game}
done



