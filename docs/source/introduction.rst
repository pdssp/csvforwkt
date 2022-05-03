============
Introduction
============

This document describes the purpose, objectives and commands to run csvforwkt.

Purpose
-------
Users now want more than just a static archive to explore data. They need
services to provide data.  Indeed, these services must be interoperable in
order to avoid that users have to access by themselves to each
database to search and retrieve the whole data set for their research.

The primary motivations for the development, compliance, and adoption of global
standards are to support interoperability between spatial data products and
interoperability between analysis methods.

Geodetic coordinate reference systems provide the basic positional framework on
which all data services are based.

The recommended planetary geodetic coordinate systems and associated coordinate
reference frames are updated every three years by the IAU Working Group on
Cartographic Coordinates and Rotational Elements.

This document describes a software allowing to transcribe the orbital
parameters of the planets and the coordinate frames defined by the IAU in a
description language allowing to be used by many softwares.


Context
-------

The figure, as below, describes the context of the generation of the WKTs.

.. uml::
   :caption: csvforwkt context

   package "IAU" {
   [physical parameters in PDF report]
   [CRS definition]
   }

   package "OGC" {
      [WKT-CRS standard]
   }

   package "USGS" {
   [CRS identifier]
   [transformation to CSV]
   }

   package "csvforwkt" {
   [projection definition]
   [transformation to WKTs]
   }

   [WKT-CRS standard] --> [projection definition]
   [WKT-CRS standard] --> [transformation to WKTs]

   [CRS definition] --> [CRS identifier]
   [physical parameters in PDF report] --> [transformation to CSV]
   [transformation to CSV] --> [transformation to WKTs]
   [CRS identifier] --> [transformation to WKTs]
   [CRS definition] --> [transformation to WKTs]
   [projection definition] --> [transformation to WKTs]

IAU provides the physical parameters for the oribits and the definition of
the coordinate reference system.

The plysical parameters are transformed by USGS as CSV file. In addition,
USGS provide a mechanism of identifiers according to the following inputs :
body, reference frame of the body and projected reference frame

OGC provides the standard for describing the coordinate reference systems.

Based on OGC standard, IAU definition of the coordinate reference systems,
mechanism of identifier provided by USGS and the physical parameters as
CSV file, wktforcsv software povides the different coordinate reference
systems of each body in the WKT-CRS description.
