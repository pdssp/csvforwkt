================
Getting starting
================

Install
-------

Make sure that Python 3.8 (or later) is available, and install the latest version of ``csv2forwkt`` using `pip <https://pip.pypa.io>`_\ ,

.. code-block:: shell

    $ pip install git+https://github.com/pole-surfaces-planetaires/csvforwkt.git
    $ cd csv2forwkt
    $ make


Running the software
--------------------

.. code-block:: shell

    csvforwkt --iau_report data/naifcodes_radii_m_wAsteroids_IAU2015.csv --iau_version 2015 --iau_doi doi:10.1007/s10569-017-9805-5

This will generate the file iau.wkt with all WKTs.
