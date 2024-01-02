from my_vehicle_model.my_vehicle_model.Trunk import Trunk
from velocitas_sdk.model import Model


class Body(Model):
    def __init__(self, parent):
        super().__init__(parent)
        self.Trunk = Trunk(self)
