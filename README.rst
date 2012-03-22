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

Installation
------------

Package requires ``pip`` for installation.
::

    pip install PyCPUID

If you're doing this on Windows you'll need to make sure you have a C++ compiler
installed and properly configured.

Using PyCPUID
-------------

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

Get the Code
------------

* https://github.com/FlightDataServices/PyCPUID

.. _Flight Data Services: http://www.flightdataservices.com/
.. _Intel: http://www.intel.com/assets/pdf/appnote/241618.pdf
.. _AMD: http://www.amd.com/us-en/assets/content_type/white_papers_and_tech_docs/25481.pdf

