Changelog
=========


v1.0
----
- Add integration_name string. [Paul Chang]


v0.18 (2018-06-20)
------------------

Changes
~~~~~~~
- Target date defaults to yesterday. [Ash Wilson]

  If no TARGET_DATE is specified, the prior day is set.


v0.17 (2018-03-19)
------------------

Changes
~~~~~~~
- Updated to use newer version of haloscans lib, now storing 100 scans
  per file. [Ash Wilson]
- Bumping halo-scans library version pin to v0.16. [Ash Wilson]


v0.13 (2017-12-15)
------------------
- Tuning down threads to 1. [mong2]


v0.9 (2016-12-22)
-----------------

New
~~~
- Implement thread pool for initial enrichment of scans. Big performance
  improvement. [Ash Wilson]
- Downloads one day of scans from Halo API.  Optionally uploads those
  scans to S3. [Ash Wilson]


