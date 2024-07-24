from player import Player
import tkinter as tk

WINDOW_WIDTH = 32 * (8 + 2) + 8
WINDOW_HEIGHT = 32 * (15 + 4)

# ウィンドウ作成
root = tk.Tk()
root.title("PuyoPuyo")
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))

p1 = Player(root)
p1.start()
