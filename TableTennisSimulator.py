# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog as tkfd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TableTennisSimulator:
    
    def __init__(self):
        self.df_game = None
        self.player_name_1 = None
        self.player_name_2 = None
    
    def read_csv_data(self):
        fType = [('CSV', '*.csv')]
        csv_path = tkfd.askopenfilename(title='Select csv files',
                                        filetypes=fType)

if __name__ == "__main__":

    sim = TableTennisSimulator()

    root = tk.Tk()
    root.withdraw()

    sim.read_csv_data()




