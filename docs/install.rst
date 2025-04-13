.. _installation:

Installation
============

MayaShaderLibrary
Minimum Version Required: Maya +2022 / Python +3.6

Download
--------

- Download/clone MayaShaderLibrary_ repository from github.
- If you are not familiar with github, download this `zip file`_

Maya Install
------------

- Copy/Paste or Unzip the contents into your preferred scripts location, or your maya scripts folder.

.. _MayaShaderLibrary: https://github.com/MaxRocamora/MayaShaderLibrary
.. _zip file: https://github.com/MaxRocamora/MayaShaderLibrary/zipball/master

Define Library Folder
---------------------

- Add the following environment variable to your Maya.env, this will be the folder where your shaders and preview files are stored.

**MAYA_SHADER_LIBRARY = your_install_directory\\library**

.. note:: Maya.env is usually located under "User/My Documents/Maya/2022"

.. note:: If you do not set this environment variable, the default location will be used, which is the "library" folder inside the MayaShaderLibrary folder.

Running the script
------------------

Create a shelf button with the following python code:

.. code-block:: python

	import msl
	msl.run()
