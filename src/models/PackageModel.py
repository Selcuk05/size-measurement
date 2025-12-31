from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Input,
    Config,
    Detection,
)


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: List[Detection]
    type: str = "object"

    class Config:
        title = "Detections"


class ClassLabel1(Config):
    """
    First class label to be used for size measurement.
    """

    name: Literal["ClassLabel1"] = "ClassLabel1"
    value: str = Field(default="")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["Enter first class label"] = "Enter first class label"

    class Config:
        title = "Class Label 1"


class ClassLabel2(Config):
    """
    Second class label to be used for size measurement.
    """

    name: Literal["ClassLabel2"] = "ClassLabel2"
    value: str = Field(default="")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["Enter second class label"] = "Enter second class label"

    class Config:
        title = "Class Label 2"


class ReferenceClassLabel1(Config):
    name: Literal["ReferenceClassLabel1"] = "ReferenceClassLabel1"
    value: Literal["ClassLabel1"] = "ClassLabel1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Class Label 1"


class ReferenceClassLabel2(Config):
    name: Literal["ReferenceClassLabel2"] = "ReferenceClassLabel2"
    value: Literal["ClassLabel2"] = "ClassLabel2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Class Label 2"


class ReferenceObjectSelection(Config):
    """
    Select which class label will be used as the reference object for size measurement.
    """

    name: Literal["ReferenceObjectSelection"] = "ReferenceObjectSelection"
    value: Union[ReferenceClassLabel1, ReferenceClassLabel2]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Reference Object"


class ReferenceSize(Config):
    """
    Size of the reference object in the specified unit.
    """

    name: Literal["ReferenceSize"] = "ReferenceSize"
    value: float = Field(ge=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["Enter reference object size"] = "Enter reference object size"

    class Config:
        title = "Reference Size"


class ReferenceObjectMethod(Config):
    """
    Configuration for reference object measurement method.
    """

    name: Literal["ReferenceObjectMethod"] = "ReferenceObjectMethod"
    referenceObject: ReferenceObjectSelection
    referenceSize: ReferenceSize
    value: Literal["ReferenceObjectMethod"] = "ReferenceObjectMethod"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Reference Object"


class PixelUnitCM(Config):
    name: Literal["PixelUnitCM"] = "PixelUnitCM"
    value: Literal["cm"] = "cm"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Centimeters"


class PixelUnitMM(Config):
    name: Literal["PixelUnitMM"] = "PixelUnitMM"
    value: Literal["mm"] = "mm"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Millimeters"


class PixelUnitInches(Config):
    name: Literal["PixelUnitInches"] = "PixelUnitInches"
    value: Literal["inches"] = "inches"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Inches"


class PixelUnit(Config):
    """
    Unit of measurement for pixel-to-unit conversion.
    """

    name: Literal["PixelUnit"] = "PixelUnit"
    value: Union[PixelUnitCM, PixelUnitMM, PixelUnitInches]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Unit"


class PixelToUnitRatio(Config):
    """
    How many units per pixel (e.g., 0.1 means 0.1 cm per pixel).
    """

    name: Literal["PixelToUnitRatio"] = "PixelToUnitRatio"
    value: float = Field(ge=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["Enter units per pixel"] = "Enter units per pixel"

    class Config:
        title = "Units per Pixel"


class ReferencePixelToUnitMethod(Config):
    """
    Configuration for pixel-to-unit measurement method.
    """

    name: Literal["ReferencePixelToUnitMethod"] = "ReferencePixelToUnitMethod"
    pixelUnit: PixelUnit
    pixelToUnitRatio: PixelToUnitRatio
    value: Literal["ReferencePixelToUnitMethod"] = "ReferencePixelToUnitMethod"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Reference Pixel to Unit"


class MeasurementMethod(Config):
    """
    Select the measurement method: reference object or pixel-to-unit conversion.
    """

    name: Literal["MeasurementMethod"] = "MeasurementMethod"
    value: Union[ReferenceObjectMethod, ReferencePixelToUnitMethod]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Measurement Method"
        json_schema_extra = {"target": "value"}


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: List[Detection]
    type: str = "object"

    class Config:
        title = "Detections"


class SizeMeasurementInputs(Inputs):
    inputDetections: InputDetections


class SizeMeasurementConfigs(Configs):
    classLabel1: ClassLabel1
    classLabel2: ClassLabel2
    measurementMethod: MeasurementMethod


class SizeMeasurementOutputs(Outputs):
    outputDetections: OutputDetections


class SizeMeasurementRequest(Request):
    inputs: Optional[SizeMeasurementInputs]
    configs: SizeMeasurementConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class SizeMeasurementResponse(Response):
    outputs: SizeMeasurementOutputs


class SizeMeasurement(Config):
    name: Literal["SizeMeasurement"] = "SizeMeasurement"
    value: Union[SizeMeasurementRequest, SizeMeasurementResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "SizeMeasurement"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[SizeMeasurement]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {"target": "value"}


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["SizeMeasurement"] = "SizeMeasurement"
