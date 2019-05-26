//Maya ASCII 2018ff09 scene
//Name: oxido_shader.ma
//Last modified: Sun, Feb 24, 2019 08:46:28 PM
//Codeset: 1252
requires maya "2018ff09";
requires "stereoCamera" "10.0";
requires -nodeType "aiStandardSurface" "mtoa" "3.0.1.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201807191615-2c29512b8a";
fileInfo "osv" "Microsoft Windows 7 Ultimate Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "shdBall";
	rename -uid "88C51F52-4C8C-4D39-F17C-57AC7D6C92CE";
createNode mesh -n "shdBallShape" -p "shdBall";
	rename -uid "690A8B9A-4016-BF6C-85C3-45AD0D599EAD";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode polySphere -n "polySphere1";
	rename -uid "436C4A1A-4CFD-8105-B57A-57A02A78F8C3";
createNode materialInfo -n "oxido_shader_materialInfo6";
	rename -uid "8F7FF0DF-46D6-2DF0-2224-F3B69A933449";
createNode shadingEngine -n "oxido_shader_aiStandardSurface1SG4";
	rename -uid "814CCF3A-4C38-4C2B-79C2-EC902292D731";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
createNode aiStandardSurface -n "oxido";
	rename -uid "8820A599-47F9-1ABE-C40C-11AAB303E8D3";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "36964E65-41BE-C680-138A-808C6A69983B";
	setAttr -s 19 ".lnk";
	setAttr -s 19 ".slnk";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 19 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "polySphere1.out" "shdBallShape.i";
connectAttr "oxido_shader_aiStandardSurface1SG4.msg" "oxido_shader_materialInfo6.sg"
		;
connectAttr "oxido.msg" "oxido_shader_materialInfo6.m";
connectAttr "oxido.msg" "oxido_shader_materialInfo6.t" -na;
connectAttr "oxido.out" "oxido_shader_aiStandardSurface1SG4.ss";
connectAttr "shdBallShape.iog" "oxido_shader_aiStandardSurface1SG4.dsm" -na;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "oxido_shader_aiStandardSurface1SG4.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "oxido_shader_aiStandardSurface1SG4.message" ":defaultLightSet.message";
connectAttr "oxido_shader_aiStandardSurface1SG4.pa" ":renderPartition.st" -na;
connectAttr "oxido.msg" ":defaultShaderList1.s" -na;
// End of oxido_shader.ma
