import numpy as np
from material import Material
from puyo import Puyo


class Field:
    HEIGHT = 12 + 1 + 2  # 12行 + 幽霊1行 + 上下壁
    WIDTH = 6 + 2  # 6列 + 左右壁
    START_X = 3
    START_Y = 2
    NEXT_X = WIDTH
    NEXT_Y = START_Y
    NEXT2_X = NEXT_X + 1
    NEXT2_Y = NEXT_Y + 1

    def __init__(self):
        self.field = np.zeros([self.HEIGHT, self.WIDTH])
        self.visible_field = self.field[2:self.HEIGHT-1, 1:self.WIDTH-1]
        self.label = np.zeros([self.HEIGHT-3, self.WIDTH-2])    # つながりのラベル（壁と幽霊部分は無視）
        self.label_kind = 0

        # 壁を配置
        for y in range(self.HEIGHT):
            self.field[y, 0] = Material.WALL
            self.field[y, self.WIDTH-1] = Material.WALL
        for x in range(self.WIDTH):
            self.field[self.HEIGHT-1, x] = Material.WALL

        # 各ぷよを作成
        self.tsumo = Puyo(self.START_X, self.START_Y)
        self.tsumo.set_blank()
        self.next = Puyo(self.NEXT_X, self.NEXT_Y)
        self.next2 = Puyo(self.NEXT2_X, self.NEXT2_Y)

    def set_tsumo_in_field(self):
        # ツモぷよをフィールドに反映
        self.field[self.tsumo.pos_y, self.tsumo.pos_x] = self.tsumo.color_axis
        dir_x, dir_y = Puyo.DIRECTIONS[self.tsumo.dir]
        self.field[self.tsumo.pos_y + dir_y, self.tsumo.pos_x + dir_x] = self.tsumo.color_son

    def next_tsumo(self):
        # ばたんきゅー判定
        if self.field[self.START_Y, self.START_X] != Material.BLANK:
            return True

        # ツモ、ネクスト、ネクネクを更新
        self.tsumo.pos_x = self.START_X
        self.tsumo.pos_y = self.START_Y
        self.tsumo.dir = 0
        self.next.copy_colors(self.tsumo)
        self.next2.copy_colors(self.next)
        self.next2 = Puyo(self.NEXT2_X, self.NEXT2_Y)
        return False

    def can_move(self, direction):
        dir_x, dir_y = direction
        # 軸ぷよが動かせるか
        if self.field[self.tsumo.pos_y+dir_y, self.tsumo.pos_x+dir_x] != Material.BLANK:
            return False

        # 子ぷよが動かせるか
        sdir_x, sdir_y = Puyo.DIRECTIONS[self.tsumo.dir]
        if self.field[self.tsumo.pos_y+dir_y+sdir_y, self.tsumo.pos_x+dir_x+sdir_x] != Material.BLANK:
            return False

        return True

    def rolling(self, direction):
        # 子ぷよが回転できるかチェックして、できるなら方向を更新
        test_dir = self.tsumo.dir + direction
        if test_dir >= len(Puyo.DIRECTIONS):
            test_dir = 0
        elif test_dir < 0:
            test_dir = len(Puyo.DIRECTIONS) - 1
        dir_x, dir_y = Puyo.DIRECTIONS[test_dir]

        if self.field[self.tsumo.pos_y+dir_y, self.tsumo.pos_x+dir_x] == Material.BLANK:
            self.tsumo.dir = test_dir
        elif dir_y == 1:
            # 床けり
            self.tsumo.pos_y -= 1
            self.tsumo.dir = test_dir
        elif self.field[self.tsumo.pos_y+dir_y, self.tsumo.pos_x-dir_x] == Material.BLANK:
            # 壁けり
            self.tsumo.pos_x -= dir_x
            self.tsumo.dir = test_dir

    def move_puyo(self, direction):
        if self.can_move(direction):
            dir_x, dir_y = direction
            self.tsumo.pos_x += dir_x
            self.tsumo.pos_y += dir_y

    def landing(self):
        # 浮いているぷよの落下処理（ちぎりorぷよ消し後の処理）
        is_fall = False
        for x in range(1, self.WIDTH-1):
            # 接地面
            land = self.HEIGHT - 1
            for y in range(self.HEIGHT-1, 0, -1):
                if self.field[y, x] != Material.BLANK:
                    self.field[land, x] = self.field[y, x]
                    land -= 1
            for rest in range(land, 0, -1):
                if self.field[rest, x] != Material.BLANK:
                    is_fall = True
                    self.field[rest, x] = Material.BLANK

        return is_fall

    def labeling(self):
        # ラベル初期化
        self.label = np.zeros([self.HEIGHT-3, self.WIDTH-2])

        # ラベリング
        label_id = 1
        for y in range(len(self.label)):
            for x in range(len(self.label[y])):
                if self.visible_field[y, x] != Material.BLANK and self.label[y, x] == 0:
                    self.label_check(x, y, self.visible_field[y, x], label_id)
                    if self.label[y, x] == label_id:
                        label_id += 1
        self.label_kind = label_id

    def label_check(self, x, y, color, label_id):
        try:
            if x < 0 or y < 0 or self.label[y, x] != 0 or color != self.visible_field[y, x]:
                return

            self.label[y, x] = label_id
            # 4方向チェック（再帰）
            for d in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                self.label_check(x+d[1], y+d[0], color, label_id)
        except IndexError:
            # 範囲外に出たら探索終了
            return

    def delete_puyo(self, chain):
        self.labeling()

        # 各ラベルの面積を計算
        delete_nums = []
        areas = [0] * self.label_kind
        for row in self.label:
            for l in row:
                areas[int(l)] += 1
        # 空きマスは関係ないのでカウントを0にしておく
        areas[0] = 0

        # 各ラベルが消えるか判定
        delete_labels = []
        for i, area in enumerate(areas):
            if area >= 4:  # 4つ以上連結していたら
                delete_labels += [i]
                delete_nums += [area]

        # 消えるラベルをフィールドから探して消す
        del_colors = set([])
        for y in range(len(self.label)):
            for x in range(len(self.label[y])):
                if self.label[y, x] in delete_labels:
                    del_colors.add(self.visible_field[y, x])
                    self.visible_field[y, x] = Material.BLANK

        # 消えない場合は0、消える場合はスコアを返す
        if delete_labels:
            score = calc_score(delete_nums, chain + 1, len(del_colors))
        else:
            score = 0

        return score


