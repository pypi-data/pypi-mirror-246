# -*- coding: utf-8 -*-
"""
@Time : 2023/12/16 23:00
@Author : sdb20200101@gmail.com
@File: PointRoi.py
@Software : PyCharm
"""
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from .constant import keyMoveFactor


class PointRoi:
    def __init__(self, scale_factor, index=0):
        super().__init__()
        self.point = [-1, -1]
        self._scale_factor = scale_factor
        self.line1 = QGraphicsLineItem()
        self.line2 = QGraphicsLineItem()
        self.line3 = QGraphicsLineItem()
        self.line4 = QGraphicsLineItem()
        self.lines = [self.line1, self.line2, self.line3, self.line4]
        self.point_rect = QGraphicsRectItem()
        self.index = index
        self.text = QGraphicsTextItem()
        # self.text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)

        self.rect_brush = QBrush(Qt.GlobalColor.yellow)
        self.rect_pen = QPen(Qt.GlobalColor.black)
        self.rect_pen.setWidthF(1 / self._scale_factor)

        self.line_pen = QPen(Qt.GlobalColor.yellow)
        self.line_pen.setWidthF(1 / self._scale_factor)

        for line in self.lines:
            line.setPen(self.line_pen)

        self.point_rect.setPen(self.rect_pen)
        self.point_rect.setBrush(self.rect_brush)

    @property
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value
        self.rect_pen.setWidthF(1 / self._scale_factor)
        self.line_pen.setWidthF(1 / self._scale_factor)

        for line in self.lines:
            line.setPen(self.line_pen)

        self.update_point()

        self.point_rect.setPen(self.rect_pen)

    def set_handles(self):
        pass

    def show_text(self):
        self.text.setPlainText(str(self.index + 1))

    def update_point(self):
        point_rect_width = 1 / self._scale_factor * 8

        self.point_rect.setRect(
            QRectF(self.point[0] - point_rect_width / 2, self.point[1] - point_rect_width / 2, point_rect_width,
                   point_rect_width))

        self.line1.setLine(self.point[0] - 1.5 * point_rect_width, self.point[1],
                           self.point[0] - 0.5 * point_rect_width, self.point[1])
        self.line2.setLine(self.point[0] + 0.5 * point_rect_width, self.point[1],
                           self.point[0] + 1.5 * point_rect_width, self.point[1])
        self.line3.setLine(self.point[0], self.point[1] - 1.5 * point_rect_width, self.point[0],
                           self.point[1] - 0.5 * point_rect_width)
        self.line4.setLine(self.point[0], self.point[1] + 0.5 * point_rect_width, self.point[0],
                           self.point[1] + 1.5 * point_rect_width)

        self.text.setPos(self.point[0] + point_rect_width, self.point[1] + point_rect_width)

        font = self.text.font()
        font.setPointSizeF(16 / self._scale_factor)
        self.text.setFont(font)

    def add_to_scene(self, scene: QGraphicsScene):
        scene.addItem(self.point_rect)
        scene.addItem(self.text)
        for line in self.lines:
            scene.addItem(line)

    def clear_from_scene(self, scene: QGraphicsScene):
        scene.removeItem(self.point_rect)
        scene.removeItem(self.text)
        for line in self.lines:
            scene.removeItem(line)

    def setROI(self, x: float, y: float):
        self.point = [x, y]
        if self.index == 0 and self.text.toPlainText() == '':
            self.text.setPlainText('')
        else:
            self.text.setPlainText(str(self.index + 1))
        self.text.setDefaultTextColor(Qt.GlobalColor.yellow)
        self.update_point()

    def is_in_roi(self, pos: QPointF):
        point_rect_width = 1 / self._scale_factor * 8
        rect = QRectF(self.point_rect.rect().x() - point_rect_width, self.point_rect.rect().y() - point_rect_width,
                      3 * point_rect_width, 3 * point_rect_width)
        if rect.contains(pos):
            return self.index + 1

        return None

    def move_roi(self, pos: QPointF):
        self.setROI(pos.x(), pos.y())

    def keyMove(self, event: QKeyEvent):
        d = 1 / self._scale_factor * keyMoveFactor
        x = self.point[0]
        y = self.point[1]
        if event.key() == Qt.Key.Key_Up:
            self.setROI(x, y - d)
        elif event.key() == Qt.Key.Key_Down:
            self.setROI(x, y + d)
        elif event.key() == Qt.Key.Key_Left:
            self.setROI(x - d, y)
        elif event.key() == Qt.Key.Key_Right:
            self.setROI(x + d, y)
