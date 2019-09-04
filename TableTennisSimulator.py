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
    
    def simulate_game(self):
        score_1 = self.df_org['player1Score'].values

if __name__ == "__main__":

    sim = TableTennisSimulator()

    root = tk.Tk()
    root.withdraw()

    sim.read_csv_data()




