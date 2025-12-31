import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.SizeMeasurement.src.utils.response import build_response
from components.SizeMeasurement.src.models.PackageModel import PackageModel


class SizeMeasurement(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.class_label1 = self.request.get_param("ClassLabel1")
        self.class_label2 = self.request.get_param("ClassLabel2")
        self.measurement_method = self.request.get_param("MeasurementMethod")
        self.detections = self.request.get_param("inputDetections")

        self.reference_object = None
        self.reference_size = None
        self.unit_value = None
        self.pixel_to_unit_ratio = None

        if self.measurement_method == "ReferenceObjectMethod":
            self.reference_object = self.request.get_param("ReferenceObjectSelection")
            self.reference_size = self.request.get_param("ReferenceSize")
            self.unit_value = self.request.get_param("Unit")

        elif self.measurement_method == "ReferencePixelToUnitMethod":
            self.unit_value = self.request.get_param("Unit")
            self.pixel_to_unit_ratio = self.request.get_param("PixelToUnitRatio")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def get_detection_by_label(self, detections, class_label):
        if not detections:
            return None

        for detection in detections:
            if detection["classLabel"].lower() == class_label.lower():
                return detection

        return None

    def get_width_from_detection(self, detection):
        if not detection or not detection.get("boundingBox"):
            return 0.0

        return float(detection["boundingBox"]["width"])

    def add_size_to_detection(self, detection, size):
        detection_dict = {
            "boundingBox": detection["boundingBox"],
            "confidence": detection["confidence"],
            "classLabel": detection["classLabel"],
            "classId": detection["classId"],
            "size": size,
            "unit": self.unit_value,
        }
        return detection_dict

    def calculate_and_add_sizes(self):
        if not self.detections:
            return self.detections

        updated_detections = []

        if self.measurement_method == "ReferenceObjectMethod":
            if self.reference_object == "ClassLabel1":
                reference_label = self.class_label1
                target_label = self.class_label2
            else:
                reference_label = self.class_label2
                target_label = self.class_label1

            reference_detection = self.get_detection_by_label(
                self.detections, reference_label
            )
            target_detection = self.get_detection_by_label(
                self.detections, target_label
            )

            if not reference_detection or not target_detection:
                return self.detections

            reference_width_pixels = self.get_width_from_detection(reference_detection)
            target_width_pixels = self.get_width_from_detection(target_detection)

            if reference_width_pixels == 0:
                return self.detections

            pixel_ratio = target_width_pixels / reference_width_pixels
            target_size = self.reference_size * pixel_ratio

            for detection in self.detections:
                detection_label = detection["classLabel"]
                if detection_label.lower() == reference_label.lower():
                    updated_detection = self.add_size_to_detection(
                        detection, self.reference_size
                    )
                elif detection_label.lower() == target_label.lower():
                    updated_detection = self.add_size_to_detection(
                        detection, target_size
                    )
                else:
                    updated_detection = detection

                updated_detections.append(updated_detection)

        elif self.measurement_method == "ReferencePixelToUnitMethod":
            detection1 = self.get_detection_by_label(self.detections, self.class_label1)
            detection2 = self.get_detection_by_label(self.detections, self.class_label2)

            for detection in self.detections:
                detection_label = detection["classLabel"]
                if (
                    detection_label.lower() == self.class_label1.lower()
                    or detection_label.lower() == self.class_label2.lower()
                ):
                    width_pixels = self.get_width_from_detection(detection)
                    size = width_pixels * self.pixel_to_unit_ratio
                    updated_detection = self.add_size_to_detection(detection, size)
                else:
                    updated_detection = detection

                updated_detections.append(updated_detection)
        else:
            return self.detections

        return updated_detections

    def run(self):
        self.output_detections = self.calculate_and_add_sizes()

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
