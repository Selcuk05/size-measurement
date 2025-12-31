from sdks.novavision.src.helper.package import PackageHelper
from components.SizeMeasurement.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    SizeMeasurementOutputs,
    SizeMeasurementResponse,
    SizeMeasurement,
    OutputDetections,
)


def build_response(context):
    outputDetections = OutputDetections(value=context.output_detections)
    Outputs = SizeMeasurementOutputs(outputDetections=outputDetections)
    sizeMeasurementResponse = SizeMeasurementResponse(outputs=Outputs)
    sizeMeasurement = SizeMeasurement(value=sizeMeasurementResponse)
    executor = ConfigExecutor(value=sizeMeasurement)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
