from dataclasses import dataclass

import numpy as np

from . import constant as const


@dataclass
class Item:
    index: int
    length: int
    width: int
    height: int
    quantity: int
    rotation: int
    x: int
    y: int
    z: int
    axis_lock: int

    @classmethod
    def from_numpy_array(cls, np_item):
        return cls(
            np_item[const.ITEM_INDEX],
            np_item[const.ITEM_LENGTH],
            np_item[const.ITEM_WIDTH],
            np_item[const.ITEM_HEIGHT],
            np_item[const.ITEM_QUANTITY],
            np_item[const.ITEM_ROTATION],
            np_item[const.ITEM_X],
            np_item[const.ITEM_Y],
            np_item[const.ITEM_Z],
            np_item[const.ITEM_AXIS_LOCK],
        )

    @classmethod
    def from_dict(cls, b):
        return cls(
            b["index"],
            b["length"],
            b["width"],
            b["height"],
            b["quantity"],
            0,
            0,
            0,
            0,
            b["axis_lock"]
        )

    def to_dict(self):
        return {
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "quantity": self.quantity,
            "index": self.index,
            "axis_lock": self.axis_lock,
        }

    @property
    def item_in_numpy(self):
        return np.array(
            [
                self.length,
                self.width,
                self.height,
                self.quantity,
                self.rotation,
                self.x,
                self.y,
                self.z,
                self.index,
                self.axis_lock,
            ],
            np.int_,
        )
