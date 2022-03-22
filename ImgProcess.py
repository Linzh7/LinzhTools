from collections import namedtuple
from ImgDatasetProcess import *

gts_gray_path = r'.\train_gray'
gts_color_path = r'.\train_rgb'

Cls = namedtuple('cls', ['name', 'id', 'color'])
CLASS_NUM = 13
Classes = [
    Cls('void', 0, (0, 0, 0)),
    Cls('s_w_d', 1, (70, 130, 180)),
    Cls('s_y_d', 1, (220, 20, 60)),
    Cls('ds_w_dn', 1, (128, 0, 128)),
    Cls('ds_y_dn', 1, (255, 0, 0)),
    Cls('sb_w_do', 1, (0, 0, 60)),
    Cls('sb_y_do', 1, (0, 60, 100)),
    Cls('b_w_g', 2, (0, 0, 142)),
    Cls('b_y_g', 2, (119, 11, 32)),
    Cls('db_w_g', 2, (244, 35, 232)),
    Cls('db_y_g', 2, (0, 0, 160)),
    Cls('db_w_s', 3, (153, 153, 153)),
    Cls('s_w_s', 3, (220, 220, 0)),
    Cls('ds_w_s', 3, (250, 170, 30)),
    Cls('s_w_c', 4, (102, 102, 156)),
    Cls('s_y_c', 4, (128, 0, 0)),
    Cls('s_w_p', 5, (128, 64, 128)),
    Cls('s_n_p', 5, (238, 232, 170)),
    Cls('c_wy_z', 6, (190, 153, 153)),
    Cls('a_w_u', 7, (0, 0, 230)),
    Cls('a_w_t', 7, (128, 128, 0)),
    Cls('a_w_tl', 7, (128, 78, 160)),
    Cls('a_w_tr', 7, (150, 100, 100)),
    Cls('a_w_tlr', 7, (255, 165, 0)),
    Cls('a_w_l', 7, (180, 165, 180)),
    Cls('a_w_r', 7, (107, 142, 35)),
    Cls('a_w_lr', 7, (201, 255, 229)),
    Cls('a_n_lu', 7, (0, 191, 255)),
    Cls('a_w_tu', 7, (51, 255, 51)),
    Cls('a_w_m', 7, (250, 128, 114)),
    Cls('a_y_t', 7, (127, 255, 0)),
    Cls('b_n_sr', 8, (255, 128, 0)),
    Cls('d_wy_za', 9, (0, 255, 255)),
    Cls('r_wy_np', 10, (178, 132, 190)),
    Cls('vom_wy_n', 11, (128, 128, 64)),
    Cls('om_n_n', 11, (102, 0, 204)),
    Cls('noise', 12, (0, 153, 153)),
    Cls('ignored', 12, (255, 255, 255))
]


if __name__ == '__main__':
    pass
    color_dict = revers_dic()
    # gray_color(color_dict)
    # color_gray(color_dict)
    # for i in range(CLASS_NUM):
    #     os.mkdir(f'{gts_gray_path}{i}')
    color2Binary(color_dict)
    # color_fakeColor(color_dict)
