Installation
============

Dependencies
------------

.. note::

    The DataLab Windows installer package already include all those required
    libraries as well as Python itself.

.. include:: ../requirements.rst

.. note::

    Python 3.11 and PyQt5 are the reference for production release


How to install
--------------

Windows installer:
^^^^^^^^^^^^^^^^^^

DataLab is available as a stand-alone application for Windows,
which does not require any Python distribution to be installed.
Just run the installer and you're good to go!

.. image:: /images/shots/windows_installer.png

The installer package is available in the `Releases`_ section.
It supports automatic uninstall and upgrade feature (no need to uninstall
DataLab before runinng the installer of another version of the
application).

.. _Releases: https://github.com/Codra-Ingenierie-Informatique/DataLab/releases


Wheel package:
^^^^^^^^^^^^^^

On any operating system, using pip and the Wheel package is the easiest way to
install DataLab on an existing Python distribution:

.. code-block:: console

    $ pip install --upgrade DataLab-2.0.2-py2.py3-none-any.whl


Source package:
^^^^^^^^^^^^^^^

Installing DataLab directly from the source package is straigthforward:

.. code-block:: console

    $ python setup.py install
