.. _guide:

QuickGuide
==========

See :ref:`installation` for details on how to install and run this tool.

- Once you load the tool you should see the interface.

.. image:: https://github.com/MaxRocamora/MayaShaderLibrary/blob/master/msl/ui/screenshot/tool.png?raw=true

Categories
----------

The MayaShaderLibrary works by creating Categories, inside each category you will save/load your shaders.

- Categories will be created and listed, but not displayed until you 'pin' them to the interface.
- To remove a category from the ui, double click on the category name.

Shaders
-------

Save shaders to disk by selecting a mesh in your scene and press the 'add shader' button,
once saved the shader should appear in the category.

- To load a shader, right click on the shader icon and select load shader, the shader will be added to the hypershade.
- If you choose load and assign, the shader will be imported and assigned to your current selected object if possible.

Shader Notes
------------

For adding or editing comments on a shader, use the text box on the lower left area, and press 'save' button.

.. note::
	The shaders are stored on this location: 
	*installDirectory\\MayaShaderLibrary\\library\\shaders*

Shader Context Menu
-------------------

* Import into Scene
	Adds selected shader to the maya hypershade

* Import and assign into selection
	Adds selected shader to the maya hypershade and assign it to selected object

* Rename
	Renames the shader

* Browse
	Open explorer into shader folder

* Generate Thumbnail
	Generates thumbnail image for this shader

* Delete from lib
	Deletes this shader from disk


Thumbnails
----------

| You can generate a thumbnail image using arnold, right click on a shader and select 'generate thumbnail'.
| To edit this file, go to the top menu a select 'Options' > 'Open Thumbnail LightRig File'

.. note::
	The maya file used for render the thumbnail image is located on this location: 
	*installDirectory\\MayaShaderLibrary\\library\\scene\\thumbnail_scene.ma*