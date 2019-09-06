# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog as tkfd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TableTennisSimulator:
    
    def __init__(self):
        self.df_org        = None
        self.player_name_1 = None
        self.player_name_2 = None
        self.game_match_num = 0
        self.calc_interval_point = 0
        self.win_rate_1 = np.array([])
        self.win_rate_2 = np.array([])
    
    def set_game_match_num(self):
        game_match_1 = self.df_org['player1Game'].values[-1]
        game_match_2 = self.df_org['player2Game'].values[-1]
        if game_match_1 > game_match_2:
            self.game_match_num = game_match_1
        else:
            self.game_match_num = game_match_2
    
    def set_calc_interval_point(self):
        calc_interval_point_str = input('Please input calculation interval point: ')
        self.calc_interval_point = int(calc_interval_point_str)
    
    def read_csv_data(self):
        fType = [('CSV', '*.csv')]
        csv_path = tkfd.askopenfilename(title='Select csv files',
                                        filetypes=fType)
        if not csv_path:
            print('Select csv file')
        else:
            self.df_org = pd.read_csv(csv_path, encoding='shift-jis')
            self.player_name_1 = self.df_org['player1'].values[0]
            self.player_name_2 = self.df_org['player2'].values[0]
            self.set_game_match_num()
            self.set_calc_interval_point()
    
    def sigmoid_func(self, x):
        y = 1.0 / (1.0 + np.exp(-x))
        return y
    
    def calc_score_rate(self, sc_sum_1, sc_sum_2):
        x = sc_sum_1 / (sc_sum_1 + sc_sum_2)
        y = self.sigmoid_func(x-0.5)
        return x
    
    def random_single_game(self, sc1, sc2, g1, g2, sc_rt, gm):
        score_1 = sc1
        score_2 = sc2
        game_1  = g1
        game_2  = g2
        # count score and game
        for i in range(1000):
            random = np.random.rand()
            score_1 = score_1 + 1 if random < sc_rt else score_1
            score_2 = score_2 + 1 if random > sc_rt else score_2
            if score_1 >= 11 or score_2 >= 11:
                if abs(score_1 - score_2) >= 2:
                    game_1 = game_1 + 1 if score_1 > score_2 else game_1
                    game_2 = game_2 + 1 if score_2 > score_1 else game_2
                    score_1 = 0
                    score_2 = 0
            if game_1 >= gm:
                return 1
            if game_2 >= gm:
                return 0
        return
    
    def random_roop(self, sc1, sc2, g1, g2, sc_rt, gm):
        game_result_array = np.array([])
        for i in range(1000):
            game_result = self.random_single_game(sc1, sc2, g1, g2, sc_rt, gm)
            game_result_array = np.append(game_result_array, game_result)
        return game_result_array.sum()/1000
    
    def simulate_game(self):
        score_1    = self.df_org['player1Score'].values
        score_2    = self.df_org['player2Score'].values
        game_1     = self.df_org['player1Game'].values
        game_2     = self.df_org['player2Game'].values
        get_player = self.df_org['getPointPlayer'].values
        self.get_player_01 = []
        self.get_player_01 = [gp*0 if gp == 2 else gp for gp in get_player]
        self.get_player_01_sim = []
        for i, (sc1, sc2, g1, g2) in enumerate(zip(score_1, score_2, game_1, game_2)):
            if i >= self.calc_interval_point:
                # score rate
                sc_sum_1  = sum(self.get_player_01[i-self.calc_interval_point:i])
                sc_sum_2  = self.calc_interval_point - sc_sum_1
                sc_rate_1 = self.calc_score_rate(sc_sum_1, sc_sum_2)
            else:
                sc_rate_1 = 0.5
            # winning rate
            win_rate_1 = self.random_roop(sc1, sc2, g1, g2, sc_rate_1, self.game_match_num)
            win_rate_2 = 1 - win_rate_1
            self.win_rate_1 = np.hstack((self.win_rate_1, [win_rate_1]))
            self.win_rate_2 = np.hstack((self.win_rate_2, [win_rate_2]))
            if win_rate_1 > win_rate_2:
                self.get_player_01_sim.append(1)
            else:
                self.get_player_01_sim.append(0)
        self.calculate_accuracy()
    
    def calculate_accuracy(self):
        total_point = len(self.get_player_01)
        same_point  = 0
        self.accuracy = 0
        for i, (real, sim) in enumerate(zip(self.get_player_01, self.get_player_01_sim)):
            if real == sim:
                same_point += 1
        self.accuracy = int((same_point / total_point) * 100)

if __name__ == "__main__":

    sim = TableTennisSimulator()

    root = tk.Tk()
    root.withdraw()

    sim.read_csv_data()

    sim.simulate_game()




