.. highlight:: shell

===============================
csvForWKT
===============================

.. image:: https://img.shields.io/github/v/tag/pole-surfaces-planetaires/csvforwkt
.. image:: https://img.shields.io/github/v/release/pole-surfaces-planetaires/csvforwkt?include_prereleases

.. image https://img.shields.io/github/downloads/pole-surfaces-planetaires/csvforwkt/total
.. image https://img.shields.io/github/issues-raw/pole-surfaces-planetaires/csvforwkt
.. image https://img.shields.io/github/issues-pr-raw/pole-surfaces-planetaires/csvforwkt
.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/pole-surfaces-planetaires/csvforwkt/graphs/commit-activity
.. image https://img.shields.io/github/license/pole-surfaces-planetaires/csvforwkt
.. image https://img.shields.io/github/forks/pole-surfaces-planetaires/csvforwkt?style=social


csvForWKT is a python script that creates a WKT-crs for solar system bodies.
The physical content of the WKT-crs comes from the IAU Working Group on
Cartographic Coordinates and Rotational Elements report.


Stable release
--------------

To install csvForWKT, run this command in your terminal:

.. code-block:: console

    $ pip install csvforwkt

This is the preferred method to install csvForWKT, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for csvForWKT can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/pole-surfaces-planetaires/csvforwkt

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/pole-surfaces-planetaires/csvforwkt/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make  # install in the system root
    $ make user # or Install for non-root usage


.. _Github repo: https://github.com/pole-surfaces-planetaires/csvforwkt
.. _tarball: https://github.com/pole-surfaces-planetaires/csvforwkt/tarball/master



Development
-----------

.. code-block:: console

        $ git clone https://github.com/pole-surfaces-planetaires/csvforwkt
        $ cd csvforwkt
        $ make prepare-dev
        $ source .csvforwkt
        $ make install-dev


To get more information about the preconfigured tasks:

.. code-block:: console

        $ make help

Usage
-----

To use csvForWKT:

    .. code-block:: console

        $ make
        $ csvforwkt --iau_report data/naifcodes_radii_m_wAsteroids_IAU2015.csv --iau_version 2015 --iau_doi doi://10.1007/s10569-017-9805-5


Run tests
---------

.. code-block:: console

        $make tests



Author
------
👤 **Jean-Christophe Malapert**


Contributors
------------
👤 **Trent Hare**


🤝 Contributing
---------------
Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/pole-surfaces-planetaires/csvforwkt/issues). You can also take a look at the [contributing guide](https://github.com/pole-surfaces-planetaires/csvforwkt/blob/master/CONTRIBUTING.rst)


📝 License
----------
This project is [GNU Lesser General Public License v3](https://github.com/pole-surfaces-planetaires/csvforwkt/blob/master/LICENSE) licensed.
