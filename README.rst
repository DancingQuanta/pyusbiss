===============================
pyusbiss
===============================

A Python module for interfacing with USB-ISS multifunction USB Communication Module

* Untested!
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

* For each operation mode, the instance of this module must pretend to be of other modules such as spidev for spi so it can be used to control various sensors via their classes.

Applications
------------

* Alphasense OPCs via `dhhagan's py-opc module <https://github.com/dhhagan/py-opc/>`_ 

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Inspired by:

.. _`Waggle's alphasense.py`: https://github.com/waggle-sensor/waggle/


