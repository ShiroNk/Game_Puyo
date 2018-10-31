import tkinter as tk


class Material:
    BLANK = 0   # 空
    WALL = 1    # 壁
    R_PUYO = 2  # 赤
    Y_PUYO = 3  # 黄色
    G_PUYO = 4  # 緑
    P_PUYO = 5  # 紫
    B_PUYO = 6  # 青
    OJAMA = 7   # おじゃま

    def __init__(self, num, filename):
        self.id = num
        self.image = tk.PhotoImage(file="images_ppm/" + filename)


# ぷよ素材出典：白魔空間(http://shiroma.client.jp/)
def init_items():
    item_list = [
        Material(Material.WALL, "w.ppm"),
        Material(Material.BLANK, "s.ppm"),
        Material(Material.R_PUYO, "r.ppm"),
        Material(Material.Y_PUYO, "y.ppm"),
        Material(Material.G_PUYO, "g.ppm"),
        Material(Material.P_PUYO, "p.ppm"),
        Material(Material.B_PUYO, "b.ppm"),
        Material(Material.OJAMA, "o.ppm"),
    ]
    # 辞書に変換して返却
    item_dict = {}
    for item in item_list:
        item_dict[item.id] = item.image
    return item_dict


def get_color_list():
    color_list = [
        "black",  # Material.BLANK
        "brown",  # Material.WALL
        "red",  # Material.R_PUYO
        "yellow",  # Material.Y_PUYO
        "green",  # Material.G_PUYO
        "purple",  # Material.P_PUYO
        "blue",  # Material.B_PUYO
        "white",  # Material.OJAMA
    ]
    return color_list

if __name__ == "__main__":
    test_root = tk.Tk()
    test_item_dict = init_items()
    for image in test_item_dict.values():
        label = tk.Label(image=image)
        label.pack()

    test_root.mainloop()
