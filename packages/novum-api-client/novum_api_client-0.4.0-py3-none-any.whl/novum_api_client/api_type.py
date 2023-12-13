# pylint: disable=C0115

import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class TNovumClient:
    pass


@dataclass
class TStats:
    last_login: Union[str, int]
    logins_count: int
    last_ip: str


@dataclass
class TProfile:
    name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    picture: Optional[str]


@dataclass
class TServiceCenterSettings:
    show_advanced_options: Optional[bool] = None
    invert_axis: Optional[bool] = None
    only_show_top_level_batteries: Optional[bool] = None
    favorite_batteries_ids: Optional[List[str]] = None
    battery_table_columns: Optional[List[str]] = None
    dashboard_table_columns: Optional[List[str]] = None
    eis_dataset_table_columns: Optional[List[str]] = None
    capacity_measurement_table_columns: Optional[List[str]] = None


@dataclass
class TUserSettings:
    service_center: Optional[TServiceCenterSettings] = None


@dataclass
class TIDAndTimes:
    id: Optional[str] = None
    created_at: Optional[Union[datetime.datetime, str]] = None
    updated_at: Optional[Union[datetime.datetime, str]] = None


@dataclass
class TUserEssentials:
    jwt: Optional[str]
    refresh_token: Optional[str]
    auth0_id: Optional[str]
    roles: Optional[List[str]]
    profile: Optional[TProfile]
    settings: Optional[TUserSettings]
    permissions: Optional[List[str]]
    stats: Optional[TStats]
    meta_data: Optional[dict]
    scope: Optional[str]


@dataclass
class TUser(TUserEssentials, TIDAndTimes):
    "TUser"


@dataclass
class TMinMax:
    min: Optional[float] = None
    max: Optional[float] = None


@dataclass
class TGeometricDimension:
    height: Optional[float] = None
    width: Optional[float] = None
    depth: Optional[float] = None


@dataclass
class TEISSetup:
    start_frequency: Optional[float] = None
    end_frequency: Optional[float] = None
    number_of_frequencies: Optional[int] = None
    excitation_current_offset: Optional[float] = None
    excitation_current_amplitude: Optional[float] = None
    excitation_mode: Optional[int] = None


@dataclass
class TChargeSetup:
    discharge_rate: Optional[float] = None
    charge_rate: Optional[float] = None


@dataclass
class TUserDocument:
    original_file_name: Optional[str] = None
    file_name: Optional[str] = None
    file_url: Optional[str] = None
    file_md5: Optional[str] = None
    file_type: Optional[Dict[str, Union[str, int, float]]] = None
    file_size: Optional[int] = None
    aws_file_url: Optional[str] = None
    aws_file_name: Optional[str] = None


@dataclass
class TBaseDocModel(TIDAndTimes):
    creator_id: Optional[str] = None
    updater_id: Optional[str] = None
    id: Optional[str] = None


@dataclass
class TDetails:
    code: Optional[int] = None
    error: Optional[str] = None
    details: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


@dataclass
class TAPIError:
    error: Optional[str] = None
    details: Optional[TDetails] = None


@dataclass
class TLatLng:
    planet: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


@dataclass
class TAddress:
    country: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None


@dataclass
class TLocation:
    geo: Optional[TLatLng] = None
    address: Optional[TAddress] = None


@dataclass
class TMetrics:
    measured_at: Optional[datetime.datetime] = None
    state_of_health: Optional[float] = None
    state_of_charge: Optional[float] = None
    temperature: Optional[float] = None


@dataclass
class TIndicatorProperty:
    scale: Optional[float] = None
    top: Optional[float] = None
    left: Optional[float] = None


@dataclass
class TIndicatorProperties:
    properties: Optional[Dict[str, TIndicatorProperty]] = None


@dataclass
class TInsights:
    enabled: Optional[bool] = None
    image: Optional[str] = None
    image_styles: Optional[str] = None
    indicator_properties: Optional[TIndicatorProperties] = None


@dataclass
class TAtomicState:
    updated_at: Union[datetime.datetime, str]
    value: float
    origin_id: Optional[str]


