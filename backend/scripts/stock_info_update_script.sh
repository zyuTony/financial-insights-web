#!/bin/bash

echo "----------------------------------------------------------------"
echo "--- Start at $(date) ---"
cd C:/Users/zongy/Desktop/repo/financial_database

# Track the start time of the entire script
start_time=$(date +%s)

# Clean up checkpoints
echo "--- Checkpoints Clean Up ---"
# FILE="/home/ec2-user/financial_database/backend/data/checkpoints/avan_overview_checkpoint.json"
FILE="C:/Users/zongy/Desktop/repo/financial_database/backend/data/checkpoints/avan_overview_checkpoint.json"
[ -f "$FILE" ] && rm "$FILE" && echo "$FILE deleted" || echo "$FILE does not exist" 


echo "--- Start running pipeline_stock_overview_updater---"
pipeline_start_time=$(date +%s)
C:/Users/zongy/Desktop/repo/financial_database/venv/Scripts/python.exe C:/Users/zongy/Desktop/repo/financial_database/backend/pipeline_stock_overview_updater.py
pipeline_end_time=$(date +%s)
echo "--- Finish running pipeline_stock_overview_updater---"
echo "--- pipeline_stock_overview_updater Duration: $((pipeline_end_time - pipeline_start_time)) seconds ---"

echo "--- Start running pipeline_stock_fundenmentals_updater---"
pipeline_start_time=$(date +%s)
C:/Users/zongy/Desktop/repo/financial_database/venv/Scripts/python.exe C:/Users/zongy/Desktop/repo/financial_database/backend/pipeline_stock_fundenmentals_updater.py
pipeline_end_time=$(date +%s)
echo "--- Finish running pipeline_stock_fundenmentals_updater---"
echo "--- pipeline_stock_fundenmentals_updater Duration: $((pipeline_end_time - pipeline_start_time)) seconds ---"

# Track the end time of the entire script
end_time=$(date +%s)
echo "--- Finished at $(date) ---"
echo "--- Total Duration: $((end_time - start_time)) seconds ---"
echo "----------------------------------------------------------------"