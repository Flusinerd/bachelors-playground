import json
import logging

from my_vehicle_model.my_vehicle_model.vehicle import Vehicle
from velocitas_sdk.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from velocitas_sdk.vehicle_app import VehicleApp, subscribe_topic

logging.setLogRecordFactory(get_opentelemetry_log_factory())
logging.basicConfig(format=get_opentelemetry_log_format())
logging.getLogger().setLevel("DEBUG")
logger = logging.getLogger(__name__)


class VehicleOwnerApp(VehicleApp):
    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client

    async def on_start(self):
        """Run when the vehicle app starts"""
        pass

    @subscribe_topic("app/trunk/getStatus/request")
    async def on_trunk_status_request_received(self, data_str: str) -> None:
        logger.info("Got trunk status request")
        response_topic = "app/trunk/getStatus/response"
        response_data = {"result": {}}  # type: ignore

        trunk_status = (await self.Vehicle.Body.Trunk.Rear.IsOpen.get()).value

        response_data["result"] = {"status": trunk_status}

        await self.publish_event(response_topic, json.dumps(response_data))

    @subscribe_topic("app/trunk/setStatus/request")
    async def on_trunk_status_set_request_received(self, data_str: str) -> None:
        logger.info("Got trunk status set request")
        data = json.loads(data_str)
        response_topic = "app/trunk/setStatus/response"
        response_data = {"result": {}}  # type: ignore

        new_status = data["status"]
        try:
            await self.Vehicle.Body.Trunk.RearTrunk.IsOpen.set(new_status)
            response_data["result"] = {"status": new_status}
        except Exception:
            response_data["result"] = {"status": "error"}

        await self.publish_event(response_topic, json.dumps(response_data))
