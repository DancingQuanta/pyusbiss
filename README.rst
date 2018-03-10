===============================
pyusbiss
===============================

A Python API module for interfacing with USB-ISS multifunction USB
Communication Module.

From the `USB-ISS's webpage`_:

  The USB-ISS Multifunction USB Communications Module provides a complete
  interface between your PC and the I2C bus, SPI bus, a Serial port and general
  purpose Analogue Input or Digital I/O.
  The module is powered from the USB.
  Operating voltage is selectable between 3.3v and 5v and can supply up to
  80mA at 5v for external circuitry from a standard 100mA USB port.

* Python 3 (2 TODO)
* Requires pyserial_
* Free software: MIT license
* Documentation: https://pyusbiss.readthedocs.io.

Features
--------

Planned features
****************

* Configure USB-ISS to different operating modes; I2C, SPI, I/O and serial

  * For each mode, the API will mimic the popular APIs such as `py-spidev`_ for
    SPI by having same method and properties names. These names will be used in
    duck typing.
    This will ensure miminal adaption of applications wishing to use USB-ISS
    for prototyping and testing.

* Query status of USB-ISS
* Send bytes to and read from components via USB-ISS

Current implementation
**********************

* The SPI mode is implemented with following methods and properties

  * Methods

    * ``xfer`` - send N bytes and read N bytes back.

  * Properties

    * ``mode`` - SPI modes. Please note that USB-ISS's SPI modes don't match up
      with official SPI modes. Use official SPI mode numbers and the API will
      configure the USB-ISS correctly.

* Other modes are not implemented.

Installation
------------

::

  pip install pyusbiss

Usage
-----

* USBISS only

Connect to your USB-ISS and get information about your USB-ISS.

::

  from usbiss.usbiss import USBISS

  port = 'COM4' # Windows
  port = '/dev/ttyACM0' # Linux

  cxn = USBISS(port)
  print(repr(cxn)))

* SPI mode

Initiate USB-ISS with SPI mode and open a port.

::

  from usbiss.spi import SPI

  spi = SPI(port)

  spi.mode = 1
  spi.max_speed_hz = 500000

  print(repr(spi._usbiss))

  # SPI transaction

  response = spi.xfer([0x00, 0x00])

* I2C mode

  TODO

* I/O mode

  TODO

* Serial mode

  TODO

More Information
----------------

* `USB-ISS'S webpage`_

Applications
------------

* Alphasense OPC via dhhagan's py-opc_ module using the SPI protocol.

Credits
-------

The project was developed during a NERC's placement at University of Leeds.

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

Inspired by `Waggle's alphasense.py`_, where most of USB-ISS functions were
copied over.

.. _`USB-ISS's webpage`: https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm
.. _pyserial: https://pypi.python.org/pypi/pyserial
.. _py-spidev: https://pypi.python.org/pypi/spidev
.. _py-opc: https://pypi.python.org/pypi/py-opc
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Waggle's alphasense.py`: https://github.com/waggle-sensor/waggle
