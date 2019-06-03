import haloscans
import time
import os
import re


class GetScans(object):
    def __init__(self, key, secret, api_host, api_port, batch_size,
                 target_date, scan_threads, enricher_threads):
        search_params = {"since": target_date, "sort_by": "created_at.asc"}

        self.integration = self.get_integration_string()
        self.h_s = haloscans.HaloScans(key, secret, api_host=api_host,
                                       api_port=api_port,
                                       max_threads=scan_threads,
                                       search_params=search_params,
                                       integration_name=self.integration)
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

    def get_integration_string(self):
        """Return integration string for this tool."""
        return "Halo-Scans-Archiver/%s" % self.get_tool_version()

    def get_tool_version(self):
        """Get version of this tool from the __init__.py file."""
        here_path = os.path.abspath(os.path.dirname(__file__))
        init_file = os.path.join(here_path, "__init__.py")
        ver = 0
        with open(init_file, 'r') as i_f:
            rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
            ver = rx_compiled.search(i_f.read()).group(1)
        return ver
