import time
import requests
import json

api_token = '5b6Cq6ktxABiB9u4L8YsdlA2nJD8jluoVzL5TzCInFI'
api_url_base = 'http://localhost:5000/'
old_job_state = None

api_url = '{}{}'.format(api_url_base, 'api/printer')
api_url_job = '{}{}'.format(api_url_base, 'api/job')

headers = {
         'X-Api-Key': api_token 
          }

while True:
    response = requests.get(api_url, headers=headers)
    job_response = requests.get(api_url_job, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        #job_response = job_response.json()

        print(response.text)
        #with open("response_pretty.json", "w", encoding="utf-8") as f:
        #    json.dump(job_response.json(), f, indent=2, ensure_ascii=False)
    else:
        print("Failed to retrieve data:", response.status_code)
    time.sleep(4)


            if status != old_job_state:
            if old_job_state== 'Operational' and status == 'Printing':
                print("-------------Print job started!----------")
                old_job_state = status
            else:
                if progress == 100:
                    print("-------------Print job completed!----------")
                    old_job_state = status
            if nozzle_target is not None:
                if nozzle_temp < nozzle_target:
                    print("Nozzle is heating up: {}°C / {}°C".format(nozzle_temp, nozzle_target))
                if bed_target is not None:
                    if bed < bed_target:
                        print("Bed is heating up: {}°C / {}°C".format(bed, bed_target))
                    elif bed >= bed_target and nozzle_temp >= nozzle_target:
                        print("-------------Heating complete!----------")

        if old_job_state is None:
            old_job_state = status