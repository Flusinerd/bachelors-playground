from my_vehicle_model.my_vehicle_model.proto.trunk_pb2 import OpenRequest
from my_vehicle_model.my_vehicle_model.proto.trunk_pb2_grpc import RearTrunkStub
from velocitas_sdk.model import Service


class RearTrunkService(Service):
    def __init__(self):
        super().__init__()
        self._stub = RearTrunkStub(self.channel)

    async def SetIsOpen(self, is_open: bool):
        response = await self._stub.SetOpenStatus(
            OpenRequest(is_open=is_open), self.metadata
        )
        return response