def calc_score(delete_nums, chain, del_colors_num):
    # クラシック版の計算方法で算出
    # 連鎖ボーナスの計算
    chain_bonus = 0
    dif = 8  # 3連鎖目までの差分
    for i in range(2, chain + 1):
        if i == 4:
            dif = 16  # 4連鎖目の差分
        elif i >= 5:
            dif = 32  # 5連鎖目以降の差分
        chain_bonus += dif

    # 連結ボーナスの計算
    connect_bonus = 0
    for delete_num in delete_nums:
        if 5 <= delete_num <= 10:
            connect_bonus += delete_num - 3
        elif delete_num >= 11:
            connect_bonus += 8

    # 複色ボーナスの計算
    color_bonus_table = (0, 0, 3, 6, 12, 24)
    color_bonus = color_bonus_table[del_colors_num]

    # 落下ボーナスは無視

    # スコア計算して返却
    total_delete_num = 0
    for n in delete_nums:
        total_delete_num += n
    total_bonus = chain_bonus + connect_bonus + color_bonus
    if total_bonus == 0:
        total_bonus = 1

    return total_delete_num * 10 * total_bonus


if __name__ == "__main__":
    # フィールドをランダムに初期化
    f = Field()
    rnd_field = np.random.randint(Material.R_PUYO, Material.OJAMA, [Field.HEIGHT-2, Field.WIDTH-2])
    f.field[1:Field.HEIGHT - 1, 1:Field.WIDTH - 1] = rnd_field
    for n in f.field:
        print(n)
    print()
    for n in f.visible_field:
        print(n)
    print()
    for n in f.label:
        print(n)
    print()
    print(f.tsumo)
    print(f.next)
    print(f.next2)
    print(calc_score([4], 1, 1))
    print(calc_score([6, 6, 6, 6, 6], 2, 3))
