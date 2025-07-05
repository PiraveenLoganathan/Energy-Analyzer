# Energy-Analyzer From Piraveen Loganathan

I made a modern and minimalistic Python desktop application as an intermediate Python user that analyzes energy patterns. 

## Features

✅ **Upload & Analyze CSV Data**  
✅ **Visualize Daily Energy Usage**  
✅ **Detect Nighttime Inefficiencies** (e.g. high usage at 2am)  
✅ **Forecast Future Usage** using Linear Regression  


## 📁 Example CSV Format

Your input `.csv` should include:

| timestamp           | energy_kWh |
|---------------------|------------|
| 2025-07-01 00:00:00 | 1.2        |
| 2025-07-01 01:00:00 | 1.1        |

- `timestamp` must be in datetime format  
- `energy_kWh` is the power consumption at that time

A sample file is included: energy_data.csv
