# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=W0105
# flake8: noqa


from datetime import datetime
import json
import pytest

from ..base_client import NovumAPIError
from ..client import NovumAPIClient
from ..api_type import (
    TAnalysis,
    TBattery,
    TBatteryEssentials,
    TBatteryType,
    TBatteryTypeEssentials,
    TCapacityMeasurement,
    TCapacityMeasurementEssentials,
    TChargeCycle,
    TChargeTypes,
    TDataset,
    TDatasetEssentials,
    TDatasetMeta,
    TDeviceMetaParticle,
    TEISSetup,
    TMeasured,
    TMeasurementCycle,
    TTimedMeasure,
    TUser,
    TAPIInfoEssentials,
    TVersion,
    TVersionEssentials,
)


class TestNovumAPIClient:
    @pytest.fixture(scope="class")
    def unauthenticated_api_client(self):
        api_client = NovumAPIClient()
        yield api_client

    @pytest.fixture(scope="class")
    def ada_logged_client(self):
        client = NovumAPIClient()
        client.login(
            email="ada.lovelace@novum-engineering.com", password="5TkbQuVEx4v2GVqJ"
        )
        yield client

    def test_ping(self, unauthenticated_api_client: NovumAPIClient):
        response = unauthenticated_api_client.ping()

        assert (
            response["message"]
            == "Hello user this is the Novum batman API server. All routes begin with /api/{api_type}/{api_version}/{resource}. You have to identify using your credentials and /api/batman/v1/login to obtain a token"
        )

    def test_get_info(self, unauthenticated_api_client: NovumAPIClient):
        info = unauthenticated_api_client.get_info()

        assert isinstance(info, TAPIInfoEssentials)
        assert info.name == "Novum Base API"
        assert info.dbName == "batman"

    def test_get_version(self, unauthenticated_api_client: NovumAPIClient):
        version = unauthenticated_api_client.get_version()

        assert isinstance(version, TVersionEssentials)
        assert version.name == "novum-api"
        assert version.branch == "master"

    def test_login_ada(self, unauthenticated_api_client: NovumAPIClient):
        response = unauthenticated_api_client.login(
            email="ada.lovelace@novum-engineering.com", password="5TkbQuVEx4v2GVqJ"
        )
        assert isinstance(response, TUser)
        assert "user" in response.roles

    def test_login_ada_with_wrong_credentials(
        self, unauthenticated_api_client: NovumAPIClient
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.login(
                email="ada.lovelace@novum-engineering.com", password="WrongPassword"
            )

        error_details = json.loads(str(excinfo.value))

        expected_error_message = "Wrong email or password."
        assert expected_error_message in error_details["details"]

    def test_check_current_user_still_authenticated(
        self, ada_logged_client: NovumAPIClient
    ):
        response = ada_logged_client.check_current_user_still_authenticated()
        assert response["authenticated"] is True

    def test_logout(self, ada_logged_client: NovumAPIClient):
        response = ada_logged_client.logout()
        assert response == {"message": "Logout successful"}

    # ********************************************************
    # Section for the Battery Type
    # ********************************************************

    @pytest.fixture
    def sample_battery_type(self):
        return TBatteryTypeEssentials(
            name="Test Battery Type",
            manufacturer="The Tester",
            nominal_voltage=3.7,
            nominal_capacity=2500,
        )

    @pytest.fixture
    def created_battery_type(
        self,
        ada_logged_client: NovumAPIClient,
        sample_battery_type: TBatteryTypeEssentials,
    ):
        response = ada_logged_client.create_battery_type(sample_battery_type)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_battery_types_by_id(response.id)

    def test_get_battery_type(
        self, ada_logged_client: NovumAPIClient, created_battery_type: TBatteryType
    ):
        response = ada_logged_client.get_battery_types()

        assert response[0].id == created_battery_type.id

    def test_get_battery_type_count(self, ada_logged_client: NovumAPIClient):
        response = ada_logged_client.get_battery_types_count()
        assert response == 5

    def test_get_battery_type_by_id(
        self, ada_logged_client: NovumAPIClient, created_battery_type: TBatteryType
    ):
        response = ada_logged_client.get_battery_types_by_id(created_battery_type.id)
        assert response.id == created_battery_type.id

    def test_create_battery_type(self, created_battery_type: TBatteryType):

        assert created_battery_type.name == "Test Battery Type"
        assert created_battery_type.nominal_voltage == 3.7
        assert created_battery_type.nominal_capacity == 2500

    @pytest.fixture
    def sample_battery_type_without_name(
        self, sample_battery_type: TBatteryTypeEssentials
    ):
        sample_battery_type.name = None  # type: ignore
        return sample_battery_type

    def test_create_battery_type_missing_required_field_name(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_battery_type_without_name: TBatteryType,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_battery_type(
                sample_battery_type_without_name
            )

        assert '{"error":"Failed to validate battery type data","details":' in str(
            excinfo.value
        )

    @pytest.fixture
    def sample_battery_type_without_manufacturer(
        self, sample_battery_type: TBatteryTypeEssentials
    ):
        sample_battery_type.manufacturer = None  # type: ignore
        return sample_battery_type

    def test_create_battery_type_missing_required_field_manufacturer(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_battery_type_without_manufacturer: TBatteryType,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_battery_type(
                sample_battery_type_without_manufacturer
            )

        assert (
            '{"error":"Failed to validate battery type data","details":"Key: \'BatteryType.Manufacturer\''
            in str(excinfo.value)
        )

    @pytest.fixture
    def sample_battery_type_without_capacity(self, sample_battery_type: TBatteryType):
        sample_battery_type.nominal_capacity = ""  # type: ignore
        return sample_battery_type

    def test_create_battery_type_missing_required_field_capacity(
        self,
        ada_logged_client: NovumAPIClient,
        sample_battery_type_without_capacity: TBatteryType,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            ada_logged_client.create_battery_type(sample_battery_type_without_capacity)

        assert '{"error":"Failed to decode battery type data"' in str(excinfo.value)

    @pytest.fixture
    def sample_battery_type_without_voltage(self, sample_battery_type: TBatteryType):
        sample_battery_type.nominal_voltage = ""  # type: ignore
        return sample_battery_type

    def test_update_battery_type(
        self, ada_logged_client: NovumAPIClient, created_battery_type: TBatteryType
    ):
        update_data = TBatteryTypeEssentials(
            name="Updated Battery Type",
            manufacturer="Updated",
            nominal_voltage=3.8,
            nominal_capacity=3200,
            description="There is an update",
        )

        updated_response = ada_logged_client.update_battery_type_by_id(
            created_battery_type.id, update_data
        )

        assert updated_response.name == "Updated Battery Type"
        assert updated_response.manufacturer == "Updated"
        assert updated_response.nominal_voltage == 3.8
        assert updated_response.nominal_capacity == 3200
        assert updated_response.description == "There is an update"

    def test_delete_battery_type_from_another_user(
        self, ada_logged_client: NovumAPIClient
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            ada_logged_client.remove_battery_types_by_id("dpgtbPhcnt5oH685D")

        assert '{"error":"Forbidden","details":""}' in str(excinfo.value)

    def test_delete_battery_type(
        self, ada_logged_client: NovumAPIClient, sample_battery_type
    ):
        sample_battery_type.name = "to be deleted"
        to_be_deleted_sample = sample_battery_type
        to_be_deleted = ada_logged_client.create_battery_type(to_be_deleted_sample)

        response = ada_logged_client.remove_battery_types_by_id(to_be_deleted.id)

        assert "was removed" in response

    # # ********************************************************
    # # Section for the Battery
    # # ********************************************************

    @pytest.fixture
    def sample_battery(self, created_battery_type: TBatteryType):
        return TBatteryEssentials(
            name="Test Battery", battery_type=created_battery_type
        )

    @pytest.fixture
    def created_battery(
        self, ada_logged_client: NovumAPIClient, sample_battery: TBatteryEssentials
    ):

        response = ada_logged_client.create_battery(sample_battery)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_battery_by_id(response.id)

    def test_create_battery(self, created_battery: TBattery):

        assert created_battery.name == "Test Battery"

    @pytest.fixture
    def sample_battery_without_name(self, sample_battery: TBatteryEssentials):
        sample_battery.name = None  # type: ignore

        return sample_battery

    def test_create_battery_missing_required_field_name(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_battery_without_name: TBatteryEssentials,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_battery(sample_battery_without_name)

        assert '{"error":"Failed to validate ' in str(excinfo.value)

    def test_update_battery(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery: TBattery,
        created_battery_type: TBatteryType,
    ):
        update_data = TBatteryEssentials(
            name="Updated Battery",
            battery_type=created_battery_type,
            description="There is an update",
        )

        updated_response = ada_logged_client.update_battery_by_id(
            created_battery.id, update_data
        )

        assert updated_response.name == "Updated Battery"
        assert updated_response.description == "There is an update"

    def test_delete_battery(
        self, ada_logged_client: NovumAPIClient, created_battery_type: TBatteryType
    ):

        to_be_deleted_sample = TBatteryEssentials(
            name="Test Battery Delete", battery_type=created_battery_type
        )
        to_be_deleted = ada_logged_client.create_battery(to_be_deleted_sample)

        response = ada_logged_client.remove_battery_by_id(to_be_deleted.id)

        assert "was removed" in response

    # ********************************************************
    # Section for the DataSet
    # ********************************************************

    @pytest.fixture
    def sample_eis_dataset(self):
        sample_eis = TDatasetEssentials(
            measured=TMeasured(
                start_time="2021-03-10T17:40:44.956Z",
                end_time="2021-03-10T17:42:43.915Z",
                eis_setup=TEISSetup(
                    start_frequency=4000,
                    end_frequency=0.1,
                    number_of_frequencies=21,
                    excitation_current_offset=0.06,
                    excitation_current_amplitude=0.05,
                    excitation_mode=None,
                ),
                voltage=TTimedMeasure(
                    before=2.853627920150757, after=2.8368048667907715
                ),
                ambient_temperature=TTimedMeasure(
                    before=23.423852920532227,
                    after=0,
                ),
                battery_temperature=TTimedMeasure(
                    before=0,
                    after=0,
                ),
                measurement_cycles=[
                    TMeasurementCycle(
                        frequency=3906.25,
                        amplitude=0.03961149351980206,
                        phase_shift=10.600752397202513,
                        voltage=3.4,
                        temperature=None,
                        time_delta=None,
                        quality=None,
                        current_raw_values=None,
                        voltage_raw_values=None,
                    )
                ],
            ),
            analysis=TAnalysis(),
            meta=TDatasetMeta(
                tags=["tag", "tag"],
                client_software=TVersion(
                    tag="test_tag",
                    name="test",
                    hash=None,
                    branch=None,
                    build_date=None,
                    error=None,
                    details=None,
                ),
                device=TDeviceMetaParticle(
                    cpu_id="test123456789",
                    serial="1235654321",
                    name=None,
                    description=None,
                    firmware=TVersion(
                        tag="test_tag",
                        name="test",
                        hash=None,
                        branch=None,
                        build_date=None,
                        error=None,
                        details=None,
                    ),
                ),
            ),
        )
        return sample_eis

    @pytest.fixture
    def created_eis_dataset(
        self, ada_logged_client: NovumAPIClient, sample_eis_dataset: TDatasetEssentials
    ):

        response = ada_logged_client.create_dataset(sample_eis_dataset)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_dataset_by_id(response.id)

    def test_create_eis_dataset(self, created_eis_dataset: TDataset):

        assert isinstance(created_eis_dataset, TDataset)

    @pytest.fixture
    def sample_dataset_without_name(self, sample_eis_dataset: TDatasetEssentials):
        sample_eis_dataset.measured.start_time = None  # type : ignore
        return sample_eis_dataset

    def test_create_dataset_missing_required_field_start_time(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_dataset_without_name: TDatasetEssentials,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_dataset(sample_dataset_without_name)

        assert (
            '{"error":"Failed to validate dataset","details":"Key: \'Dataset.Measured.StartTime\' Error:'
            in str(excinfo.value)
        )

    def test_get_dataset(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDataset
    ):
        response = ada_logged_client.get_datasets()

        assert response[0].id == created_eis_dataset.id

    def test_get_datasets_count(self, ada_logged_client: NovumAPIClient):
        response = ada_logged_client.get_datasets_count()

        assert response == 0

    def test_get_dataset_by_id(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDataset
    ):
        response = ada_logged_client.get_dataset_by_id(created_eis_dataset.id)

        assert response.id == created_eis_dataset.id

    def test_update_dataset(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDataset
    ):
        response = ada_logged_client.get_dataset_by_id(created_eis_dataset.id)
        response.context_id = "new_context_id"
        ada_logged_client.update_dataset_by_id(created_eis_dataset.id, response)
        response_updated = ada_logged_client.get_dataset_by_id(created_eis_dataset.id)

        assert response_updated.context_id == "new_context_id"

    def test_delete_dataset(
        self, ada_logged_client: NovumAPIClient, sample_eis_dataset: TDatasetEssentials
    ):
        to_be_deleted_sample = sample_eis_dataset
        to_be_deleted = ada_logged_client.create_dataset(to_be_deleted_sample)

        response = ada_logged_client.remove_dataset_by_id(to_be_deleted.id)

        assert "was removed" in response

    # ********************************************************
    # Section for the Capacity Measurement
    # ********************************************************

    @pytest.fixture
    def sample_capacity_measurement(self):
        return TCapacityMeasurementEssentials(
            start_time=datetime(2023, 11, 10, 5, 5, 5),
            end_time=None,
            current_setpoint=1,
            voltage_setpoint=2,
            charge_type=TChargeTypes.CC,
            charge_cycles=[
                TChargeCycle(
                    timestamp="2023-09-12T09:57:47.221Z",
                    voltage=3,
                    current=1,
                    charge=1,
                )
            ],
            tags=["test0 only test"],
            ambient_temperature=22.3,
            device_name="NOVUM Testing Device",
            device_info="Firmware: v1.02",
            voltage_min=2.14,
            voltage_max=3.14,
            state_of_health=0.94,
            grade="D",
        )

    @pytest.fixture
    def created_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        sample_capacity_measurement: TCapacityMeasurementEssentials,
    ):

        response = ada_logged_client.create_capacity_measurement(
            sample_capacity_measurement
        )

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_capacity_measurement_by_id(response.id)

    def test_create_capacity_measurement(
        self, created_capacity_measurement: TCapacityMeasurementEssentials
    ):

        assert created_capacity_measurement.current_setpoint == 1

    @pytest.fixture
    def sample_capacity_measurement_without_start_time(
        self, sample_capacity_measurement: TCapacityMeasurementEssentials
    ):
        sample_capacity_measurement.start_time = None  # type: ignore
        return sample_capacity_measurement

    def test_create_capacity_measurement_missing_required_field_start_time(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_capacity_measurement_without_start_time: TCapacityMeasurementEssentials,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_capacity_measurement(
                sample_capacity_measurement_without_start_time
            )

        assert (
            '{"error":"Failed to validate capacity measurement","details":"Key: \'CapacityMeasurement.StartTime\' Error:Field validation for \'StartTime\' failed'
            in str(excinfo.value)
        )

    def test_get_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurement,
    ):
        response = ada_logged_client.get_capacity_measurement()

        assert response[0].id == created_capacity_measurement.id

    def test_get_capacity_measurement_count(self, ada_logged_client: NovumAPIClient):
        response = ada_logged_client.get_capacity_measurement_count()

        assert response == 0

    def test_get_capacity_measurement_by_id(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurement,
    ):
        response = ada_logged_client.get_capacity_measurement_by_id(
            created_capacity_measurement.id
        )

        assert response.id == created_capacity_measurement.id

    def test_update_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurement,
    ):
        response = ada_logged_client.get_capacity_measurement_by_id(
            created_capacity_measurement.id
        )
        response.context_id = "new_context_id"
        ada_logged_client.update_capacity_measurement_by_id(
            created_capacity_measurement.id, response
        )
        response_updated = ada_logged_client.get_capacity_measurement_by_id(
            created_capacity_measurement.id
        )

        assert response_updated.context_id == "new_context_id"

    def test_delete_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        sample_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        to_be_deleted_sample = sample_capacity_measurement
        to_be_deleted = ada_logged_client.create_capacity_measurement(
            to_be_deleted_sample
        )

        response = ada_logged_client.remove_capacity_measurement_by_id(to_be_deleted.id)

        assert "was removed" in response

    #####  No test available because we dont have an delete function for this section

    # ********************************************************
    # Section for the Measurement
    # ********************************************************

    # @pytest.fixture
    # def sample_live_data(self, sample_battery :TBattery):
    #     uit_measurement = UITMeasurement(
    #     time=datetime.now(),
    #     voltage=3.5,
    #     current=1.2,
    #     temperature=25.0,
    #     charge=None,
    #     soc=75.0
    #     )

    #     device_measurement = TDeviceMeasurement(
    #         device_id=sample_battery.id,
    #         measurements=[uit_measurement]
    #     )

    #     # Creating a DeviceMeasurements variable
    #     device_measurements = [device_measurement]

    #     return device_measurements

    # @pytest.fixture
    # def created_live_data(
    #     self, ada_logged_client: NovumAPIClient, sample_live_data:List[TDeviceMeasurement]
    # ):

    #     response = ada_logged_client.write_device_measurements(
    #         sample_live_data
    #     )

    #     yield response

    #     # Add cleanup code here to delete the created battery type
    #     ada_logged_client.remove_______________by_id(response.id)


if __name__ == "__main__":
    pytest.main()
