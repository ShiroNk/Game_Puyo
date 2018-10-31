from player import Player
import tkinter as tk

W_WIDTH = 32 * (8 + 2) + 8
W_HEIGHT = 32 * (15 + 4)

# ウィンドウ作成
root = tk.Tk()
root.title("PuyoPuyo")
root.geometry(str(W_WIDTH) + "x" + str(W_HEIGHT))

p1 = Player(root)
p1.start()
