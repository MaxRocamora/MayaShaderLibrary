.. _ui:

User Interface
==============

On this section you will find a detailed explanation of each action on the user interface.

..note:: Hover over any button to see what it does on the bottom status bar

User Interface Description
--------------------------

.. image:: https://github.com/MaxRocamora/MayaShaderLibrary/blob/master/scripts/ui/screenshot/uiAreasDetail.png?raw=true

1. Shader Info Area
Here is displayed the name of the shader, the maya node type, and user, pc name of who generate this shader. This is useful when you have MayaShaderLibrary installed over a network with a single shader repository.

2. Notes Areas
You can add/edit comments here, remember to press the save button to save (3) the changes on the comments.

Shader Category's
-----------------

4. To create a category
Go to menu Categorgy > Add New Category or use the ui button to create a new category.

5. To pin a category
Use the pin button to pin the category to the tabs.

6. To unpin category
Use the unpin button to remove a category from the tabs, this button dont delete the category from disk, just removes it from the tabs panel.

7. Browse category folder
Opens an explorer to the actual folder of the category

8. Refresh
Refresh the interface, this is usefull when the MayaShaderLibrary is used over a network with multiple users and you need to check for changes made by another user.


Shaders
-------

Shaders are represented as thumbnail icons on the selected category, to add a shaders, simply select any maya geometry with a shader on it, and press the green plus button. The shader will appear on the category tab.

9. Add Shader
Select a geometry to save his shader into current category selected.

Shader Menu
-----------

10. To access shader menu, right click on the thumbnail image of any shader on your category tab.

Each menu option explained below:

* Import into Scene
* Import and assing into selection
* Rename
* Browse
* Generate Thumnail
* Delete from lib

Menubar
-----------------

Options

Misc
----

The maya file used for the thumnails is located under:
*installDirectory\MayaShaderLibrary\maya\scene\thumbnail_scene.ma*

The shaders are stored under this location:
*installDirectory\MayaShaderLibrary\maya\shaders*