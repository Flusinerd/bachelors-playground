from my_vehicle_model.my_vehicle_model.Body import Body
from velocitas_sdk.model import Model


class Vehicle(Model):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.Body = Body(self)


vehicle = Vehicle("Vehicle")
