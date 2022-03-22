import os
import sys
import time
import cv2
import numpy as np
from collections import namedtuple


import LinzhUtil

# 类别信息

gts_gray_path = '.\\datasets\\apollo\\y_train\\'  # y_train_rgb
gts_color_path = '.\\datasets\\apollo\\y_train_rgb\\'

Cls = namedtuple('cls', ['name', 'id', 'color'])
CLASS_NUM = 13
Clss = [
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


def gray2Color(color_dict, gray_path=gts_gray_path, color_path=gts_color_path):
    '''
    swift gray image to color, by color mapping relationship
    :param color_dict:color mapping relationship, dict format
    :param gray_path:gray imgs path
    :param color_path:color imgs path
    :return:
    '''
    pass
    t1 = time.time()
    gt_list = LinzhUtil.getFileList(color_path)
    for index, gt_name in enumerate(gt_list):
        gt_gray_path = os.path.join(gray_path, gt_name)
        gt_color_path = os.path.join(color_path, gt_name)
        gt_gray = cv2.imread(gt_gray_path, cv2.IMREAD_GRAYSCALE)
        assert len(gt_gray.shape) == 2                          # make sure gt_gray is 1band

        # # region method 1: swift by pix, slow
        # gt_color = np.zeros((gt_gray.shape[0],gt_gray.shape[1],3),np.uint8)
        # for i in range(gt_gray.shape[0]):
        #     for j in range(gt_gray.shape[1]):
        #         gt_color[i][j] = color_dict[gt_gray[i][j]]      # gray to color
        # # endregion

        # region method 2: swift by array
        # gt_color = np.array(np.vectorize(color_dict.get)(gt_gray),np.uint8).transpose(1,2,0)
        # endregion

        # region method 3: swift by matrix, fast
        gt_color = matrix_mapping(color_dict, gt_gray)
        # endregion

        gt_color = cv2.cvtColor(gt_color, cv2.COLOR_RGB2BGR)
        cv2.imwrite(gt_color_path, gt_color,)
        process_show(index+1, len(gt_list))
    print(time.time()-t1)


def color2Gray(color_dict, color_path=gts_color_path, gray_path=gts_gray_path, ):
    '''
    swift color image to gray, by color mapping relationship
    :param color_dict:color mapping relationship, dict format
    :param gray_path:gray imgs path
    :param color_path:color imgs path
    :return:
    '''
    gray_dict = {}
    for k, v in color_dict.items():
        gray_dict[v] = k
    t1 = time.time()
    gt_list = os.listdir(color_path)
    for index, gt_name in enumerate(gt_list):
        gt_gray_path = os.path.join(gray_path, gt_name)
        gt_color_path = os.path.join(color_path, gt_name)
        color_array = cv2.imread(gt_color_path, cv2.IMREAD_COLOR)
        assert len(color_array.shape) == 3

        gt_gray = np.zeros((color_array.shape[0], color_array.shape[1]), np.uint8)
        b, g, r = cv2.split(color_array)
        color_array = np.array([r, g, b])
        for cls_color, cls_index in gray_dict.items():
            cls_pos = arrays_jd(color_array, cls_color)
            gt_gray[cls_pos] = cls_index

        cv2.imwrite(gt_gray_path, gt_gray)
        process_show(index + 1, len(gt_list))
    print(time.time() - t1)


def color2FakeColor(color_dict, color_path=gts_color_path, gray_path=gts_gray_path, ):
    '''
    swift color image to blue channal, by color mapping relationship
    :param color_dict:color mapping relationship, dict format
    :param gray_path:gray imgs path
    :param color_path:color imgs path
    :return:
    '''
    gray_dict = {}
    for k, v in color_dict.items():
        gray_dict[v] = k
    t1 = time.time()
    gt_list = os.listdir(color_path)
    for index, gt_name in enumerate(gt_list):
        gt_gray_path = os.path.join(gray_path, gt_name)
        gt_color_path = os.path.join(color_path, gt_name)
        color_array = cv2.imread(gt_color_path, cv2.IMREAD_COLOR)
        assert len(color_array.shape) == 3

        gt_gray = np.zeros(color_array.shape, np.uint8)
        b, g, r = cv2.split(color_array)
        color_array = np.array([r, g, b])
        for cls_color, cls_index in gray_dict.items():
            cls_pos = arrays_jd(color_array, cls_color)
            gt_gray[cls_pos] = cls_index

        cv2.imwrite(gt_gray_path, gt_gray)
        process_show(index + 1, len(gt_list))
    print(time.time() - t1)


def color2Binary(color_dict, color_path=gts_color_path, gray_path=gts_gray_path, ):
    '''
    swift color image to bin, by color mapping relationship
    :param color_dict:color mapping relationship, dict format
    :param gray_path:gray imgs path
    :param color_path:color imgs path
    :return:
    '''
    '''
    swift color image to gray, by color mapping relationship
    :param color_dict:color mapping relationship, dict format
    :param gray_path:gray imgs path
    :param color_path:color imgs path
    :return:
    '''
    gray_dict = {}
    for k, v in color_dict.items():
        gray_dict[k] = v
    t1 = time.time()
    gt_list = os.listdir(color_path)
    for index, gt_name in enumerate(gt_list):
        gt_color_path = os.path.join(color_path, gt_name)
        color_array = cv2.imread(gt_color_path, cv2.IMREAD_COLOR)
        assert len(color_array.shape) == 3

        b, g, r = cv2.split(color_array)
        color_array = np.array([r, g, b])
        lastClassIndex = -1
        for cls_color, cls_index in gray_dict.items():
            # print(f'{cls_color}, {cls_index}')
            if cls_index != lastClassIndex:
                # print(f"Update {lastClassIndex} into {cls_index}")
                gt_gray = np.zeros((color_array.shape[1], color_array.shape[2]), np.uint8)
                lastClassIndex = cls_index
            cls_pos = arrays_jd(color_array, cls_color)

            gt_gray[cls_pos] = 255
            gt_gray_path = os.path.join(gray_path, str(cls_index), gt_name)
            cv2.imwrite(gt_gray_path, gt_gray)
        process_show(index + 1, len(gt_list))
        # break
    print(time.time() - t1)


def arrays_jd(arrays, cond_nums):
    r = arrays[0] == cond_nums[0]
    g = arrays[1] == cond_nums[1]
    b = arrays[2] == cond_nums[2]
    return r & g & b


def matrix_mapping(color_dict, gt):
    colorize = np.zeros([len(color_dict), 3], 'uint8')
    for cls, color in color_dict.items():
        colorize[cls, :] = list(color)
    ims = colorize[gt, :]
    ims = ims.reshape([gt.shape[0], gt.shape[1], 3])
    return ims


def nt_dic(nt=Clss):
    '''
    swift nametuple to color dict
    :param nt: nametuple
    :return:
    '''
    color_dict = {}
    for cls in nt:
        color_dict[cls.id] = cls.color
    return color_dict


def revers_dic(nt=Clss):
    '''
    swift nametuple to color dict
    :param nt: nametuple
    :return:
    '''
    color_dict = {}
    for cls in nt:
        color_dict[cls.color] = cls.id
    return color_dict


def process_show(num, nums, pre_fix='', suf_fix=''):
    '''
    auxiliary function, print work progress
    :param num:
    :param nums:
    :param pre_fix:
    :param suf_fix:
    :return:
    '''
    rate = num / nums
    ratenum = round(rate, 3) * 100
    bar = '\r%s %g/%g [%s%s]%.1f%% %s' % \
        (pre_fix, num, nums, '#' * (int(ratenum) // 5), '_' * (20 - (int(ratenum) // 5)), ratenum, suf_fix)
    sys.stdout.write(bar)
    sys.stdout.flush()


if __name__ == '__main__':
    pass
    color_dict = revers_dic()
    # gray_color(color_dict)
    # color_gray(color_dict)
    # for i in range(CLASS_NUM):
    #     os.mkdir(f'{gts_gray_path}{i}')
    color2Binary(color_dict)
    # color_fakeColor(color_dict)
