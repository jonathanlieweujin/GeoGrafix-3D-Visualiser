from vtkmodules.all import*

class ActorsDictList():
    def createDictList(self, actor, source):
        self.current_generated_number = 0
        self.current_iteration = 0
        id = self.idGenerator()[1]
        self.scene_actor_list = [
            # {
            #     "id": self.idGenerator()[1],
            #     "actor": camera,
            #     "name": "Camera",
            #     "source": None,
            # },
            {
                "id": id,
                "actor": actor,
                "name": "actor_001",
                "source": source,
            }
        ]
        self.setGeneratedID(id)

    def getDictList(self):
        return self.scene_actor_list
    
    def updateDictList(self, target_id: str, dictionary: dict):
        for i, dictionary in enumerate(self.getDictList()):
            if self.getDictList()[i] == {}:
                pass
            elif dictionary["id"] == target_id:
                self.getDictList()[i] = dictionary

    def getActorProperties(self):
        actor_list = []
        for dictionary in self.getDictList():
            if not dictionary:  # Check if the dictionary is empty
                continue  # Skip empty dictionaries
            actor = dictionary.get("actor")  # Get the "name" value
            if actor:
                actor_list.append(actor)
        if actor_list == []:
            return ["Null"]
        else:
            return actor_list
        
    def getActorNames(self):
        name_list = []
        for dictionary in self.getDictList():
            if not dictionary:  # Check if the dictionary is empty
                continue  # Skip empty dictionaries
            name = dictionary.get("name")  # Get the "name" value
            if name:
                name_list.append(name)
        if name_list == []:
            return ["Null"]
        else:
            return name_list
        
    def getActorSources(self):
        name_list = []
        for dictionary in self.getDictList():
            if not dictionary:
                continue  # Check if the dictionary is empty
            name = dictionary.get("source")  # Get the "name" value
            if name:
                name_list.append(name)
            # else:
            #     name_list.append("Import_Actor")
        # print(name_list)
        if name_list == []:
            return ["Null"]
        else:
            return name_list
    
    def generateActorDict(self, actor, source, name = None):
        number, id, regen_bool = self.DictListChecker()
        if name is None:
            dictionary = {
                "id": id,
                "actor": actor,
                "name": f"actor_{number:03d}",
                "source": source,
            }
        else:
            dictionary = {
                "id": id,
                "actor": actor,
                "name": name,
                "source": source,
            }
        if regen_bool is True:
            self.getDictList()[number - 1] = dictionary
        else:
            self.getDictList().append(dictionary)
        # if number < self.getCurrentGenNum():
        #     self.getDictList()[number - 1] = dictionary
        # else:
        #     self.getDictList().append(dictionary)
        self.setGeneratedID(id)
        # print(self.getDictList())

    def getActorDict(self, target_id: str, bool = False): # have to return null if empty list
        if target_id == "-1": # After deleted, select last one in the list
            for i in range(len(self.getDictList()) - 1, -1, -1):
                if self.getDictList()[i]:
                    return self.getDictList()[i]
            return {}
            # if all_empty:
            #     return {}
            # else:
            #     return self.getDictList()[-1]
        if bool is False:
            for dictionary in self.getDictList():
                if not dictionary:
                    pass
                elif dictionary["id"] == target_id:
                    return dictionary
        elif bool is True:
            for dictionary in self.getDictList():
                if not dictionary:
                    pass
                elif dictionary["name"] == target_id:
                    return dictionary
    
    def deleteActorDict(self, target_id): # Delete and replace with empty dict
        
        for i, dictionary in enumerate(self.getDictList()):
            if not dictionary:
                pass
            elif dictionary["id"] == target_id:
                self.getDictList()[i] = {}
                return self.getActorDict("-1")
            
    def DictListChecker(self): # Check Empty Dictionary
        for i, d in enumerate(self.getDictList()):
            if not d:  # Check for empty dictionary
                return self.idGenerator(i+1)
        else:
            return self.idGenerator() # If no empty dictionary found, add a new one
        
    def idGenerator(self, iteration_num = None):
        if iteration_num is None:
            self.current_generated_number += 1
            return self.current_generated_number, f"{self.current_generated_number:06d}", False
        else:
            return iteration_num, f"{iteration_num:06d}", True
        
    def setGeneratedID(self, id):
        self.current_id = id

    def getCurrentGeneratedID(self):
        return self.current_id
    
    def getCurrentGenNum(self):
        return self.current_generated_number
    
    def actorTypeDict(self):
        actor_type_dict = {
            "vtkCubeSource": "VTK_Cube",
            "vtkCylinderSource": "VTK_Cylinder",
            "vtkConeSource": "VTK_Cone",
            "vtkSphereSource": "VTK_Sphere",
            "vtkDiskSource": "VTK_Disk",
            "vtkTessellatedBoxSource": "VTK_Tess_Box",
            "vtkParametricFunctionSource": "VTK_Para_Func"
        }

        return actor_type_dict
    
    def getActorType(self, source = None):
        dict = self.actorTypeDict()
        if source is not None:
            if isinstance(source, str):
                actor_type = source
            else:
                current_source_class = source.GetClassName()
                actor_type = dict.get(current_source_class, "None")
            return actor_type
        
    def getVertices(self, polydata: vtkPolyData):
        num_points = polydata.GetNumberOfPoints()
        return num_points
    
    def getEdges(self, polydata: vtkPolyData):
        edges = vtkCellArray()
        edge_extractor = vtkExtractEdges()
        edge_extractor.SetInputData(polydata)
        edge_extractor.Update()
        edges.ShallowCopy(edge_extractor.GetOutput().GetLines())
        num_edges = edges.GetNumberOfCells()
        return num_edges

    def getFaces(self, polydata: vtkPolyData):
        num_faces = polydata.GetNumberOfCells()
        return num_faces
    
