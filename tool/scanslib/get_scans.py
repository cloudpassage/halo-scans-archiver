import haloscans
import time


class GetScans(object):
    def __init__(self, key, secret, api_host, api_port, batch_size,
                 target_date, scan_threads, enricher_threads):
        search_params = {"since": target_date, "sort_by": "created_at.asc"}
        self.h_s = haloscans.HaloScans(key, secret, api_host=api_host,
                                       api_port=api_port,
                                       max_threads=scan_threads,
                                       search_params=search_params)
        self.target_date = target_date
        self.batch_size = batch_size
        self.max_threads = scan_threads
        print("Scan retrieval initialized for date %s") % self.target_date

    def __iter__(self):
        batch = []
        for scan in self.h_s:
            if scan["created_at"].startswith(self.target_date):
                batch.append(scan)
                if len(batch) >= self.batch_size:
                    yield list(batch)
                    batch = []
            else:
                yield list(batch)
                print("No more scans for target day!\nShutting down tool...")
                self.h_s.shutdown = True
                time.sleep(60)
                raise StopIteration
