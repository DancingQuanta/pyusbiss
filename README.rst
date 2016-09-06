===============================
pyusbiss
===============================

A Python module for interfacing with USB-ISS multifunction USB Communication Module

* Working for SPI using only xfer function, see description in spidev docs.
* Python 3 (2 todo)
* Free software: MIT license
* Documentation: https://pyusbiss.readthedocs.io.


Features
--------

* Configuring USB-ISS to different operating modes; I2C, SPI, I/O and serial
* Query status of USB-ISS
* Send bytes to components via USB-ISS and read from components via USB-ISS

More Information
----------------
https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm#Response Bytes

TODO
----

* SPI mode is nearly implemented and other operating modes needs to be added as well. 
* Any future addition of operating modes must have same method names as the hardware libraries, eg, xfer from spidev must be used in this module.

Applications
------------

* Alphasense OPCs via `dhhagan's py-opc module <https://github.com/dhhagan/py-opc/>`_ 

Credits
-------

The project was developed during a NERC's placement at University of Leeds.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Inspired by:

.. _`Waggle's alphasense.py`: https://github.com/waggle-sensor/waggle