@dataclass
class TBatteryState:
    state_of_health: Optional[TAtomicState] = None
    state_of_charge: Optional[TAtomicState] = None
    current: Optional[TAtomicState] = None
    voltage: Optional[TAtomicState] = None
    temperature: Optional[TAtomicState] = None


@dataclass
class TTreeProperties:
    is_leaf: Optional[bool] = None
    enabled: Optional[bool] = None
    parent: Optional[str] = None
    ancestors: Optional[List[str]] = None
    children_topology: Optional[str] = None


@dataclass
class TEstimatorOverview:
    file_name: Optional[str] = None
    description: Optional[str] = None
    time: Optional[Union[str, datetime.datetime]] = None
    last_valid_time: Optional[Union[str, datetime.datetime]] = None
    model_state: Optional[List[float]] = None
    last_valid_model_state: Optional[List[float]] = None
    report: Optional[str] = None


@dataclass
class TEstimators:
    soc_estimator: Optional[TEstimatorOverview] = None


@dataclass
class TBatteryTypeEssentials:
    """For writing"""

    name: str
    manufacturer: str
    nominal_voltage: float
    nominal_capacity: float
    description: Optional[str] = None
    cell_chemistry: Optional[str] = None
    battery_design: Optional[str] = None
    allowed_voltage_range_single_cell: Optional[TMinMax] = None
    allowed_voltage_range_battery_pack: Optional[TMinMax] = None
    allowed_peak_charge_current_range: Optional[TMinMax] = None
    allowed_continuous_charge_current_range: Optional[TMinMax] = None
    allowed_temperature_range_for_charging: Optional[TMinMax] = None
    allowed_temperature_range_for_storage: Optional[TMinMax] = None
    allowed_temperature_range_for_use: Optional[TMinMax] = None
    internal_resistance: Optional[float] = None
    self_discharge_rate_per_month: Optional[float] = None
    allowed_cycles_for_100_depth_of_discharge: Optional[int] = None
    mass_based_power_density: Optional[float] = None
    cell_mass: Optional[float] = None
    outer_geometric_dimension: Optional[TGeometricDimension] = None
    default_eis_setup: Optional[TEISSetup] = None
    default_charge_setup: Optional[TChargeSetup] = None
    image: Optional[str] = None
    user_docs: Optional[List[TUserDocument]] = None
    user_doc_ids: Optional[List[str]] = None
    public: Optional[bool] = None
    tags: Optional[List[str]] = None


@dataclass
class TBatteryType(TBatteryTypeEssentials, TBaseDocModel):
    """For reading"""


@dataclass
class TBatteryEssentials:
    name: str
    battery_type: TBatteryType
    serial_number: Optional[str] = None
    description: Optional[str] = None
    location: Optional[TLocation] = None
    image: Optional[str] = None
    tags: Optional[List[str]] = None
    metrics: Optional[TMetrics] = None
    insights: Optional[TInsights] = None
    state: Optional[TBatteryState] = None
    tree: Optional[TTreeProperties] = None
    estimators: Optional[TEstimators] = None
    user_doc_ids: Optional[List[str]] = None


@dataclass
class TBattery(TBatteryEssentials, TBaseDocModel):
    """For reading"""


@dataclass
class TChargeTypes:
    UNKNOWN = "UNKNOWN"
    CC = "CC"
    CCCV = "CCCV"
    CCPulse = "CCPulse"


@dataclass
class TChargeCycle:
    timestamp: Optional[Union[str, datetime.datetime]]
    voltage: Optional[float] = None  # in Voltage (V)
    current: Optional[float] = None  # in Ampere (A)
    charge: Optional[float] = None  # in AmpereHours (Ah)
    temperature: Optional[float] = None  # in °C (K)


