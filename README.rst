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

Installation
------------

- Install from setup.py

  python setup.py install


Usage
-----

Initiate with SPI mode and opening port

  usb = usbiss.USBISS(port, 'spi', spi_mode=2, freq=500000)

  usb.open()

  print(usb.get_iss_info())


More Information
----------------
https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm#Response Bytes

TODO
----

* SPI mode is nearly implemented and other operating modes needs to be added as well. 
* Any future addition of operating modes must have same method names as the hardware libraries, eg, xfer from spidev must be used in this module.

Applications
------------

* Alphasense OPCs via `dhhagan's py-opc module <https://github.com/dhhagan/py-opc/>`_ using SPI protocol.

Credits
-------

The project was developed during a NERC's placement at University of Leeds.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Inspired by `Waggle's alphasense.py`_, where most of USB-ISS functions was copied over.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Waggle's alphasense.py`: https://github.com/waggle-sensor/waggle

