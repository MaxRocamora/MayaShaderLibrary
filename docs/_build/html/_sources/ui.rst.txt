.. _ui:

User Interface
==============

On this section you will find a detailed explanation of each action on the user interface.

.. note:: Hover over any button to see what it does on the bottom status bar

User Interface Description
--------------------------

.. image:: https://github.com/MaxRocamora/MayaShaderLibrary/blob/master/msl/ui/screenshot/uiAreasDetail.png?raw=true

1. Shader Info Area

Here is displayed the name of the shader, the maya node type, and user, pc name of who generate this shader.
This is useful when you have MayaShaderLibrary installed over a network with a single shader repository.

2. Notes Area

You can add/edit comments here, remember to press the save button to save (3) the changes on the comments.

Shader Category's
-----------------

4. Create a category

Go to menu Category > Add New Category or use the ui button to create a new category.

5. Pin a category

Use the pin button to pin the category to the tabs.

6. Unpin category

Use the unpin button to remove a category from the tabs, this button do not delete the category from disk,
just removes it from the tabs panel.

7. Browse category folder

Opens an explorer to the actual folder of the category

8. Refresh

Refresh the interface, this is useful when the MayaShaderLibrary is used over a network with multiple users
and you need to check for changes made by another user.


Shaders
-------

Shaders are represented as thumbnail icons on the selected category, to add a shaders,
simply select any maya geometry with a shader on it, and press the green plus button.
The shader will appear on the category tab.

9. Add Shader

Select a geometry to save his shader into current category selected.

Shader Menu
-----------

10. To access shader menu, right click on the thumbnail image of any shader on your category tab.

Each menu option explained below:

* Import into Scene
	Adds selected shader to the maya hypershade

* Import and assign into selection
	Adds selected shader to the maya hypershade and assign it to selected object

* Rename
	Renames the shader

* Browse
	Open explorer into shader folder

* Generate Thumbnail
	Generates thumbnail image for this shader, using the default lightRig maya file [*uses arnold render*]

* Delete from lib
	Deletes this shader from disk

Menubar
-------

* Help
    Opens a browser to this documentation.


.. note::
	The maya file used for render the thumbnail image is located on this location: 
	*installDirectory\\MayaShaderLibrary\\library\\scene\\thumbnail_scene.ma*

.. note::
	The shaders are stored on this location: 
	*installDirectory\\MayaShaderLibrary\\library\\shaders*
