#!/bin/bash

echo "----------------------------------------------------------------"
echo "--- Start at $(date) ---"
cd /home/ec2-user/financial_database

# Track the start time of the entire script
start_time=$(date +%s)

# Clean up checkpoints
echo "--- Checkpoints Clean Up ---"
FILE="/home/ec2-user/financial_database/backend/data/checkpoints/avan_checkpoint.json"
FILE2="/home/ec2-user/financial_database/backend/data/checkpoints/calc_pipeline.json"
[ -f "$FILE" ] && rm "$FILE" && echo "$FILE deleted" || echo "$FILE does not exist"
[ -f "$FILE2" ] && rm "$FILE2" && echo "$FILE2 deleted" || echo "$FILE2 does not exist"


echo "--- Start running pipeline_stock_price_updater ---"
pipeline_start_time=$(date +%s)
/home/ec2-user/financial_database/venv/bin/python3 /home/ec2-user/financial_database/backend/pipeline_stock_price_updater.py
pipeline_end_time=$(date +%s)
echo "--- Finish running pipeline 1---"
echo "--- pipeline_stock_price_updater Duration: $((pipeline_end_time - pipeline_start_time)) seconds ---"


# echo "--- Start running pipeline_stock_signal_updater_coint---"
# pipeline_start_time=$(date +%s)
# /home/ec2-user/financial_database/venv/bin/python3 /home/ec2-user/financial_database/backend/pipeline_stock_signal_updater_coint.py
# pipeline_end_time=$(date +%s)
# echo "--- Finish running pipeline_stock_signal_updater_coint---"
# echo "--- pipeline_stock_signal_updater_coint Duration: $((pipeline_end_time - pipeline_start_time)) seconds ---"
 
 
# echo "--- Start running pipeline_stock_signal_updater_coint_by_sectors---"
# pipeline_start_time=$(date +%s)
# /home/ec2-user/financial_database/venv/bin/python3 /home/ec2-user/financial_database/backend/pipeline_stock_signal_updater_coint_by_sectors.py
# pipeline_end_time=$(date +%s)
# echo "--- Finish running pipeline_stock_signal_updater_coint_by_sectors---"
# echo "--- pipeline_stock_signal_updater_coint_by_sectors Duration: $((pipeline_end_time - pipeline_start_time)) seconds ---"

# Track the end time of the entire script
end_time=$(date +%s)
echo "--- Finished at $(date) ---"
echo "--- Total Duration: $((end_time - start_time)) seconds ---"
echo "----------------------------------------------------------------"