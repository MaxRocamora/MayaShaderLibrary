.. _installation:

Installation
============

Download
--------

- Download/clone MayaShaderLibrary_ repository from gitHub.
- If you are not familiar with gitHub, download this `zip file`_

- Copy/Paste or Unzip the contents into your preferred scripts location, or your maya scripts folder.

.. _MayaShaderLibrary: https://github.com/MaxRocamora/MayaShaderLibrary
.. _zip file: https://github.com/MaxRocamora/MayaShaderLibrary/zipball/master

Maya Install
------------

- MayaShaderLibrary works on Maya 2017, 2018, and 2019
- Copy 'sanityChecker' folder into users/maya scripts folder

- Add the following environment variable to your Maya.env, this folder is where your shaders are stored. ::

	MAYA_SHADER_LIBRARY = your_install_directory\library

.. note:: Maya.env is usually located under User/My Documents/Maya/2018)

- Make sure to load the plugin '"ARCANE Tools ShaderLibrary 1.0"' from plugin manager once maya is restarted.

Maya plugin manager is located in maya menu under 'Windows' > 'Settings/Preferences' > 'Plug-in Manager'

Running the script
------------------

Create a shelf button with the following python code:

.. code-block:: python

	import msl.shader_library as maya_shader_library
	maya_shader_library.load()
