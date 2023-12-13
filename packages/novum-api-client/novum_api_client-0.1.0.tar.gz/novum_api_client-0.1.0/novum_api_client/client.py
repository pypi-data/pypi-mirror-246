# pylint: disable=C0115
# pylint: disable=C0116
# flake8: noqa

import json
from typing import Optional, List
import requests
from dataclasses import dataclass
from .base_client import BaseAPIClient, NovumAPIError
from .api_type import (
    TAPIInfoEssentials,
    TBattery,
    TBatteryType,
    TCapacityMeasurement,
    TDataset,
    TDeviceMeasurement,
    TUser,
    TDatasetEssentials,
    TBatteryEssentials,
    TBatteryTypeEssentials,
    TCapacityMeasurementEssentials,
    TVersionEssentials,
)

PRODUCTION_API_HOST: str = "https://novum-batteries.com"


@dataclass
class NovumAPIClient(BaseAPIClient):
    def __init__(self, user=None, host=PRODUCTION_API_HOST):
        super().__init__(user, host)

    # ********************************************************
    # Section for the Service Center info
    # ********************************************************

    def ping(self) -> dict:
        return self._get_json("/api/batman/v1/")

    def get_info(self) -> TAPIInfoEssentials:
        info = self._get_json("/api/batman/v1/info")
        return TAPIInfoEssentials(**info)

    def get_version(self) -> TVersionEssentials:
        version = self._get_json("/api/batman/v1/version")
        return TVersionEssentials(**version)

    # ********************************************************
    # Section for the users
    # ********************************************************

    def login(
        self, email: str, password: str, store_user=True, timeout: float = 4
    ) -> TUser | None:
        header = {"authorization": "auth", "content-type": "application/json"}
        payload = {"username": email, "password": password}
        response = requests.post(
            self.host + "/api/batman/v1/login",
            data=json.dumps(payload),
            headers=header,
            timeout=timeout,
        )
        if response.status_code == requests.codes.get("ok"):
            if store_user is True:
                user = response.json()
                self.user = TUser(**user)
                self._install_token_refresh_procedure()
                self.headers = dict(
                    {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + str(self.user.jwt),
                    }
                )

            return self.user

        else:
            raise NovumAPIError(response.text, response.status_code)

    def logout(self):
        return self._get_json("/api/batman/v1/logout")

    def check_current_user_still_authenticated(self) -> dict:
        return self._get_json("/api/batman/v1/check_token")

    # ********************************************************
    # Section for the Battery Types
    # ********************************************************

    def get_battery_types(
        self,
        filter_types: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryType]:
        battery_types_list = self._get_json(
            "/api/batman/v1/batteryTypes",
            filter_json=filter_types,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        battery_types = [
            TBatteryType(**battery_type) for battery_type in battery_types_list
        ]

        return battery_types

    def get_battery_types_count(
        self,
        filter_types: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        return self._get_json(
            "/api/batman/v1/batteryTypes/count",
            filter_json=filter_types,
            option=option,
            fields=fields,
            timeout=timeout,
        )

    def get_battery_types_by_id(
        self, battery_type_id: str, timeout: float = 4.0
    ) -> TBatteryType:
        battery_type = self._get_json(
            f"/api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout
        )
        return TBatteryType(**battery_type)

    def remove_battery_types_by_id(self, battery_type_id: str, timeout: float = 4.0):
        self._delete_json(
            f"/api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout
        )
        return "The battery type was removed."

    def create_battery_type(
        self,
        battery_type: TBatteryTypeEssentials,
        timeout: float = 4.0,
    ) -> TBatteryType:
        created_battery_type = self._post_json(
            "/api/batman/v1/batteryTypes", input_data=battery_type, timeout=timeout
        )
        return TBatteryType(**created_battery_type)

    def update_battery_type_by_id(
        self,
        battery_type_id: str,
        battery_type_update: TBatteryTypeEssentials,
        timeout: float = 4.0,
    ) -> TBatteryType:
        updated_battery_type = self._put_json(
            f"/api/batman/v1/batteryTypes/{battery_type_id}",
            input_data=battery_type_update,
            timeout=timeout,
        )
        return TBatteryType(**updated_battery_type)

    # ********************************************************
    # Section for the Datasets
    # ********************************************************

    def dataset_exists_on_remote(self, dataset_id: str, timeout: float = 4.0) -> bool:
        response = self._get_json(
            f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout
        )
        try:
            if len(response["measured"]["measurement_cycles"]) != 0:
                return True
            else:
                return False
        except KeyError:
            return False

    def create_dataset(
        self, dataset: TDatasetEssentials, timeout: float = 4.0
    ) -> TDataset:
        created_dataset = self._post_json(
            "/api/batman/v1/datasets", input_data=dataset, timeout=timeout
        )
        return TDataset(**created_dataset)

    def get_dataset_by_id(self, dataset_id: str, timeout: float = 4.0) -> TDataset:
        dataset = self._get_json(
            f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout
        )
        return TDataset(**dataset)

    def get_datasets(
        self,
        filter_datasets: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TDataset]:
        dataset_list = self._get_json(
            "/api/batman/v1/datasets",
            filter_json=filter_datasets,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        datasets = [TDataset(**dataset) for dataset in dataset_list]

        return datasets

    def get_datasets_count(
        self,
        filter_datasets: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        return self._get_json(
            "/api/batman/v1/datasets/count",
            filter_json=filter_datasets,
            option=option,
            fields=fields,
            timeout=timeout,
        )

    def get_datasets_count_by_battery(
        self,
        battery: TBattery,
        filter_datasets: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        filter_with_id = {"meta.battery._id": battery.id}
        if filter_datasets is not None:
            filter_with_id.update(filter_datasets)
        response = self._get_json(
            "/api/batman/v1/datasets/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response

    def update_dataset_by_id(
        self, dataset_id: str, dataset: TDatasetEssentials, timeout: float = 4.0
    ) -> TDataset:
        updated_dataset = self._put_json(
            f"/api/batman/v1/datasets/{dataset_id}",
            input_data=dataset,
            timeout=timeout,
        )
        return TDataset(**updated_dataset)

    def remove_dataset_by_id(self, dataset_id: str, timeout: float = 4.0):
        self._delete_json(f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return "The data set was removed."

    # ********************************************************
    # Section for the Battery
    # ********************************************************

    def create_battery(
        self, battery: TBatteryEssentials, timeout: float = 4.0
    ) -> TBattery:
        created_battery = self._post_json(
            "/api/batman/v1/batteries", input_data=battery, timeout=timeout
        )
        return TBattery(**created_battery)

    def get_battery_by_id(self, battery_id: str, timeout: float = 4.0) -> TBattery:
        battery = self._get_json(
            f"/api/batman/v1/batteries/{battery_id}", timeout=timeout
        )

        return TBattery(**battery)

    def update_battery(self, battery: TBattery, timeout: float = 4.0) -> TBattery:
        updated_battery = self._put_json(
            f"/api/batman/v1/batteries/{battery.id}",
            input_data=battery,
            timeout=timeout,
        )

        return TBattery(**updated_battery)

    def update_battery_by_id(
        self, battery_id: str, battery_update: TBatteryEssentials, timeout: float = 4.0
    ) -> TBattery:
        updated_battery = self._put_json(
            f"/api/batman/v1/batteries/{battery_id}",
            input_data=battery_update,
            timeout=timeout,
        )
        return TBattery(**updated_battery)

    def remove_battery_by_id(self, battery_id: str, timeout: float = 4.0) -> str:
        self._delete_json(f"/api/batman/v1/batteries/{battery_id}", timeout=timeout)
        return "The battery was removed."

    def get_batteries(
        self,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBattery]:
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_batteries,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBattery(**battery) for battery in battery_list]

        return batteries

    def get_batteries_count(
        self,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        return self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_batteries,
            option=option,
            fields=fields,
            timeout=timeout,
        )

    def get_children_of_battery_by_id(
        self,
        parent_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBattery]:
        filter_with_id = {"tree.parent": parent_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBattery(**battery) for battery in battery_list]

        return batteries

    def get_children_of_battery_by_id_count(
        self,
        parent_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        filter_with_id = {"tree.parent": parent_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        response = self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response

    def get_leaves_of_battery_by_id(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBattery]:
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBattery(**battery) for battery in battery_list]
        return batteries

    def get_leaves_of_battery_by_id_count(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBattery]:
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBattery(**battery) for battery in battery_list]
        return batteries

    def get_descendants_of_battery_by_id(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBattery]:
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBattery(**battery) for battery in battery_list]
        return batteries

    def get_descendants_of_battery_by_id_count(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBattery]:
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBattery(**battery) for battery in battery_list]
        return batteries

    # ********************************************************
    # Section for the CapacityMeasurement
    # ********************************************************

    def create_capacity_measurement(
        self, capacity_measurement: TCapacityMeasurementEssentials, timeout: float = 4.0
    ) -> TCapacityMeasurement:
        response = self._post_json(
            "/api/batman/v1/capacityMeasurements",
            input_data=capacity_measurement,
            timeout=timeout,
        )

        return TCapacityMeasurement(**response)

    def update_capacity_measurement_by_id(
        self,
        capacity_measurement_id: str,
        capacity_measurement: TCapacityMeasurementEssentials,
        timeout: float = 4.0,
    ) -> TCapacityMeasurement:
        updated_capacity_measurement = self._put_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            input_data=capacity_measurement,
            timeout=timeout,
        )
        return TCapacityMeasurement(**updated_capacity_measurement)

    def remove_capacity_measurement_by_id(
        self, capacity_measurement_id: str, timeout: float = 4.0
    ):
        self._delete_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            timeout=timeout,
        )
        return "Capacity measurement was removed."

    def get_capacity_measurement(
        self,
        filter_measurements: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TCapacityMeasurement]:
        capacity_measurement_list = self._get_json(
            "/api/batman/v1/capacityMeasurements",
            filter_json=filter_measurements,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        capacity_measurements = [
            TCapacityMeasurement(**capacity_measurement)
            for capacity_measurement in capacity_measurement_list
        ]

        return capacity_measurements

    def get_capacity_measurement_count(
        self,
        filter_measurements: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        response = self._get_json(
            "/api/batman/v1/capacityMeasurements/count",
            filter_json=filter_measurements,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response

    def get_capacity_measurement_by_id(
        self, capacity_measurement_id: str, timeout: float = 4.0
    ) -> TCapacityMeasurement:
        capacity_measurement = self._get_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            timeout=timeout,
        )
        return TCapacityMeasurement(**capacity_measurement)

    def get_capacity_measurements_count_by_battery(
        self, battery_id: str, timeout: float = 4.0
    ) -> dict:
        filter_by_id = {"battery._id": battery_id}
        response = self._get_json(
            "/api/batman/v1/capacityMeasurements/count",
            filter_json=filter_by_id,
            timeout=timeout,
        )
        return response

    def capacity_measurement_exists_on_remote(
        self, capacity_measurement_id: dict, timeout: float = 4.0
    ) -> bool:
        response = self._get_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            timeout=timeout,
        )
        return response["id"] == capacity_measurement_id

    # ********************************************************
    # Section for the Measurements
    # ********************************************************

    def get_latests_measurements(
        self, device_id: str, count: int = 1, timeout: float = 4.0
    ) -> dict:
        return self._get_json(
            f"/api/time-series/v1/devices/{device_id}/measurements/last/{count}",
            timeout=timeout,
        )

    def write_device_measurements(
        self, device_measurements: List[TDeviceMeasurement], timeout: float = 4.0
    ) -> dict:
        return self._post_json(
            "/api/time-series/v1/measurements",
            input_data=device_measurements,
            timeout=timeout,
        )

    def read_device_measurements(
        self,
        device_filter: Optional[dict],
        option=None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        return self._get_json(
            "/api/time-series/v1/measurements",
            filter_json=device_filter,
            option=option,
            fields=fields,
            timeout=timeout,
        )

    def read_device_measurements_by_id(
        self,
        battery_id,
        device_filter: Optional[dict],
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        return self._get_json(
            f"/api/time-series/v1/measurements/{battery_id}",
            filter_json=device_filter,
            fields=fields,
            timeout=timeout,
        )

    # ********************************************************
    # Section for the Reports
    # ********************************************************

    def create_report(self, report, headers=None, timeout: float = 4.0):
        return self._post_json(
            "/api/batman/v1/reports", report, headers, timeout=timeout
        )

    def update_report_by_id(
        self, report_id: str, report, headers=None, timeout: float = 4
    ):
        return self._put_json(
            f"/api/batman/v1/reports/{report_id}", report, headers, timeout=timeout
        )

    def get_reports(
        self,
        report_filter=None,
        option=None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ):
        response = self._get_json(
            "/api/batman/v1/reports",
            filter_json=report_filter,
            fields=fields,
            option=option,
            timeout=timeout,
        )
        return response

    def get_reports_count(
        self,
        report_filter=None,
        option=None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ):
        response = self._get_json(
            "/api/batman/v1/reports/count",
            report_filter,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response

    def get_reports_count_by_battery(self, battery: TBattery, timeout: float = 4):
        response = self._get_json(
            "/api/batman/v1/reports/count",
            filter_json={"origin_id": battery.id},
            timeout=timeout,
        )

        return response

    def get_report_by_id(self, report_id: str, timeout: float = 4) -> dict:
        return self._get_json(f"/api/batman/v1/reports/{report_id}", timeout=timeout)

    def get_reports_by_origin_id(
        self,
        origin_id: str,
        report_filter: Optional[dict] = None,
        option=None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ) -> dict:
        return self._get_json(
            f"/api/batman/v1/reports/byOriginId/{origin_id}",
            report_filter,
            option,
            fields=fields,
            timeout=timeout,
        )

    def get_reports_by_origin_id_count(
        self,
        origin_id: str,
        report_filter: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ) -> dict:
        return self._get_json(
            f"/api/batman/v1/reports/byOriginId/{origin_id}/count",
            report_filter,
            option,
            fields=fields,
            timeout=timeout,
        )

    def remove_report_by_id(
        self, report_id: str, report_filter=None, option=None, timeout: float = 4
    ):
        response = self._delete_json(
            f"/api/batman/v1/reports/{report_id}",
            filter_json=report_filter,
            option=option,
            timeout=timeout,
        )
        return response
