import os
import sys
import time
import cv2
import numpy as np

import LinzhUtil

# 类别信息


def gray2Color(color_dict, gray_path, color_path):
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
        processShow(index+1, len(gt_list))
    print(time.time()-t1)


def color2Gray(color_dict, color_path, gray_path, ):
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
        processShow(index + 1, len(gt_list))
    print(time.time() - t1)


def color2FakeColor(color_dict, color_path, gray_path, ):
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
        processShow(index + 1, len(gt_list))
    print(time.time() - t1)


def color2Binary(color_dict, color_path, gray_path, ):
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
        processShow(index + 1, len(gt_list))
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


def nt_dic(nt):
    '''
    swift nametuple to color dict
    :param nt: nametuple
    :return:
    '''
    color_dict = {}
    for cls in nt:
        color_dict[cls.id] = cls.color
    return color_dict


def revers_dic(nt):
    '''
    swift nametuple to color dict
    :param nt: nametuple
    :return:
    '''
    color_dict = {}
    for cls in nt:
        color_dict[cls.color] = cls.id
    return color_dict


def processShow(num, nums, pre_fix='', suf_fix=''):
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
