import cloudpassage
import scanslib
import os
import sys
import time
from datetime import datetime

config = cloudpassage.ApiKeyManager()
env_date = os.getenv("TARGET_DATE")
output_dir = os.getenv("DROP_DIRECTORY")
scans_per_file = 10000
start_time = datetime.now()
s3_bucket_name = os.getenv("AWS_S3_BUCKET")
file_number = 0
counter = 0
scan_threads = int(os.getenv("SCAN_THREADS", 10))
enricher_threads = int(os.getenv("ENRICHER_THREADS", 5))
scan_cache = scanslib.GetScans(config.key_id, config.secret_key,
                               config.api_hostname, config.api_port,
                               scans_per_file, env_date, scan_threads,
                               enricher_threads)

if (env_date is None or
        scanslib.Utility.target_date_is_valid(env_date) is False):
    msg = "Bad date: %s \nExiting!" % env_date
    print(msg)
    sys.exit(2)

for batch in scan_cache:
    counter = counter + len(batch)
    try:
        print("Last timestamp in batch: %s" % batch[-1]["created_at"])
    except IndexError:
        pass
    file_number = file_number + 1
    output_file = "Halo-Scans_%s_%s" % (env_date, str(file_number))
    full_output_path = os.path.join(output_dir, output_file)
    print("Writing %s" % full_output_path)
    dump_file = scanslib.Outfile(full_output_path)
    dump_file.flush(batch)
    dump_file.compress()
    if s3_bucket_name is not None:
        time.sleep(1)
        dump_file.upload_to_s3(s3_bucket_name)

end_time = datetime.now()

difftime = str(end_time - start_time)

print("Total time taken to download %s scans for %s: %s") % (str(counter),
                                                             env_date,
                                                             difftime)
