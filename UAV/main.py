import logging
from drone_controller import DroneController
from anomaly_detector import AnomalyDetector
from gps_tracker import GPSTracker
from alarm_system import AlarmSystem
from database_manager import DatabaseManager


class UAVSurveillanceSystem:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.drone_controller = DroneController()
        self.gps_tracker = GPSTracker()
        self.anomaly_detector = AnomalyDetector()
        self.alarm_system = AlarmSystem()
        self.database_manager = DatabaseManager()

    def initialize_mission(self, initial_coordinates):
        """
        Initialize surveillance mission

        Args:
            initial_coordinates (tuple): (latitude, longitude) of takeoff location
        """
        try:
            # Log mission start
            self.logger.info(f"Initializing surveillance mission at {initial_coordinates}")

            # Record initial coordinates
            self.database_manager.log_mission_start(initial_coordinates)

            # Take off and hover
            takeoff_success = self.drone_controller.takeoff(initial_coordinates)
            if not takeoff_success:
                self.logger.error("Takeoff failed. Aborting mission.")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Mission initialization error: {e}")
            return False

    def detect_and_respond(self, current_coordinates):
        """
        Detect anomalies and respond accordingly

        Args:
            current_coordinates (tuple): Current GPS coordinates
        """
        try:
            # Capture video frame
            video_frame = self.drone_controller.capture_frame()

            # Detect anomalies
            anomaly_detected = self.anomaly_detector.detect_human_anomaly(video_frame)

            if anomaly_detected:
                # Log anomaly details
                self.database_manager.log_anomaly(current_coordinates)

                # Trigger alarm
                self.alarm_system.raise_alarm(current_coordinates)

                # Optional: Capture high-resolution evidence
                evidence_frame = self.drone_controller.capture_high_res_frame()
                self.database_manager.store_evidence(evidence_frame)

            return anomaly_detected

        except Exception as e:
            self.logger.error(f"Anomaly detection error: {e}")
            return False

    def return_and_land(self, initial_coordinates):
        """
        Return to initial coordinates and land

        Args:
            initial_coordinates (tuple): Original takeoff location
        """
        try:
            # Navigate back to initial coordinates
            return_success = self.drone_controller.navigate_to(initial_coordinates)

            if return_success:
                # Attempt landing
                landing_success = self.drone_controller.land_on_charging_pad()

                if landing_success:
                    self.logger.info("Mission completed successfully")
                    self.database_manager.log_mission_end()
                    return True
                else:
                    self.logger.warning("Landing failed")
                    return False

        except Exception as e:
            self.logger.error(f"Return and land error: {e}")
            return False


def main():
    # Example usage
    surveillance_system = UAVSurveillanceSystem()

    # Sample initial coordinates (replace with actual GPS coordinates)
    initial_coords = (37.7749, -122.4194)  # Example: San Francisco

    # Run mission workflow
    if surveillance_system.initialize_mission(initial_coords):
        # Simulate continuous surveillance
        current_coords = initial_coords
        anomaly_found = surveillance_system.detect_and_respond(current_coords)

        if anomaly_found:
            surveillance_system.return_and_land(initial_coords)


if __name__ == "__main__":
    main()