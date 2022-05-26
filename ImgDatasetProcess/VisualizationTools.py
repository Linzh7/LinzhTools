import cv2
# import matplotlib.pyplot as plt
# from PIL import Image
# import matplotlib.patches as patches

# rec in recList should be: [(point_1_X, point_1_Y), (point_2_X, point_2_Y), (color_b, color_g, color_r), lineWidth]


def drawBoxesWithOpenCV(image, recList):
    for rec in recList:
        image = cv2.rectangle(image, rec[0], rec[1], rec[2], rec[3])
    return image


def drawBoxesWithMatplot(image, recList):
    pass
