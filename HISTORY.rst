=======
History
=======

0.1.0 (2016-09-02)
------------------

* Initialised project

0.1.1 (2018-03-08)
------------------

* functional usbiss control and spi control.


0.1.2 (2018-03-08)
------------------

* Changed SPI mode scheme to official SPI scheme rather than USB-ISS scheme.
* Clarifies project mission in README.rst

0.2.0 (2018-03-10)
------------------

* Refactored the codebase so that each protocol can be controlled by its own
  class. This means a breaking change in the interface.
* SPI and USBISS support only in this release with updated usage.
* Added SPI tests.
* Updated README.rst with new interface.