@dataclass
class TCapacityMeasurementEssentials:
    tags: List[str]
    charge_cycles: List[TChargeCycle]
    start_time: datetime.datetime
    charge_type: TChargeTypes
    context_id: Optional[str] = None
    battery: Optional[TBattery] = None
    end_time: Optional[datetime.datetime] = None
    current_setpoint: Optional[float] = None  # in Ampere (A)
    voltage_setpoint: Optional[float] = None  # in Voltage (V)
    ambient_temperature: Optional[float] = None  # in °C (K)
    device_name: Optional[str] = None
    device_info: Optional[str] = None
    voltage_min: Optional[float] = None  # in Voltage (V)
    voltage_max: Optional[float] = None  # in Voltage (V)
    capacity: Optional[float] = None  # in AmpereHours (Ah)
    state_of_health: Optional[float] = None
    internal_resistance: Optional[float] = None  # in Ohm (Ω)
    grade: Optional[str] = None
    is_preview: Optional[bool] = None


@dataclass
class TCapacityMeasurement(TCapacityMeasurementEssentials, TBaseDocModel):
    """For reading"""


@dataclass
class TTimedMeasure:
    before: Optional[float] = None
    after: Optional[float] = None


@dataclass
class TVersionEssentials:
    tag: str
    name: str
    hash: Optional[str] = None
    branch: Optional[str] = None
    build_date: Optional[datetime.datetime] = None


@dataclass
class TVersion(TAPIError, TVersionEssentials):
    "TVersion"


@dataclass
class TMeasurementCycle:
    frequency: float  # frequency of the periodic excitation in Hz
    amplitude: float  # amplitude of the oscillation current in A
    phase_shift: float  # phase shift of the oscillation current
    temperature: Optional[float] = None
    voltage: Optional[float] = None  # voltage measured before the excitation in V
    time_delta: Optional[float] = None  # in seconds
    quality: Optional[float] = None  # a quality indicator
    voltage_raw_values: Optional[List[float]] = None
    current_raw_values: Optional[List[float]] = None


@dataclass
class TRemoteProcedureReport:
    success: bool
    report: str


@dataclass
class TDeviceMetaParticle:
    cpu_id: str
    serial: str
    firmware: TVersion
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class TProduct(TBaseDocModel):
    gtin: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class TDeviceMeta(TBaseDocModel, TDeviceMetaParticle):
    product: Optional[TProduct] = None
    revision: Optional[str] = None
    description: Optional[str] = None


@dataclass
class TAPIInfoEssentials:
    name: Optional[str] = None
    dbName: Optional[str] = None
    version: Optional[TVersion] = None
    description: Optional[str] = None
    dev_container_mode: Optional[str] = None


@dataclass
class TAPIInfo(TAPIInfoEssentials, TAPIError):
    "Info"


@dataclass
class TMeasured:
    start_time: Optional[Union[datetime.datetime, str]] = None
    end_time: Optional[Union[datetime.datetime, str]] = None
    eis_setup: Optional[TEISSetup] = None
    voltage: Optional[TTimedMeasure] = None
    ambient_temperature: Optional[TTimedMeasure] = None
    battery_temperature: Optional[TTimedMeasure] = None
    measurement_cycles: Optional[List[TMeasurementCycle]] = None


@dataclass
class TAnalysis:
    grade: Optional[str] = None
    state_of_health: Optional[float] = None
    state_of_charge: Optional[float] = None
    temperature: Optional[float] = None
    enforce_capacity_test: Optional[bool] = None
    reports: Optional[Dict[str, TRemoteProcedureReport]] = None


@dataclass
class TDatasetMeta:
    tags: List[str]
    device: TDeviceMetaParticle
    client_software: TVersion
    comment: Optional[str] = None
    battery: Optional[TBattery] = None
    user_defined: Optional[str] = None


@dataclass
class TDatasetEssentials:
    measured: TMeasured
    analysis: TAnalysis
    meta: TDatasetMeta
    show_in_chart: Optional[bool] = None
    context_id: Optional[str] = None


@dataclass
class TDataset(TDatasetEssentials, TBaseDocModel):
    """For reading"""


@dataclass
class UITMeasurement:
    time: datetime.datetime
    voltage: Optional[float]
    current: Optional[float]
    temperature: Optional[float]
    charge: Optional[float]
    soc: Optional[float]


@dataclass
class UITMeasurements(List[UITMeasurement]):
    pass


@dataclass
class TDeviceMeasurement:
    device_id: str
    measurements: UITMeasurements
