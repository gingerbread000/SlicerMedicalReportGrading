cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(Medical-report-grading)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/ReportsScore")
set(EXTENSION_CATEGORY "tools")
set(EXTENSION_CONTRIBUTORS "LKG (AnyWare Corp.)")
set(EXTENSION_DESCRIPTION "This 3D Slicer plugin is designed to assist in reading images and corresponding reports, and providing options to rate the reports within the 3D Slicer platform.")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/ReportsScore.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/ReportsScore/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(showImageReports)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
