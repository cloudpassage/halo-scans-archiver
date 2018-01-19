import haloscans
from multiprocessing.dummy import Pool as ThreadPool


class GetScans(object):
    def __init__(self, key, secret, api_host, api_port, batch_size,
                 target_date, scan_threads, enricher_threads):
        search_params = {"since": target_date, "sort_by": "created_at.asc"}
        self.h_s = haloscans.HaloScans(key, secret, api_host=api_host,
                                       api_port=api_port,
                                       max_threads=scan_threads,
                                       search_params=search_params)
        # The following statement governs behavior of enricher, including
        # the size of the thread pool that retrieves FIM findings.
        self.enricher = haloscans.HaloScanDetails(key, secret,
                                                  api_host=api_host,
                                                  api_port=api_port,
                                                  max_threads=enricher_threads)
        self.enricher.set_halo_session()
        self.target_date = target_date
        self.batch_size = batch_size
        self.max_threads = scan_threads
        print("Scan retrieval initialized for date %s") % self.target_date

    def __iter__(self):
        batch = []
        for scan in self.h_s:
            if scan["created_at"].startswith(self.target_date):
                batch.append(scan["id"])
                if len(batch) >= self.batch_size:
                    yield list(self.get_enriched_scans(batch))
                    batch = []
            else:
                yield list(self.get_enriched_scans(batch))
                print("No more scans for target day!")
                raise StopIteration

    def get_enriched_scans(self, scan_ids):
        """Map pages to threads, return results when it's all done."""
        pool = ThreadPool(self.max_threads)
        results = pool.map(self.enricher.get, scan_ids)
        pool.close()
        pool.join()
        return results
