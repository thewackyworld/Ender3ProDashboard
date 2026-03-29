
    response = requests.get(api_url, headers=headers)
    job_response = requests.get(api_url_job, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        job_data = job_response.json()
        nozzle_temp = json_data['temperature']['tool0']['actual']
        nozzle_target = json_data['temperature']['tool0']['target']
        bed = json_data['temperature']['bed']['actual']
        bed_target = json_data['temperature']['bed']['target']
        status = job_data['st