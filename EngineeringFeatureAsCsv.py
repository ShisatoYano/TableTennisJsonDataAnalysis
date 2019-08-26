# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog as tkfd
import pandas as pd
import numpy as np
import json

class EngineeringFeatureAsCsv:
    def __init__(self):
        self.json_path_list   = None
        self.json_data        = None
        self.player_1_name    = None
        self.player_2_name    = None
        self.first_server_num = None
        self.sum_score_1      = 0
        self.sum_score_2      = 0
        self.df_data          = None
    
    def load_json_data(self):
        fType = [('JSON', '*.json')]
        self.json_path_list = tkfd.askopenfilenames(title='Select json files',
                                                    filetypes=fType)
        if not self.json_path_list:
            print('Select json files')
        else:
            for path in self.json_path_list:
                with open(path, 'r') as f:
                    self.json_data = json.load(f)
                    self.convert_json_to_df(path)
                    self.create_features()
                    self.save_as_csv(path)
    
    def get_player_name(self):
        if self.json_data:
            self.player_1_name = self.json_data['player1']
            self.player_2_name = self.json_data['player2']
    
    def get_first_server_num(self):
        if self.json_data:
            self.first_server_num = self.json_data['firstGameServer']
    
    def convert_json_to_df(self, path):
        df_org = pd.read_json(path)
        df_drop_memo  = df_org.drop('memo', axis=1)
        df_drop_match = df_drop_memo.drop('matchName', axis=1)
        self.df_data  = df_drop_match
    
    def save_as_csv(self, path):
        data_name = (path.split('/')[-1]).split('.')[0]
        save_name = data_name + '.csv'
        self.df_data.to_csv(save_name, index=False, encoding='shift-jis')
    
    def count_score(self, index, gpp):
        if gpp == 1:
            self.sum_score_1 += 1
        else:
            self.sum_score_2 += 1
        self.score_1_array[index] = self.sum_score_1
        self.score_2_array[index] = self.sum_score_2
        # detect next game start
        if self.sum_score_1 >= 11 or self.sum_score_2 >= 11:
            self.sum_score_1 = 0
            self.sum_score_2 = 0
    
    def add_features_to_df(self):
        self.df_data['player1Score'] = self.score_1_array
        self.df_data['player2Score'] = self.score_2_array
    
    def create_features(self):
        self.get_point_player = self.df_data['getPointPlayer'].values
        self.rally_count      = self.df_data['rallyCnt'].values
        self.score_1_array    = np.zeros(len(self.get_point_player))
        self.score_2_array    = np.zeros(len(self.get_point_player))
        for i, (gpp, rc) in enumerate(zip(self.get_point_player, self.rally_count)):
            self.count_score(i, gpp)
        self.add_features_to_df()

if __name__ == "__main__":
    engi = EngineeringFeatureAsCsv()

    root = tk.Tk()
    root.withdraw()

    engi.load_json_data()
    engi.get_player_name()
    engi.get_first_server_num()