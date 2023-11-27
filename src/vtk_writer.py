import os
import numpy as np
from vtkmodules.all import *
from PyQt5 import QtWidgets

class VtkWriter: #ply stl obj fbx vtk
        def singleWriter(self, actor: vtkActor = None, name: str = None, format = 3):
                
                if actor is not None:
                        self.actor = actor
                        self.actor_name = name

                if actor.GetClassName() == "vtkVolume":   
                        msg_box = QtWidgets.QMessageBox()
                        msg_box.setIcon(msg_box.Warning)
                        msg_box.setWindowTitle("Warning")
                        msg_box.setText("Currently unable to export volume\n"
                                        f"{self.actor_name}")
                        msg_box.setStandardButtons(msg_box.Ok)
                        result = msg_box.exec_()
                        if result == msg_box.Ok:
                                return
                        return
                
                if format == 1:
                        options = QtWidgets.QFileDialog.Options()
                        options |= QtWidgets.QFileDialog.DontUseNativeDialog
                        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", f"./export/{self.actor_name}", 
                                                                        "Stanford (*.ply)", options=options)
                        if file_path == "":
                                return
                        self.writePLY(file_path) 
                elif format == 2:
                        options = QtWidgets.QFileDialog.Options()
                        options |= QtWidgets.QFileDialog.DontUseNativeDialog
                        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", f"./export/{self.actor_name}", 
                                                                        "Stl (*.stl)", options=options)
                        if file_path == "":
                                return
                        self.writeSTL(file_path) 
                elif format == 3:
                        options = QtWidgets.QFileDialog.Options()
                        options |= QtWidgets.QFileDialog.DontUseNativeDialog
                        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", f"./export/{self.actor_name}", 
                                                                        "Wavefront (*.obj)", options=options)
                        if file_path == "":
                                return
                        self.writeOBJ(file_path) 
                elif format == 4:
                        options = QtWidgets.QFileDialog.Options()
                        options |= QtWidgets.QFileDialog.DontUseNativeDialog
                        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", f"./export/{self.actor_name}", 
                                                                        "Vtp (*.vtp)", options=options)
                        if file_path == "":
                                return
                        self.writeVTP(file_path) 
                elif format == 5:
                        options = QtWidgets.QFileDialog.Options()
                        options |= QtWidgets.QFileDialog.DontUseNativeDialog
                        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", f"./export/{self.actor_name}", 
                                                                        "Vtk (*.vtk)", options=options)
                        if file_path == "":
                                return
                        self.writeVTK(file_path)

                if format != 3:
                        self.saveProperties(file_path) 

        def multipleWriter(self, actors_list: list = None, name_list: list = None, format = 3):
                
                folder_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder', './export')
                if folder_path == "":
                        return
                folder_path += "/"

                for i in range(len(actors_list)):
                        self.actor = actors_list[i]
                        actor_name = name_list[i]

                        if self.actor.GetClassName() == "vtkVolume":   
                                msg_box = QtWidgets.QMessageBox()
                                msg_box.setIcon(msg_box.Warning)
                                msg_box.setWindowTitle("Warning")
                                msg_box.setText("Currently unable to export volume\n"
                                                f"{actor_name}")
                                msg_box.setStandardButtons(msg_box.Ok)
                                result = msg_box.exec_()
                                if result == msg_box.Ok:
                                        continue
                                continue

                        name = folder_path + f"{actor_name}"
                        if format == 1:
                                self.writePLY(name) 
                        elif format == 2:
                                self.writeSTL(name)
                        elif format == 3:
                                self.writeOBJ(name)
                        elif format == 4:
                                self.writeVTP(name) 
                        elif format == 5:
                                self.writeVTK(name)
                        if format != 3:
                                self.saveProperties(name) 

        def writeVTK(self, file_path):
                exporter = vtkPolyDataWriter()
                exporter.SetFileName(file_path + ".vtk")

                mapper = self.actor.GetMapper()
                mapper.Update()
                polydata = vtkPolyData()
                polydata.ShallowCopy(mapper.GetInput())
        
                exporter.SetInputData(polydata)
                exporter.Write()

        def writePLY(self, file_path):
                exporter = vtkPLYWriter()
                exporter.SetFileName(file_path)

                mapper = self.actor.GetMapper()
                mapper.Update()
                polydata = vtkPolyData()
                polydata.ShallowCopy(mapper.GetInput())
        
                exporter.SetInputData(polydata)
                exporter.Write()

        def writeSTL(self, file_path):
                exporter = vtkSTLWriter()
                exporter.SetFileName(file_path + ".stl")

                mapper = self.actor.GetMapper()
                mapper.Update()
                polydata = vtkPolyData()
                polydata.ShallowCopy(mapper.GetInput())
        
                exporter.SetInputData(polydata)
                exporter.Write()
        
        def writeOBJ(self, file_path):
                exporter = vtkOBJExporter()
                exporter.SetInput(self.getRenderWindow())
                exporter.SetFilePrefix(file_path)
                exporter.Write()

        def writeVTP(self, file_path):
                exporter = vtkXMLPolyDataWriter()
                exporter.SetFileName(file_path + ".vtp")

                mapper = self.actor.GetMapper()
                mapper.Update()
                polydata = vtkPolyData()
                polydata.ShallowCopy(mapper.GetInput())
        
                exporter.SetInputData(polydata)
                exporter.SetDataModeToAscii()
                exporter.Write()

        def getRenderWindow(self):

                renderer = vtkRenderer()
                renderer.AddActor(self.actor)
                render_window = vtkRenderWindow()
                render_window.AddRenderer(renderer)

                return render_window
        
        def saveProperties(self, file_path: str):

                text = ""
                if (self.actor is not None):
                        location = [self.actor.GetPosition()[0], 
                                    self.actor.GetPosition()[1],
                                    self.actor.GetPosition()[2]
                        ]
                        text += f"Location {location}"
                        rotation = [self.actor.GetOrientation()[0], 
                                    self.actor.GetOrientation()[1],
                                    self.actor.GetOrientation()[2]
                        ]
                        for i in range(len(rotation)):
                                if rotation[i] < 0:
                                        rotation[i] += 360
                                elif rotation[i] == -0.0:
                                        rotation[i] = 0.0
                        text += f"\nRotation {rotation}"
                        scale = [self.actor.GetScale()[0], 
                                    self.actor.GetScale()[1],
                                    self.actor.GetScale()[2]
                        ]
                        text += f"\nScale {scale}"
                        colour = self.actor.GetProperty().GetColor()
                        text += f"\nColour {colour}"

                        directory, _ = os.path.splitext(file_path)
                        directory = directory + ".txt"

                        # Write the text to the file
                        with open(directory, "w") as file:
                                file.write(text)

