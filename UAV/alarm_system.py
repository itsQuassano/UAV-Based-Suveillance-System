import smtplib


class AlarmSystem:
    def __init__(self):
        # Initialize alarm configurations
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'port': 587,
            'sender_email': 'your_email@gmail.com',
            'recipients': ['security@example.com']
        }

    def raise_alarm(self, coordinates):
        """
        Raise alarm for detected anomaly

        Args:
            coordinates (tuple): GPS coordinates of anomaly
        """
        print(f"ALARM: Suspicious activity detected at {coordinates}")
        self.send_email_alert(coordinates)

    def send_email_alert(self, coordinates):
        """Send email alert for anomaly"""
        try:
            # Email sending logic (simulated)
            print(f"Sending email alert for coordinates: {coordinates}")
        except Exception as e:
            print(f"Failed to send email alert: {e}")
