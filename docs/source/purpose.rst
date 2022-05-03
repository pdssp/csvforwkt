=======================
Purpose of the Software
=======================

Workflow
========

.. automodule:: csvforwkt

Positive longitudes
===================

.. automodule:: csvforwkt.crs

List of projections
===================

The list of supported projections is defined as below :

.. include:: list_projections.rst

How the IAU code is created
===========================

The IAU code is created according to this relation:

.. code-block::

    <naif_code> * 100 + <x_crs> + <code_projection>
    where :
        x_crs = 0 for SPHERE Ocentric
                1 for ELLIPSE Ographic
                2 for ELLIPSE Ocentric
                3 for TRIAXIAL Ographic
                4 for TRIAXIAL Ocentric

        code_projection is one of the code in the projection table
