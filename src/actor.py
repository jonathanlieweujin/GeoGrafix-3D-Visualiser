import numpy as np
from vtkmodules.all import*
from actors_dict_list import*

class Actor:
    def setActorDict(self, dictionary_list: ActorsDictList = None, dictionary = None):
        if (dictionary_list is not None):
            self.actor_dictionary = dictionary_list.getActorDict(dictionary_list.getCurrentGeneratedID())
            # {
            #     "id": ...,
            #     "actor": ...,
            #     "name": ...,
            #     "source": ...,
            # }
        elif (dictionary is not None):
            self.actor_dictionary = dictionary
        if self.actor_dictionary == {}:
            self.setID(None)
            self.setActor(None)
            self.setName(None)
            self.setSource(None)
        else:
            self.setID(self.actor_dictionary["id"])
            self.setActor(self.actor_dictionary["actor"])
            self.setName(self.actor_dictionary["name"])
            self.setSource(self.actor_dictionary["source"])

    def getActorDict(self):
        return self.actor_dictionary

    # Resolution
    def getResolution(self):
        if self.actor is not None:
            source_class = self.getSource().GetClassName() 
            if source_class == "vtkConeSource" or source_class == "vtkCylinderSource":
                return self.getSource().GetResolution()
            elif source_class == "vtkSphereSource":
                return self.getSource().GetThetaResolution()
            elif source_class == "vtkDiskSource":
                return self.getSource().GetRadialResolution()
            elif source_class == "vtkTessellatedBoxSource":
                return self.getSource().GetLevel()
            elif source_class =="vtkParametricFunctionSource":
                return self.getSource().GetUResolution()
        else:
             return None

    def setResolution(self, offset, keyboard_bool):
        if self.actor is not None:
            source_class = self.getSource().GetClassName()
            colour = self.getActor().GetProperty().GetColor()
            if source_class == "vtkConeSource" or source_class == "vtkCylinderSource":
                if (keyboard_bool is True):
                    if (offset < 1):
                        offset = 1
                    self.getSource().SetResolution(round(offset))
                else:
                    value = self.getSource().GetResolution() + offset
                    if (value < 1):
                        value = 1
                    self.getSource().SetResolution(round(value))
            elif source_class == "vtkSphereSource":
                if (keyboard_bool is True):
                    if (offset < 1):
                        offset = 1
                    self.getSource().SetThetaResolution(round(offset))
                    self.getSource().SetPhiResolution(round(offset))
                else:
                    value = self.getSource().GetPhiResolution() + offset
                    if (value < 1):
                        value = 1
                    self.getSource().SetThetaResolution(round(value))
                    self.getSource().SetPhiResolution(round(value))
            elif source_class == "vtkDiskSource":
                if (keyboard_bool is True):
                    if (offset < 1):
                        offset = 1
                    self.getSource().SetRadialResolution(round(offset))
                    self.getSource().SetCircumferentialResolution(round(offset))
                else:
                    value = self.getSource().GetRadialResolution() + offset
                    if (value < 1):
                        value = 1
                    self.getSource().SetRadialResolution(round(value))
                    self.getSource().SetCircumferentialResolution(round(value))
            elif source_class == "vtkTessellatedBoxSource":
                if (keyboard_bool is True):
                    if (offset < 1):
                        offset = 1
                    self.getSource().SetLevel(round(offset))
                else:
                    value = self.getSource().GetLevel() + offset
                    # self.getSource().QuadsOn()
                    # self.getSource().SetBounds([-0.5, 0.5, -0.5, 0.5, -0.5, 0.5])
                    
                    # self.getSource().SetOutputPointsPrecision(vtkAlgorithm.DOUBLE_PRECISION)
                    if (value < 1):
                        value = 1
                    self.getSource().SetLevel(round(value))
            elif source_class == "vtkParametricFunctionSource":
                if (keyboard_bool is True):
                    if (offset < 1):
                        offset = 1
                    self.getSource().SetUResolution(round(offset))
                    self.getSource().SetVResolution(round(offset))
                    self.getSource().SetWResolution(round(offset))
                else:
                    value = self.getSource().GetUResolution() + offset
                    if (value < 1):
                        value = 1
                    self.getSource().SetUResolution(round(value))
                    self.getSource().SetVResolution(round(value))
                    self.getSource().SetWResolution(round(value))
            self.mapSourceToActor(self.getSource(), self.getActor())
            self.mapSourceToActor(self.getSource(), self.getActor())
            self.setColour(colour)
            self.getActorDict()["source"] = self.getSource()
            self.getActorDict()["actor"] = self.getActor()
        
    # Location
    def getLocation(self, mode):
        if self.actor is not None:
            if (mode == 1):
                return self.getActor().GetPosition()[0]
            elif (mode == 2):
                return self.getActor().GetPosition()[1]
            elif (mode == 3):
                return self.getActor().GetPosition()[2]
        else:
             return None
        
    def setLocation(self, mode, offset, keyboard_bool):
        if self.actor is not None:
            if (mode == 1):
                if (keyboard_bool is True):
                        self.getActor().SetPosition(offset, 
                                        self.getLocation(2), 
                                        self.getLocation(3))
                        # self.actor_guide.SetPosition(offset, 
                        #                 self.getLocation(2), 
                        #                 self.getLocation(3))
                else:
                    self.getActor().SetPosition(self.getLocation(1) + offset, 
                                        self.getLocation(2), 
                                        self.getLocation(3))
                    # self.actor_guide.SetPosition(self.getLocation(1) + offset, 
                    #                     self.getLocation(2), 
                    #                     self.getLocation(3))
            if (mode == 2):
                if (keyboard_bool is True):
                        self.getActor().SetPosition(self.getLocation(1), 
                                        offset, 
                                        self.getLocation(3))
                        # self.actor_guide.SetPosition(self.getLocation(1), 
                        #                 offset, 
                        #                 self.getLocation(3))
                else: 
                    self.getActor().SetPosition(self.getLocation(1), 
                                        self.getLocation(2) + offset, 
                                        self.getLocation(3))
                    # self.actor_guide.SetPosition(self.getLocation(1), 
                    #                     self.getLocation(2) + offset, 
                    #                     self.getLocation(3))
            if (mode == 3):
                if (keyboard_bool is True):
                    self.getActor().SetPosition(self.getLocation(1), 
                                        self.getLocation(2), 
                                        offset)
                    # self.actor_guide.SetPosition(self.getLocation(1), 
                    #                     self.getLocation(2), 
                    #                     offset)
                else:
                    self.getActor().SetPosition(self.getLocation(1), 
                                        self.getLocation(2), 
                                        self.getLocation(3) + offset)
                    # self.actor_guide.SetPosition(self.getLocation(1), 
                    #                     self.getLocation(2), 
                    #                     self.getLocation(3) + offset)
            self.getActorDict()["actor"] = self.getActor()

    # Rotation 
    def getRotation(self, mode):
        if self.actor is not None:
            if (mode == 4):
                angle = self.getActor().GetOrientation()[0]
            elif (mode == 5):
                angle = self.getActor().GetOrientation()[1]
            elif (mode == 6):
                angle = self.getActor().GetOrientation()[2]  
            if angle == -0.0:
                angle = 0.0
            return angle
        else:
            return None
        
    def setRotation(self, mode, offset, keyboard_bool):
        if self.actor is not None:
            angle = offset
            if (mode == 4):
                if (keyboard_bool is True): 
                        while (angle > 360):
                            angle -= 360
                        while (angle < 0):
                            angle += 360
                        if angle > 180 :
                            angle -= 360
                        self.getActor().SetOrientation(offset, 
                                        self.getRotation(5), 
                                        self.getRotation(6))
                else:
                    angle += self.getRotation(4)
                    if angle < 0 :
                            angle += 360
                    self.getActor().SetOrientation(angle, 
                                        self.getRotation(5), 
                                        self.getRotation(6))
            if (mode == 5):
                if (keyboard_bool is True):
                        while (angle > 360):
                            angle -= 360
                        while (angle < 0):
                            angle += 360
                        if angle > 180 :
                            angle -= 360
                        self.getActor().SetOrientation(self.getRotation(4), 
                                        offset, 
                                        self.getRotation(6))
                else: 
                    angle += self.getRotation(5)
                    if angle < 0 :
                            angle += 360
                    self.getActor().SetOrientation(self.getRotation(4), 
                                        angle, 
                                        self.getRotation(6))
            if (mode == 6):
                if (keyboard_bool is True):
                        while (angle > 360):
                            angle -= 360
                        while (angle < 0):
                            angle += 360
                        if angle > 180 :
                            angle -= 360
                        self.getActor().SetOrientation(self.getRotation(4), 
                                        self.getRotation(5), 
                                        offset)
                else: 
                    angle += self.getRotation(6)
                    if angle < 0 :
                            angle += 360
                    self.getActor().SetOrientation(self.getRotation(4), 
                                        self.getRotation(5), 
                                        angle)

            # self.actor.SetPosition(translate_x, translate_y, translate_z)
            self.getActorDict()["actor"] = self.getActor()
        
    # For Scaling
    def getScale(self, mode):
        if self.actor is not None:
            if (mode == 7):
                return self.getActor().GetScale()[0]
            elif (mode == 8):
                return self.getActor().GetScale()[1]
            elif (mode == 9):
                return self.getActor().GetScale()[2]
        else:
            return None
    
    def setScale(self, mode, offset, keyboard_bool):
        if self.actor is not None:
            if (mode == 7):
                if (keyboard_bool is True):
                        self.getActor().SetScale(offset, 
                                        self.getScale(8), 
                                        self.getScale(9))
                else:
                    self.getActor().SetScale(self.getScale(7) + offset, 
                                        self.getScale(8), 
                                        self.getScale(9))
            if (mode == 8):
                if (keyboard_bool is True):
                        self.getActor().SetScale(self.getScale(7), 
                                        offset, 
                                        self.getScale(9))
                else: 
                    self.getActor().SetScale(self.getScale(7), 
                                        self.getScale(8) + offset, 
                                        self.getScale(9))
            if (mode == 9):
                if (keyboard_bool is True):
                    self.getActor().SetScale(self.getScale(7), 
                                        self.getScale(8), 
                                        offset)
                else:
                    self.getActor().SetScale(self.getScale(7), 
                                        self.getScale(8), 
                                        self.getScale(9) + offset)
            self.getActorDict()["actor"] = self.getActor()
    
    # Colour
    def setColour(self, colour_input):
        if self.actor is not None:
            # if self.getSource() == "VTK_Import":

            # polydata = vtkPolyData()
            # polydata.DeepCopy(self.getActor().GetMapper().GetInput())

            # colors_data = vtkUnsignedCharArray()
            # colors_data.SetNumberOfComponents(3)
            # colors_data.SetName('Colors')

            # colour_input = tuple(int(value * 255) for value in colour_input)
            # for i in range(polydata.GetNumberOfPoints()):
            #     color_tuple = [*colour_input]
            #     colors_data.InsertNextTypedTuple(color_tuple)
            # polydata.GetPointData().SetScalars(colors_data)

            # mapper = vtkPolyDataMapper()
            # mapper.SetInputData(polydata)

            # self.getActor().SetMapper(mapper)
            # else:
            self.getActor().GetProperty().SetColor(*colour_input)
            self.getActorDict()["actor"] = self.getActor()

    def getColour(self):
        if self.actor is not None and self.getActor().GetClassName() != "vtkVolume":
            # if self.getSource() == "VTK_Import":
            # polydata = vtkPolyData()
            # polydata.DeepCopy(self.getActor().GetMapper().GetInput())
            # if polydata.GetPointData().GetScalars():
            #     scalar_array = polydata.GetPointData().GetScalars()
            #     colour = scalar_array.GetTuple3(0)
            #     colour = np.array(colour)
            # else:
            colour = self.getActor().GetProperty().GetColor()
            return tuple(int(value * 255) for value in colour)
        else:
            return (1,1,1)
    
    # Mapper
    def mapSourceToActor(self, source, actor):
        self.setSource(source)
        self.setActor(actor)
        self.getActor().GetProperty().SetColor(1.0, 1.0, 1.0)
        self.getColour()
        self.getActor().SetMapper(self.getMapper(source))
        return self.actor
    
    def getMapper(self, source = None):
        if (source is None):
            source = self.getSource()
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        mapper.Update()
        return mapper
    
    def setID(self, id):
        self.actor_id = id

    def getID(self):
        return self.actor_id

    def setActor(self, actor: vtkActor):
        self.actor = actor
        
    def getActor(self):
        return self.actor
    
    def setName(self, name: str):
        self.actor_name = name
        self.getActorDict()["name"] = self.getName()

    def getName(self):
        return self.actor_name
    
        # Source
    def setSource(self, source):
        self.source = source

    def getSource(self):
        return self.source
