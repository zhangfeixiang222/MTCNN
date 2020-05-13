import numpy as np


# 计算iou，用两个框的交集除以 并集或最小集
def iou(box, boxes, isMin=False):
    area = (box[2] - box[0]) * (box[3] - box[1])
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    # 交集的左上角取两个框大的值，右下角取两个款小的值
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])
    # 求交集的边长，最短为0
    w = np.maximum(0, x2 - x1)
    h = np.maximum(0, y2 - y1)
    inter = w * h

    if isMin:
        return np.divide(inter, np.minimum(area, areas))
    else:
        return np.divide(inter, area + areas - inter)


# 非极大值抑制，iou大于阈值的框看作重复框去除，留下iou小的框，可能是另一个人脸
def nms(boxes, thresh=0.3, isMin=False):
    if boxes.shape[0] == 0:
        return np.array([])
    # 将框根据置信度从大到小排序
    _boxes = boxes[(-boxes[:, 4]).argsort()]
    r_box = []
    # 计算iou，留下iou值小的框
    while _boxes.shape[0] > 1:
        a_box = _boxes[0]
        b_boxes = _boxes[1:]
        r_box.append(a_box)
        index = np.where(iou(a_box, b_boxes, isMin) < thresh)
        _boxes = b_boxes[index]

    if _boxes.shape[0] > 0:
        r_box.append(_boxes[0])

    return np.stack(r_box)


# 扩充成正方形
def convert_to_square(boxes):
    if boxes.shape[0] == 0:
        return np.array([])
    square_boxes = boxes.copy()
    w = boxes[:, 2] - boxes[:, 0]
    h = boxes[:, 3] - boxes[:, 1]
    max_side = np.maximum(w, h)
    square_boxes[:, 0] = boxes[:, 0] + w / 2 - max_side / 2
    square_boxes[:, 1] = boxes[:, 1] + h / 2 - max_side / 2
    square_boxes[:, 2] = square_boxes[:, 0] + max_side
    square_boxes[:, 3] = square_boxes[:, 1] + max_side
    return square_boxes


if __name__ == '__main__':
    a = np.array([1, 1, 10, 10, 0.98])
    bs = np.array([[1, 1, 9, 9, 0.8], [9, 8, 13, 20, 0.7], [6, 11, 18, 17, 0.85]])
    print(iou(a, bs))

    bs = np.array([[1, 1, 10, 10, 0.98], [1, 1, 9, 9, 0.8], [9, 8, 13, 20, 0.7], [6, 11, 18, 17, 0.85]])
    print((-bs[:, 4]).argsort())
    print(nms(bs))
    c = np.array([[1, 1, 9, 3]])
    print(convert_to_square(c))
