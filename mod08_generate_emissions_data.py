import pandas as pd

def generate_data():
    #table of jobs generated with below data
    #job number, how many CPU cores job needs
    #and how long jor runs in hours
    jobs = pd.DataFrame({
        "job_id": range(1, 16),
        "cpu_cores": [1, 2, 4, 8, 2, 1, 16, 4, 8, 2, 4, 8, 2, 8, 16],
        "runtime_hours": [0.5, 1.2, 0.75, 2.5, 1.0, 0.3, 3.0, 1.5, 2.0, 0.8, 0.5, 2.25, 1.6, 0.9, 1.1]
    })

    carbon_intensity = {
        #how intense the carbon is, 
            #
        "coal_heavy_region": 0.9,   # kg CO2 per kWh
    #    "mixed_region": 0.45,
        "renewable_region": 0.05
    }

    power_per_core_kw = 0.05  # 50W per CPU core

    max_cores_per_region = {
        #computing capacity per cores for this region
        "coal_heavy_region": 32,
    #   "mixed_region": 24,
        "renewable_region": 16
    }

    #returned so could be used in sustainability 
    # calculations file
    return jobs, carbon_intensity, power_per_core_kw, max_cores_per_region