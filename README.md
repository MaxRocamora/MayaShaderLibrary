[![Message](https://img.shields.io/badge/Maya_Shader_Library-ffffff)]()
[![Message](https://img.shields.io/badge/Maya-2022-blue?logo=autodesk)]()
[![Message](https://img.shields.io/badge/Maya-2023-blue?logo=autodesk)]()
[![Message](https://img.shields.io/badge/Maya-2024-blue?logo=autodesk)]()
[![Documentation Status](https://readthedocs.org/projects/mayashaderlibrary/badge/?version=latest)](https://mayashaderlibrary.readthedocs.io/en/latest/?badge=latest)

# Maya Shader Library

A shading library tool to store and organize shaders in Autodesk Maya.
Create and Manage Categories to organize, save and load maya shaders.

See the [Documentation](https://mayashaderlibrary.readthedocs.io/en/latest/#) for installation & usage

*Maya +2022 Python 3 only*

----------------------------------
![ScreenShot](https://github.com/MaxRocamora/MayaShaderLibrary/blob/master/msl/resources/screenshot/tool.png)

![ScreenShot](https://github.com/MaxRocamora/MayaShaderLibrary/blob/master/msl/resources/screenshot/tool_ui.png)

# Features

- Create and Manage Categories to organize, save and load maya shaders.  
- Save and Load Shaders into a library.  
- Import shaders to scene or selected mesh.  
- Add custom thumbnail to shaders.  
- Add a note to shaders.  
- Generate a thumbnail image, using a provided scene file.  
- Resizable UI & Movable Toolbar.


# Folders

- Documentation (is online)  
*/docs*

- Saved Shaders Default Location  
*/library/shaders*

- Custom Location using environment variable  
*%LIBRARY%/shaders*

- Default Thumbnail Scene  
*/library/scene*
*%LIBRARY%/scene/thumbnail_scene.ma*

- Python Package root  
*/msl*


### Roadmap 2024...

- export arnold ai shader file (now is a .ma file only)
- update shader from scene (look for the shader in the scene and update the library.)
- show texture maps used for given shader
- copy maps to library repository / deploy maps into target folder
- import into selected mesh, ask for replace shader if exists
- fill library from selection: takes all shaders from selection and fills current category
- import custom image for shader thumbnail (maybe drag and drop?)