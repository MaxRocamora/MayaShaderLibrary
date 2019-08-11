.. _installation:

Installation
============

Download
--------

- Download/clone MayaShaderLibrary_ repository from gitHub.
- If you are not familiar with gitHub, download this `zip file`_

- Copy/Paste or Unzip the contents into your preferred scripts location.

.. _MayaShaderLibrary: https://github.com/MaxRocamora/MayaShaderLibrary
.. _zip file: https://github.com/MaxRocamora/MayaShaderLibrary/zipball/master

Maya Install
------------

- MayaShaderLibrary works on Maya 2017, 2018, and 2019
- Add the following two environment variables to your Maya.env file, replacing 'installDirectory' with the location where you download/unzip the repository. ::

	MAYA_PLUG_IN_PATH = installDirectory\\MayaShaderLibrary\\shaderLibrary\\plugin\\maya
	ARCANE_SHADER_LIBRARY = installDirectory

.. note:: Maya.env is usually located under User/My Documents/Maya/2018)

- Make sure to load the plugin '"ARCANE Tools ShaderLibrary 1.0"' from plugin manager once maya is restarted.

Maya plugin manager is located in maya menu under 'Windows' > 'Settings/Preferences' > 'Plug-in Manager'
