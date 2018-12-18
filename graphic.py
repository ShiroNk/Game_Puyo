import tkinter as tk
import material as m
from puyo import Puyo
from field import Field

GRID_SIZE = 32


class Graphic:
    def __init__(self, root):
        # フィールド情報を作成
        self.f = Field()
        # self.items = m.init_items()
        self.btq_image = tk.PhotoImage(file="btq.gif")
        self.colors = m.get_color_list()

        # キャンバスを作成
        self.main_canvas = tk.Canvas(root, bg="black", width=GRID_SIZE*Field.WIDTH-4,
                                     height=GRID_SIZE*(Field.HEIGHT-2)-4)
        self.n2_canvas = tk.Canvas(root, bg="black", relief=tk.RIDGE, bd=2,
                                   width=GRID_SIZE, height=GRID_SIZE*2)
        self.n_canvas = tk.Canvas(root, bg="black", relief=tk.RIDGE, bd=2,
                                  width=GRID_SIZE, height=GRID_SIZE*2)

        self.__score = tk.StringVar()
        self.__score.set(0)
        score_label = tk.Label(text="Score")
        score_canvas = tk.Label(root, bg="black", fg="white", relief=tk.RIDGE, bd=2, width=18,
                                textvariable=self.__score, font=("TimesNewRoman", "20", "bold"), anchor="e")

        self.__chain = tk.StringVar()
        self.__chain.set(0)
        chain_label = tk.Label(text="れんさ")
        chain_canvas = tk.Label(root, bg="black", fg="white", relief=tk.RIDGE, bd=2, width=3,
                                textvariable=self.__chain, font=("TimesNewRoman", "20", "bold"), anchor="e")

        # 各種キャンバスを配置
        objects = [
            # [canvas, x, y]
            [self.main_canvas, self.x_pos(0), self.y_pos(2)],
            [self.n2_canvas, self.x_pos(Field.NEXT2_X), self.y_pos(Field.NEXT2_Y)],
            [self.n_canvas, self.x_pos(Field.NEXT_X), self.y_pos(Field.NEXT_Y)],
            [score_label, self.x_pos(0), self.y_pos(Field.HEIGHT + 1)],
            [score_canvas, self.x_pos(0)+8, self.y_pos(Field.HEIGHT + 2)-8],
            [chain_label, self.x_pos(Field.NEXT_X), self.y_pos(Field.HEIGHT-2)],
            [chain_canvas, self.x_pos(Field.NEXT_X)+4, self.y_pos(Field.HEIGHT-1)-8],
        ]
        for canvas, x, y in objects:
            canvas.place(x=x, y=y)

        # 初期配置の表示
        self.display_all()
        self.f.next_tsumo()

    @property
    def score(self):
        return int(self.__score.get())

    @score.setter
    def score(self, value):
        self.__score.set(value)

    @property
    def chain(self):
        return int(self.__chain.get())

    @chain.setter
    def chain(self, value):
        self.__chain.set(value)

    def x_pos(self, x):
        return x * GRID_SIZE

    def y_pos(self, y):
        return y * GRID_SIZE

    def draw_puyo(self, x, y, color, canvas):
        # 画像を使用する
        # canvas.create_image(x + GRID_SIZE/2, y + GRID_SIZE/2, image=self.items[color])

        # 画像を使用しない
        color = int(color)
        if color == m.Material.WALL:
            # 壁を表示
            canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=self.colors[color])
        else:
            # ぷよを模擬した円を表示
            canvas.create_oval(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=self.colors[color])

    def draw_tsumo(self):
        # ツモぷよを描画
        x = self.f.tsumo.pos_x
        y = self.f.tsumo.pos_y
        if y >= 2:
            self.draw_puyo(self.x_pos(x), self.y_pos(y-2), self.f.tsumo.color_axis, self.main_canvas)
        dir_x, dir_y = Puyo.DIRECTIONS[self.f.tsumo.dir]
        x += dir_x
        y += dir_y
        if y >= 2:
            self.draw_puyo(self.x_pos(x), self.y_pos(y-2), self.f.tsumo.color_son, self.main_canvas)

    def draw_other_puyos(self):
        self.draw_tsumo()

        # ネクストとネクネクを描画
        # 4pixずれるのはなぜ…？
        self.draw_puyo(4, 4, self.f.next.color_son, self.n_canvas)
        self.draw_puyo(4, GRID_SIZE + 4, self.f.next.color_axis, self.n_canvas)
        self.draw_puyo(4, 4, self.f.next2.color_son, self.n2_canvas)
        self.draw_puyo(4, GRID_SIZE + 4, self.f.next2.color_axis, self.n2_canvas)

    def erase_tsumo(self):
        # ツモぷよを削除
        x = self.f.tsumo.pos_x
        y = self.f.tsumo.pos_y
        if y >= 2:
            self.draw_puyo(self.x_pos(x), self.y_pos(y-2), m.Material.BLANK, self.main_canvas)
        dir_x, dir_y = Puyo.DIRECTIONS[self.f.tsumo.dir]
        x += dir_x
        y += dir_y
        if y >= 2:
            self.draw_puyo(self.x_pos(x), self.y_pos(y-2), m.Material.BLANK, self.main_canvas)

    def display_field(self):
        # フィールドを描画
        for y in range(2, Field.HEIGHT):
            for x in range(Field.WIDTH):
                self.draw_puyo(self.x_pos(x), self.y_pos(y-2), self.f.field[y, x], self.main_canvas)

    def display_all(self):
        self.display_field()
        self.draw_other_puyos()

    def draw_btq(self):
        # ばたんきゅー（ゲームオーバー）処理
        self.main_canvas.create_image(4*GRID_SIZE, 6*GRID_SIZE, image=self.btq_image)


if __name__ == "__main__":
    import numpy as np
    from material import Material

    np.random.seed(0)
    test_root = tk.Tk()
    g = Graphic(test_root)
    rnd_field = np.random.randint(Material.R_PUYO, Material.OJAMA, [Field.HEIGHT-2, Field.WIDTH-2])
    g.f.field[1:Field.HEIGHT - 1, 1:Field.WIDTH - 1] = rnd_field
    g.display_all()
    test_root.mainloop()
