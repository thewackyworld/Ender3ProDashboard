import requests
from key import get_api_token


old_job_state = None

def get_printer_data():
    api_token = get_api_token()
    api_url_base = 'http://localhost:5000/'
    api_url = '{}{}'.format(api_url_base, 'api/printer')
    api_url_job = '{}{}'.format(api_url_base, 'api/job')
    global old_job_state

    headers = {
            'X-Api-Key': api_token 
            }

    response = requests.get(api_url, headers=headers)
    job_response = requests.get(api_url_job, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        job_data = job_response.json()
        nozzle_temp = json_data['temperature']['tool0']['actual']
        nozzle_target = json_data['temperature']['tool0']['target']
        bed = json_data['temperature']['bed']['actual']
        bed_target = json_data['temperature']['bed']['target']
        status = job_data['state']
        progress = job_data['progress']['completion']
        job = "idle"
        event = None

        match(status):
            case 'Operational' if nozzle_target is None:
               job = "idle"
            case 'Printing' if nozzle_target is not None and bed_target is not None:
                if nozzle_temp < nozzle_target or bed < bed_target:
                    job = "preheating"
                if nozzle_temp >= nozzle_target-5 and bed >= bed_target-5:
                    job = "printing"

        if status != old_job_state:
            if old_job_state== 'Operational' and status == 'Printing':
                event = "Print job started!"
            elif old_job_state == 'Printing' and status == 'Operational':
                event = "Print job completed!"

        old_job_state = status
        progress = round(progress, 2) if progress is not None else "N/A"

        return {
            "temperature": {
                "nozzle": {
                    "actual": nozzle_temp,
                    "target": nozzle_target
                },
                "bed": {
                    "actual": bed,
                    "target": bed_target
                }
            },
            "status": job,
            "progress": progress,
            "event": event
        } 
    else:
        print("Failed to retrieve data:", response.status_code)
        return response.status_code
