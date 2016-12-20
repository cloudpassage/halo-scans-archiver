import haloscans


class GetScans(object):
    def __init__(self, key, secret, batch_size, target_date):
        self.h_s = haloscans.HaloScans(key, secret,
                                       start_timestamp=target_date)
        self.enricher = haloscans.HaloScanDetails(key, secret)
        self.target_date = target_date
        self.batch_size = batch_size
        print("Scan retrieval initialized for date %s") % self.target_date

    def __iter__(self):
        batch = []
        for scan in self.h_s:
            if scan["created_at"].startswith(self.target_date):
                batch.append(self.enricher.get(scan["id"]))
                if len(batch) >= self.batch_size:
                    yield list(batch)
                    batch = []
            else:
                yield list(batch)
                print("No more scans for target day!")
                raise StopIteration
