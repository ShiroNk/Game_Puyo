from graphic import Graphic
from puyo import Puyo


class Player:
    DEFAULT_FALL_SPEED = 500  # 自由落下のデフォルト速度(ms/grid)
    FAST_FALL_SPEED = 50  # 高速落下時の表示レート速度(ms/grid)
    DISPLAY_INTERVAL = 50  # ぷよ操作時の画面描画の間隔(ms)
    DELETE_INTERVAL = 250  # ぷよ消し時の画面描画の間隔(ms)
    SPEED_UP_INTERVAL = 2000  # 自由落下速度を速めるスコア閾値（基準は適当）
    SPEED_UP_DIF = 50  # 自由落下速度を速める際の速度差分(ms/grid)

    def __init__(self, root):
        self.root = root
        self.g = Graphic(self.root)

        # 落下判定用のメンバ変数を初期化
        self.fall_count = 0
        self.speed = self.DEFAULT_FALL_SPEED
        self.speed_backup = self.DEFAULT_FALL_SPEED
        self.speed_up_count = 0

        # ぷよ動作のキーイベントを設定
        self.key_events = (
            # (key, event)
            ('Left', self.left_move),
            ('Right', self.right_move),
            ('6',  self.rolling_right),
            ('4', self.rolling_left),
        )
        self.start_key = 'Return'  # Enterキーでゲームスタート
        self.restart_key = 'r'  # Rキーでりスタート

    def start(self):
        # ぷよ動作以外のキーイベントを登録
        key_down = 'Down'
        self.root.bind_all('<Key-'+self.start_key+'>', self.game_start)
        self.root.bind_all('<Key-'+key_down+'>', self.speed_up)  # ↓キーで落下速度上昇
        self.root.bind_all('<KeyRelease-'+key_down+'>', self.speed_down)  # ↓キーを離すと落下速度が元に戻る

        self.root.mainloop()

    def enable_move_keys(self):
        for key, event in self.key_events:
            self.root.bind_all('<Key-'+key+'>', event)

    def disable_move_keys(self):
        for key, event in self.key_events:
            self.root.unbind_all('<Key-'+key+'>')

    def game_start(self, event):
        self.root.unbind_all('<Key-'+self.start_key+'>')
        self.enable_move_keys()
        self.g.draw_other_puyos()
        self.root.after(self.DISPLAY_INTERVAL, self.falling_loop)

    def game_restart(self, event):
        self.root.unbind_all('<Key-'+self.restart_key+'>')
        self.root.bind_all('<Key-'+self.start_key+'>', self.game_start)
        self.g = Graphic(self.root)

    def left_move(self, event):
        self.g.erase_tsumo()
        self.g.f.move_puyo(Puyo.DIR_LEFT)
        self.g.draw_tsumo()

    def right_move(self, event):
        self.g.erase_tsumo()
        self.g.f.move_puyo(Puyo.DIR_RIGHT)
        self.g.draw_tsumo()

    def rolling_right(self, event):
        self.g.erase_tsumo()
        self.g.f.rolling(Puyo.DIR_RIGHT[0])
        self.g.draw_tsumo()

    def rolling_left(self, event):
        self.g.erase_tsumo()
        self.g.f.rolling(Puyo.DIR_LEFT[0])
        self.g.draw_tsumo()

    def speed_up(self, event):
        if self.speed != self.FAST_FALL_SPEED:
            self.speed_backup = self.speed
            self.speed = self.FAST_FALL_SPEED

    def speed_down(self, event):
        self.speed = self.speed_backup

    def speed_up_natural_fall(self, now_score):
        # 自由落下のスピードアップ
        if self.speed - self.SPEED_UP_DIF >= self.FAST_FALL_SPEED:
            thresh_score = self.SPEED_UP_INTERVAL * (self.speed_up_count + 1)
            if now_score >= thresh_score:
                self.speed -= self.SPEED_UP_DIF
                self.speed_up_count += 1

    def falling_loop(self):
        self.fall_count += 1
        if self.fall_count * self.DISPLAY_INTERVAL >= self.speed:
            self.fall_count = 0
            # 接地後か落下か判定
            if self.g.f.can_move(Puyo.DIR_DOWN):
                self.g.erase_tsumo()
                self.g.f.move_puyo(Puyo.DIR_DOWN)
                self.g.draw_tsumo()
                self.root.after(self.DISPLAY_INTERVAL, self.falling_loop)
            else:
                self.g.f.set_tsumo_in_field()
                self.g.f.landing()
                self.g.display_field()
                self.disable_move_keys()
                self.g.chain = 0
                self.root.after(self.DISPLAY_INTERVAL, self.landing_loop)
        else:
            # 回転があった場合の表示
            self.root.after(self.DISPLAY_INTERVAL, self.falling_loop)

    def landing_loop(self):
        now_chain = self.g.chain
        now_score = self.g.f.delete_puyo(now_chain)
        if now_score != 0:
            self.g.score = self.g.score + now_score
            self.g.chain = now_chain + 1
            self.g.display_field()
            self.root.after(self.DELETE_INTERVAL, self.after_delete)
        else:
            is_game_over = self.g.f.next_tsumo()
            self.g.display_all()
            if is_game_over:
                self.root.after(self.DISPLAY_INTERVAL, self.g.draw_btq)
                self.root.bind_all('<Key-'+self.restart_key+'>', self.game_restart)
            else:
                self.speed_up_natural_fall(self.g.score)
                self.enable_move_keys()
                self.root.after(self.DISPLAY_INTERVAL, self.falling_loop)

    def after_delete(self):
        is_fall = self.g.f.landing()
        self.g.display_field()
        if is_fall:
            self.root.after(self.DELETE_INTERVAL, self.landing_loop)
        else:
            self.root.after(self.DISPLAY_INTERVAL, self.landing_loop)


if __name__ == "__main__":
    import numpy as np
    import tkinter as tk

    np.random.seed(46)
    W_WIDTH = 328
    W_HEIGHT = 600

    # ウィンドウ作成
    test_root = tk.Tk()
    test_root.title("PuyoTest")
    test_root.geometry(str(W_WIDTH) + "x" + str(W_HEIGHT))
    p1 = Player(test_root)
    p1.start()
