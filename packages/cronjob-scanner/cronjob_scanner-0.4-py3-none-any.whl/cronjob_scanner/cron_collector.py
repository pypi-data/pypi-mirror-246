import subprocess
import requests
import argparse


def get_cron_jobs():
    print('Start fetching cron jobs...')
    print('-----------------------------------')

    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    print('-----------------------------------')
    print(result)
    print('Cron jobs was successfully fetched.')
    print('-----------------------------------')

    return result.stdout


def send_to_endpoint(cron_data):
    print('Sending data to server...')
    print('-----------------------------------')
    print(cron_data)
    response = requests.post('http://ping.keepuptime.com/cronjob-scan-result', json={'data': cron_data})

    if response.status_code == 200:
        print('Data was successfully sent.')
        print('-----------------------------------')
    else:
        print('Something went wrong.')
        print('-----------------------------------')

    return response.status_code


def main():
    print('Start scanning...')
    print('-----------------------------------')

    parser = argparse.ArgumentParser(description='Cronjob scanner')
    parser.add_argument('--key', required=True, help='An Apikey to use with the scanner')
    args = parser.parse_args()
    api_key = args.key

    print(f"Received an apikey: {api_key}")

    cron_jobs = get_cron_jobs()

    send_to_endpoint(cron_jobs)

    print('Done.')
