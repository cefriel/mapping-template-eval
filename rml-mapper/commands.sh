#!/bin/sh

mkdir /home/store

# Wait a little bit to ensure volumes are mounted correctly
sleep 3

# Print 'tree' in current folder
# find . -print | sed -e "s;[^/]*/;|____;g;s;____|; |;g"

/usr/bin/time -f "elapsed_time,kernel_mode,user_mode,memory_max,memory_average\n%e,%S,%U,%M,%K" -o /home/out/time.txt java -Xmx64g -jar /home/rmlmapper.jar -m /home/mappings/mapping.ttl -o /home/out/output.ttl
# elapsed_time(seconds)
# cpu_percentage[(%U + %S) / %E]
# kernel_mode(CPU-seconds)
# user_mode(CPU-seconds)
# memory_max(Kbytes)
# memory_average(Kbytes)

sleep 10
