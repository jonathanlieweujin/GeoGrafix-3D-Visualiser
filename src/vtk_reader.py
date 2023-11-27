import re
from vtkmodules.all import *
from PyQt5.QtWidgets import QFileDialog

import os

class VtkReader: #ply stl obj fbx vtk
    def reader(self, format = 3):
        if format is not None:

            dialog = QFileDialog()
            option = QFileDialog.Options()

            if format == 1:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'Stanford (*.ply)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                actor_reader = vtkPLYReader()
                outliner_name = "PLY_Import"
                
            elif format == 2:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'Stl (*.stl)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                actor_reader = vtkSTLReader()
                outliner_name = "STL_Import"
            elif format == 3:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'Wavefront (*.obj)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                actor_reader = vtkOBJReader()
                outliner_name = "OBJ_Import"
            elif format == 4:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'Vtp (*.vtp)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                actor_reader = vtkXMLPolyDataReader()
                outliner_name = "VTP_Import"
            elif format == 5:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'Vtk (*.vtk)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                actor_reader = vtkPolyDataReader()
                outliner_name = "VTK_Import"

            elif format == 6:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'DICOM (*.dcm)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                else:
                    dir = os.path.dirname(import_file[0])
                    name = os.path.basename(dir)
                    outliner_name = "DICOM_Import"

                    actor_reader = vtkDICOMImageReader()
                    actor_reader.SetDirectoryName (dir)
                    actor_reader.SetDataScalarTypeToUnsignedShort()
                    actor_reader.UpdateWholeExtent()
                    actor_reader.Update()

                    image_data = vtkImageData()
                    image_data.ShallowCopy(actor_reader.GetOutput())

                    volume_mapper = vtkSmartVolumeMapper()
                    volume_mapper.SetBlendModeToComposite()
                    volume_mapper.SetRequestedRenderModeToGPU()
                    volume_mapper.SetInputData(image_data)

                    volume_property = vtkVolumeProperty()
                    volume_property.ShadeOn()
                    volume_property.SetInterpolationTypeToLinear()
                    volume_property.SetAmbient(0.1)
                    volume_property.SetDiffuse(0.9)
                    volume_property.SetSpecular(0.2)
                    volume_property.SetSpecularPower(10.0)

                    colour = vtkColorTransferFunction()
                    colour.AddRGBPoint(-750, 0.08, 0.05, 0.03)
                    colour.AddRGBPoint(-350, 0.39, 0.25, 0.16)
                    colour.AddRGBPoint(-200, 0.80, 0.80, 0.80)
                    colour.AddRGBPoint(2750, 0.70, 0.70, 0.70)
                    colour.AddRGBPoint(3000, 0.35, 0.35, 0.35)
                    volume_property.SetColor(colour)

                    gradient_opacity = vtkPiecewiseFunction()
                    gradient_opacity.AddPoint(0, 0)
                    gradient_opacity.AddPoint(2000, 1)
                    volume_property.SetGradientOpacity(gradient_opacity)

                    scalar_opacity = vtkPiecewiseFunction()
                    scalar_opacity.AddPoint(-800,0)
                    scalar_opacity.AddPoint(-750,1)
                    scalar_opacity.AddPoint(-350,1)
                    scalar_opacity.AddPoint(-300,0)
                    scalar_opacity.AddPoint(-200,0)
                    scalar_opacity.AddPoint(-100,1)
                    scalar_opacity.AddPoint(1000,0)
                    scalar_opacity.AddPoint(2750,0)
                    scalar_opacity.AddPoint(2976,1)
                    scalar_opacity.AddPoint(3000,0)
                    volume_property.SetScalarOpacity(scalar_opacity)

                    volume = vtkVolume()
                    volume.SetMapper(volume_mapper)
                    volume.SetProperty(volume_property)

                    return volume, name, outliner_name

                    # volume_mapper = vtkSmartVolumeMapper()
                    # volume_property = vtkVolumeProperty()
                    # colour = vtkColorTransferFunction()
                    # volume = vtkVolume()   

            elif format == 7:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', 'MetaImage (*.mhd)', 
                                                    options=option)
                if import_file[0] == "":
                    return None, None, None
                actor_reader = vtkMetaImageReader()
                outliner_name = "MHD_Import"

                if import_file[0]:
                    dir: str = import_file[0]

                    # print(dir)
                    name: str = os.path.basename(dir)
                    name, __ = os.path.splitext(name)
                    
                    actor_reader.SetFileName(dir)
                    actor_reader.Update()

                    # locator = vtkMergePoints()
                    # locator.SetDivisions(64, 64, 92)
                    # locator.SetNumberOfPointsPerBucket(2)
                    # locator.AutomaticOff()
                    # locator.Update()
                    iso = vtkMarchingCubes()
                    iso.SetInputConnection(actor_reader.GetOutputPort())
                    iso.ComputeGradientsOn()
                    iso.ComputeScalarsOff()
                    iso.SetValue(0, 1150)
                    # iso.SetLocator(locator)
                    iso.Update()

                    iso_mapper = vtkPolyDataMapper()
                    iso_mapper.SetInputConnection(iso.GetOutputPort())
                    iso_mapper.ScalarVisibilityOff()

                    actor = vtkActor()
                    actor.SetMapper(iso_mapper)

                    return actor, name, outliner_name

            elif format == 8:
                import_file = dialog.getOpenFileName(None, 'Import Model', '', '3D Scene (*.3ds)', 
                                                options=option)
                if import_file[0] == "":
                    return []
                actor_reader = vtk3DSImporter()

                if import_file[0]:
                    dir: str = import_file[0]
                    
                    actor_reader.SetFileName(dir)
                    actor_reader.ComputeNormalsOn()
                    
                    renderer = vtkRenderer()
                    render_window = vtkRenderWindow()
                    render_window.AddRenderer(renderer)
                    actor_reader.SetRenderWindow(render_window)
                    actor_reader.Update()

                    actor_collection = renderer.GetActors() 
                    actor_collection.InitTraversal()
                    actor = actor_collection.GetNextActor()
                    actor_collection_list = []

                    while actor:
                        actor_collection_list.append(actor)
                        actor = actor_collection.GetNextActor()
                    
                    actor_list = []
                    
                    for i in range (len(actor_collection_list)):
                        actor = actor_collection_list[i]
                        if actor.GetClassName() == "vtkAxesActor" or actor.GetClassName() == "vtkOpenGLLight":
                            pass
                        else:
                            actor_list.append(actor)

                    return actor_list
                    # return actor, name, outliner_name

            elif format == 9 or format == 10:
                import_file = dialog.getOpenFileName(None, 'Import Model', './models/data/', 'MHD (*.mhd)', 
                                                options=option)
                if import_file[0] == "":
                    return None, None, None
                else:
                    dir: str = import_file[0]
                    name: str = os.path.basename(dir)
                    name, __ = os.path.splitext(name)

                    actor_reader = vtkMetaImageReader()
                    actor_reader.SetFileName(dir)
                    # reader_volume.SetDataScalarType(VTK_UNSIGNED_SHORT)
                    # reader_volume.SetFileDimensionality(3)
                    # reader_volume.SetDataExtent ( 0,255, 0,255, 0,576)
                    # reader_volume.SetDataSpacing( 1,1,1 )
                    # reader_volume.SetNumberOfScalarComponents( 1 )
                    # reader_volume.SetDataByteOrderToBigEndian()
                    actor_reader.Update()

                    if format == 9:
                        outliner_name = "IsoS_ContourFilter"
                        marching = vtkContourFilter()
                    elif format == 10:
                        outliner_name = "IsoS_MarchingCubes"
                        marching = vtkMarchingCubes()
                    # marching.SetInputData(Grid)
                    # marching.SetValue(0, 0.5)
                    # marching.Update()
                    marching.SetInputConnection(actor_reader.GetOutputPort())
                    marching.ComputeGradientsOn()
                    marching.ComputeScalarsOff()
                    marching.SetValue(0, 1150)
                    marching.Update()
                    
                    # Take the isosurface data and create geometry
                    mapper = vtkPolyDataMapper()
                    mapper.SetInputConnection(marching.GetOutputPort())
                    # geoBoneMapper.ScalarVisibilityOff()
                    mapper.Update()
                
                    actor = vtkActor()
                    # actor.SetNumberOfCloudPoints(1000000)
                    actor.SetMapper(mapper)
                    return actor, name, outliner_name

            if import_file[0]:
                dir: str = import_file[0]

                # print(dir)
                name: str = os.path.basename(dir)
                name, __ = os.path.splitext(name)
                
                actor_reader.SetFileName(dir)
                actor_reader.Update()
                polydata = actor_reader.GetOutput()

                polydata.GetPointData().SetScalars(None)
                
                mapper = vtkPolyDataMapper()
                mapper.SetInputData(polydata)

                actor = vtkActor()
                actor.SetMapper(mapper)

                if format == 3:
                    material_file_path = os.path.splitext(import_file[0])[0] + ".mtl"
                    if os.path.isfile(material_file_path):
                        diffuse_colour = self.readMTLFile(material_file_path)
                        actor.GetProperty().SetColor(*diffuse_colour)
                else:
                    material_file_path = os.path.splitext(import_file[0])[0] + ".txt"
                    if os.path.isfile(material_file_path):
                        location, rotation, scale, colour = self.readOtherProperties(material_file_path)
                        actor.SetPosition(location[0],
                                          location[1],
                                          location[2])
                        actor.SetOrientation(rotation[0],
                                          rotation[1],
                                          rotation[2])
                        actor.SetScale(scale[0],
                                          scale[1],
                                          scale[2])
                        actor.GetProperty().SetColor(*colour)
                return actor, name, outliner_name

            else:
                pass

    def readOtherProperties(self, file_path: str):
        with open(file_path, 'r') as file:
            content = file.read()

        # Define regular expression patterns to extract values
        pattern_location = re.compile(r'Location \[([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\]')
        pattern_rotation = re.compile(r'Rotation \[([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\]')
        pattern_scale = re.compile(r'Scale \[([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\]')
        pattern_colour = re.compile(r'Colour \(([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\)')

        # Match the patterns in the content
        match_location = pattern_location.search(content)
        match_rotation = pattern_rotation.search(content)
        match_scale = pattern_scale.search(content)
        match_colour = pattern_colour.search(content)

        # Extract values from the matches
        location = [float(match_location.group(i)) for i in range(1, 4)] if match_location else None
        rotation = [float(match_rotation.group(i)) for i in range(1, 4)] if match_rotation else None
        scale = [float(match_scale.group(i)) for i in range(1, 4)] if match_scale else None
        colour = [float(match_colour.group(i)) for i in range(1, 4)] if match_colour else None

        return location, rotation, scale, colour

    def readMTLFile(self, file_path: str):
        try:
            with open(file_path, 'r') as mtl_file:
                mtl_content = mtl_file.read()

                # Initialize a flag to indicate when to start keeping lines
                start_keeping_lines = False

                # Process each line
                lines_after_target = []
                for line in mtl_content.splitlines():
                    if not line.strip() or line.strip().startswith("#"):
                        continue
                    start_keeping_lines = True
                    if start_keeping_lines:
                        lines_after_target.append(line)

                # Join the lines back together
                mtl_content = '\n'.join(lines_after_target)

               # Initialize variables
                diffuse_color = [1,1,1]

                print(mtl_content.splitlines())
                # Process each line
                for line in mtl_content.splitlines():
                    if line.lower().startswith("kd"):
                        # Extract RGB values and convert to floats
                        diffuse_color = [float(value) for value in line.split()[1:]]

            return diffuse_color
        except:
            return [1,1,1]
