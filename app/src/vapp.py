import json
import logging

from vehicle import Vehicle  # type: ignore
from velocitas_sdk.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from velocitas_sdk.vdb.reply import DataPointReply
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
        await self.Vehicle.Cabin.Seat.Row1.Pos1.Position.subscribe(
            self.on_seat_position_changed
        )

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
            await self.Vehicle.Body.Trunk.Rear.IsOpen.set(new_status)
            response_data["result"] = {"status": new_status}
        except Exception:
            response_data["result"] = {"status": "error"}

        await self.publish_event(response_topic, json.dumps(response_data))

    async def on_seat_position_changed(self, data: DataPointReply):
        response_topic = "seatadjuster/currentPosition"
        await self.publish_event(
            response_topic,
            json.dumps(
                {"position": data.get(self.Vehicle.Cabin.Seat.Row1.Pos1.Position).value}
            ),
        )

    @subscribe_topic("seatadjuster/setPosition/request")
    async def on_set_position_request_received(self, data_str: str) -> None:
        logger.info(f"Got message: {data_str!r}")
        data = json.loads(data_str)
        response_topic = "seatadjuster/setPosition/response"
        response_data = {"requestId": data["requestId"], "result": {}}

        vehicle_speed = (await self.Vehicle.Speed.get()).value

        position = data["position"]
        if vehicle_speed == 0:
            try:
                await self.Vehicle.Cabin.Seat.Row1.Pos1.Position.set(position)
                response_data["result"] = {
                    "status": 0,
                    "message": f"Set Seat position to: {position}",
                }
            except ValueError as error:
                response_data["result"] = {
                    "status": 1,
                    "message": f"Failed to set the position {position}, error: {error}",
                }
            except Exception:
                response_data["result"] = {
                    "status": 1,
                    "message": "Exception on set Seat position",
                }

        else:
            error_msg = f"""Not allowed to move seat because vehicle speed
                is {vehicle_speed} and not 0"""
            response_data["result"] = {"status": 1, "message": error_msg}

        await self.publish_event(response_topic, json.dumps(response_data))
