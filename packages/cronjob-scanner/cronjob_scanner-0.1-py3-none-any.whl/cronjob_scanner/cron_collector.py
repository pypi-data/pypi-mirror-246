import subprocess
import requests


def get_cron_jobs():
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    return result.stdout


def send_to_endpoint(cron_data):
    response = requests.post('http://ping.keepuptime.com/cronjob-scan-result', json={'data': cron_data})

    return response.status_code


def main():
    cron_jobs = get_cron_jobs()
    send_to_endpoint(cron_jobs)
