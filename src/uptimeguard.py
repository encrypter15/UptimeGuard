import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class UptimeGuard:
    def __init__(self, websites, email_config):
        self.websites = websites
        self.email_config = email_config
        self.downtime_log = {}

    def check_website(self, url):
        try:
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def send_email_alert(self, website):
        msg = MIMEText(f"Alert: {website} is down!")
        msg['Subject'] = f"UptimeGuard Alert: {website}"
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)

    def log_downtime(self, website):
        if website not in self.downtime_log:
            self.downtime_log[website] = []
        self.downtime_log[website].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def run(self):
        while True:
            for website in self.websites:
                if not self.check_website(website):
                    print(f"{website} is down!")
                    self.log_downtime(website)
                    self.send_email_alert(website)
                else:
                    print(f"{website} is up.")
            time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    websites = ["https://example.com", "https://google.com"]
    email_config = {
        "from": "uptimeguard@example.com",
        "to": "admin@example.com",
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "username": "uptimeguard",
        "password": "yourpassword"
    }

    uptime_guard = UptimeGuard(websites, email_config)
    uptime_guard.run()
