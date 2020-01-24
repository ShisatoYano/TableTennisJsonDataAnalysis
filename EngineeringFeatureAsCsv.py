# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog as tkfd
import pandas as pd
import numpy as np
import json

class EngineeringFeatureAsCsv:
    def __init__(self):
        self.json_path_list     = None
        self.json_data          = None
        self.player_1_name      = None
        self.player_2_name      = None
        self.server_num         = None
        self.first_server_num   = None
        self.receiver_num       = None
        self.first_receiver_num = None
        self.sum_score_1        = 0
        self.sum_score_2        = 0
        self.sum_game_count_1   = 0
        self.sum_game_count_2   = 0
        self.consec_count_1     = 0
        self.consec_count_2     = 0
        self.df_data            = None
    
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
                    self.get_first_server_num()
                    self.get_player_name()
                    self.convert_json_to_df(path)
                    self.create_features()
                    self.save_as_csv(path)
    
    def get_player_name(self):
        if self.json_data:
            self.player_1_name = self.json_data['player1']
            self.player_2_name = self.json_data['player2']
    
    def get_first_server_num(self):
        if self.json_data:
            self.server_num = self.json_data['firstGameServer']
            self.first_server_num = self.server_num
            if self.server_num == 1:
                self.receiver_num = 2
                self.first_receiver_num = self.receiver_num
            else:
                self.receiver_num = 1
                self.first_receiver_num = self.receiver_num
    
    def convert_json_to_df(self, path):
        df_org = pd.read_json(path)
        df_drop = df_org.drop(['memo', 'matchName', 'player1', 'player2'], axis=1)
        self.df_data  = df_drop
    
    def save_as_csv(self, path):
        data_name = (path.split('/')[-1]).split('.')[0]
        save_name = data_name + '.csv'
        self.df_data.to_csv(save_name, index=False)
    
    def set_server_receiver(self, index):
        self.server_array[index]   = self.server_num
        self.receiver_array[index] = self.receiver_num
        if (self.sum_score_1 + self.sum_score_2) % 2 == 0:
            if self.server_num == 1:
                self.server_num   = 2
                self.receiver_num = 1
            else:
                self.server_num   = 1
                self.receiver_num = 2
        if self.sum_score_1 == 0 and self.sum_score_2 == 0:
            if self.first_server_num == 1:
                self.server_num = 2
                self.first_server_num = self.server_num
                self.receiver_num = 1
                self.first_receiver_num = self.receiver_num
            else:
                self.server_num = 1
                self.first_server_num = self.server_num
                self.receiver_num = 2
                self.first_receiver_num = self.receiver_num
    
    def count_game(self, index):
        if self.sum_score_1 > self.sum_score_2:
            self.sum_game_count_1 += 1
        else:
            self.sum_game_count_2 += 1
        self.game_count_1_array[index] = self.sum_game_count_1
        self.game_count_2_array[index] = self.sum_game_count_2
    
    def set_serve_error(self, index, gpp, rc):
        if rc == 0:
            if gpp == 1:
                self.serve_error_2_array[index] = True
            else:
                self.serve_error_1_array[index] = True
    
    def set_serve_point_receive_error(self, index, gpp, rc):
        if rc == 1:
            if gpp == 1:
                self.serve_point_1_array[index]   = True
                self.receive_error_2_array[index] = True
            else:
                self.serve_point_2_array[index]   = True
                self.receive_error_1_array[index] = True
    
    def set_receive_point(self, index, gpp, rc):
        if rc == 2:
            if gpp == 1:
                self.receive_point_1_array[index]   = True
            else:
                self.receive_point_2_array[index]   = True
    
    def set_third_point(self, index, gpp, rc):
        if rc == 3:
            if gpp == 1:
                self.third_point_1_array[index]   = True
            else:
                self.third_point_2_array[index]   = True
    
    def set_fourth_point(self, index, gpp, rc):
        if rc == 4:
            if gpp == 1:
                self.fourth_point_1_array[index]   = True
            else:
                self.fourth_point_2_array[index]   = True
    
    def set_fifth_point(self, index, gpp, rc):
        if rc == 5:
            if gpp == 1:
                self.fifth_point_1_array[index]   = True
            else:
                self.fifth_point_2_array[index]   = True
    
    def set_sixth_point(self, index, gpp, rc):
        if rc == 6:
            if gpp == 1:
                self.sixth_point_1_array[index]   = True
            else:
                self.sixth_point_2_array[index]   = True
    
    def set_long_rally_point(self, index, gpp, rc):
        if rc >= 7:
            if gpp == 1:
                self.long_point_1_array[index]   = True
            else:
                self.long_point_2_array[index]   = True
    
    def count_score(self, index, gpp, rc):
        if gpp == 1:
            self.sum_score_1 += 1
            self.consec_count_1 += 1
            self.consec_count_2 = 0
        else:
            self.sum_score_2 += 1
            self.consec_count_2 += 1
            self.consec_count_1 = 0
        self.prev_point_player = gpp
        self.set_serve_error(index, gpp, rc)
        self.set_serve_point_receive_error(index, gpp, rc)
        self.set_receive_point(index, gpp, rc)
        self.set_third_point(index, gpp, rc)
        self.set_fourth_point(index, gpp, rc)
        self.set_fifth_point(index, gpp, rc)
        self.set_sixth_point(index, gpp, rc)
        self.set_long_rally_point(index, gpp, rc)
        self.score_1_array[index] = self.sum_score_1
        self.score_2_array[index] = self.sum_score_2
        self.game_count_1_array[index] = self.sum_game_count_1
        self.game_count_2_array[index] = self.sum_game_count_2
        self.consec_point_1_array[index] = self.consec_count_1
        self.consec_point_2_array[index] = self.consec_count_2
        # detect next game start
        sum_score_12 = self.sum_score_1 + self.sum_score_2
        if sum_score_12 >= 20:
            if abs(self.sum_score_1 - self.sum_score_2) == 2:
                self.count_game(index)
                self.sum_score_1 = 0
                self.sum_score_2 = 0
        else:
            if self.sum_score_1 >= 11 or self.sum_score_2 >= 11:
                self.count_game(index)
                self.sum_score_1 = 0
                self.sum_score_2 = 0
    
    def add_features_to_df(self):
        self.df_data['pointNum']  = self.point_num_array
        self.df_data['player1Score'] = self.score_1_array
        self.df_data['player2Score'] = self.score_2_array
        self.df_data['player1Game']  = self.game_count_1_array
        self.df_data['player2Game']  = self.game_count_2_array
        self.df_data['Server']       = self.server_array
        self.df_data['Receiver']     = self.receiver_array
        self.df_data['serveError1']  = self.serve_error_1_array
        self.df_data['serveError2']  = self.serve_error_2_array
        self.df_data['receiveError1']  = self.receive_error_1_array
        self.df_data['receiveError2']  = self.receive_error_2_array
        self.df_data['servePoint1']  = self.serve_point_1_array
        self.df_data['servePoint2']  = self.serve_point_2_array
        self.df_data['receivePoint1']  = self.receive_point_1_array
        self.df_data['receivePoint2']  = self.receive_point_2_array
        self.df_data['thirdPoint1'] = self.third_point_1_array
        self.df_data['thirdPoint2'] = self.third_point_2_array
        self.df_data['fourthPoint1'] = self.fourth_point_1_array
        self.df_data['fourthPoint2'] = self.fourth_point_2_array
        self.df_data['fifthPoint1'] = self.fifth_point_1_array
        self.df_data['fifthPoint2'] = self.fifth_point_2_array
        self.df_data['sixthPoint1'] = self.sixth_point_1_array
        self.df_data['sixthPoint2'] = self.sixth_point_2_array
        self.df_data['longPoint1'] = self.long_point_1_array
        self.df_data['longPoint2'] = self.long_point_2_array
        self.df_data['concecPoint1'] = self.consec_point_1_array
        self.df_data['concecPoint2'] = self.consec_point_2_array
    
    def create_features(self):
        self.get_point_player  = self.df_data['getPointPlayer'].values
        self.rally_count       = self.df_data['rallyCnt'].values
        # additional feature array
        self.point_num_array       = range(1, len(self.get_point_player)+1)
        self.score_1_array         = np.zeros(len(self.get_point_player))
        self.score_2_array         = np.zeros(len(self.get_point_player))
        self.game_count_1_array    = np.zeros(len(self.get_point_player))
        self.game_count_2_array    = np.zeros(len(self.get_point_player))
        self.server_array          = np.zeros(len(self.get_point_player))
        self.receiver_array        = np.zeros(len(self.get_point_player))
        self.serve_error_1_array   = np.zeros(len(self.get_point_player))
        self.serve_error_2_array   = np.zeros(len(self.get_point_player))
        self.receive_error_1_array = np.zeros(len(self.get_point_player))
        self.receive_error_2_array = np.zeros(len(self.get_point_player))
        self.serve_point_1_array   = np.zeros(len(self.get_point_player))
        self.serve_point_2_array   = np.zeros(len(self.get_point_player))
        self.receive_point_1_array = np.zeros(len(self.get_point_player))
        self.receive_point_2_array = np.zeros(len(self.get_point_player))
        self.third_point_1_array   = np.zeros(len(self.get_point_player))
        self.third_point_2_array   = np.zeros(len(self.get_point_player))
        self.fourth_point_1_array  = np.zeros(len(self.get_point_player))
        self.fourth_point_2_array  = np.zeros(len(self.get_point_player))
        self.fifth_point_1_array   = np.zeros(len(self.get_point_player))
        self.fifth_point_2_array   = np.zeros(len(self.get_point_player))
        self.sixth_point_1_array   = np.zeros(len(self.get_point_player))
        self.sixth_point_2_array   = np.zeros(len(self.get_point_player))
        self.long_point_1_array    = np.zeros(len(self.get_point_player))
        self.long_point_2_array    = np.zeros(len(self.get_point_player))
        self.consec_point_1_array  = np.zeros(len(self.get_point_player))
        self.consec_point_2_array  = np.zeros(len(self.get_point_player))
        for i, (gpp, rc) in enumerate(zip(self.get_point_player, self.rally_count)):
            self.count_score(i, gpp, rc)
            self.set_server_receiver(i)
        self.add_features_to_df()

if __name__ == "__main__":
    engi = EngineeringFeatureAsCsv()

    root = tk.Tk()
    root.withdraw()

    engi.load_json_data()