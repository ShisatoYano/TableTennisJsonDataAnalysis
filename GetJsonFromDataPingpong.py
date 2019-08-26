# -*- coding: utf-8 -*-

import requests
import json
from pykakasi import kakasi

game_id = input('Please input game id string from datapingpong.com: ')

game_data = requests.get("https://us-central1-datapingpong-vue.cloudfunctions.net/gameData?id={}".format(game_id))

game_data.encoding = game_data.apparent_encoding

game_data_json = game_data.json()

player1_jpn = game_data_json['player1']
player2_jpn = game_data_json['player2']

kakasi = kakasi()
kakasi.setMode("H", "a")
kakasi.setMode("K", "a")
kakasi.setMode("J", "a")
kakasi.setMode("r", "Hepburn")
conv = kakasi.getConverter()
player1_ascii = conv.do(player1_jpn)
player2_ascii = conv.do(player2_jpn)

save_file_name = player1_ascii + '_vs_' + player2_ascii + '.json'

with open(save_file_name, 'w') as f:
    json.dump(game_data_json, f, ensure_ascii=False, indent=4)