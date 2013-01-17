Introduction
============

PyCPUID reads the information available from the CPUID assembly instruction and
makes it available to any Python program.

It could be used to decide on some codepath based on whether the target computer
supports SSE2. 
::

    import pycpuid
    if pycpuid.HAS_SSE2:
        import foobar_sse2 as foobar
    else:
        import foobar

It is not the goal of PyCPUID to provide a full report of all CPUID information
available. It's merely a way to get raw access to the machine instruction from
within Python. Some functions are provided for translation to something human
readable, but this is far from complete. Full details on how to interpret the
raw data can be found in the application notes of `Intel`_ and `AMD`_.

Project maintained by `Flight Data Services`_ and released under the GNU Lesses 
General Public License (`LGPL-2.1`_).

Installation
------------

Package requires ``pip`` for installation.
::

    pip install PyCPUID

If you're doing this on Windows you'll need to make sure you have a C++ compiler
installed and properly configured.

Source Code
-----------

Source code is available from `GitHub`_:

* https://github.com/organizations/FlightDataServices/PyCPUID

Documentation
-------------

Documentation is available from the `Python Package Index`_:

* http://packages.python.org/PyCPUID/

Using PyCPUID
=============

There's not much to it, really. PyCPUID is just a bunch of module constants.
Just import the module and access the constants. The ``HAS_FOOBAR`` constants
are Boolean flags to indicate whether the feature is available. The function
``features()`` returns a list of all the available features as strings. There
are some other functions like ``vendor()`` and ``brand_string()`` you can use to
identify the CPU.
::

    import pycpuid
    print "has SSE2:", pycpuid.HAS_SSE2
    print "all availabe features:", pycpuid.features()
    print "brand string:", pycpuid.brand_string()

.. _Flight Data Services: http://www.flightdataservices.com/
.. _LGPL-2.1: http://www.opensource.org/licenses/lgpl-2.1.php
.. _GitHub: https://github.com/
.. _Python Package Index: http://pypi.python.org/
.. _Intel: http://www.intel.com/content/www/us/en/processors/processor-identification-cpuid-instruction-note.html
.. _AMD: http://support.amd.com/us/Embedded_TechDocs/25481.pdf

.. image:: https://cruel-carlota.pagodabox.com/95fea790ea9043d121f74b6c0d365eed
    :alt: githalytics.com
    :target: http://githalytics.com/FlightDataServices/PyCPUID
