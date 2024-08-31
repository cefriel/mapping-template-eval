import pandas as pd
import os

test_case = os.getenv('TEST_CASE')

stats_file = os.getenv('STATS_FILE')
df = pd.read_csv(stats_file)

output_file = 'aggregated_stats.csv'

with open(output_file, 'a') as file:
    for index, row in df.iterrows():
        file.write(f"{test_case},{row['step']},{row['duration_median']},{row['memory_ram_max_median']},{row['cpu_user_system_diff_median']}\n")

