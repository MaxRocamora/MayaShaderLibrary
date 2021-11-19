.. _installation:

Installation
============

MayaShaderLibrary tested on Maya 2017, 2018, and 2019, 2022
Supports Python 2.7/3.7

Download
--------

- Download/clone MayaShaderLibrary_ repository from github.
- If you are not familiar with github, download this `zip file`_

- Copy/Paste or Unzip the contents into your preferred scripts location, or your maya scripts folder.

.. _MayaShaderLibrary: https://github.com/MaxRocamora/MayaShaderLibrary
.. _zip file: https://github.com/MaxRocamora/MayaShaderLibrary/zipball/master

Maya Install
------------

- Add the following environment variable to your Maya.env
- This will be the folder where your shaders and preview files are stored.

*MAYA_SHADER_LIBRARY = your_install_directory\\library*

.. note:: Maya.env is usually located under "User/My Documents/Maya/2018"

Running the script
------------------

Create a shelf button with the following python code:

.. code-block:: python

	import msl.shader_library as maya_shader_library
	maya_shader_library.load()
