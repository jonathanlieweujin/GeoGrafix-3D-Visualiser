import math
import pyautogui, ctypes, sys
from PyQt5 import QtCore, QtGui, QtWidgets

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vtkmodules.all import *
import actor
import vtk_reader
import vtk_writer
import actors_dict_list as actorsdictlist

class GuiWindow(object):
        """
        Creates GUI Interface.
        """

        def __init__(self, m_window: QtWidgets.QMainWindow):
                super().__init__()
                self.m_window = m_window
                self.update()

        def update(self):

                vtk_label_dir = "./images/vtk_rect.png"
                outl_label_dir = "./images/outliner_rect.png"
                properties_rect_dir = "./images/properties_rect.png"
                stat_label_dir = "./images/details_rect.png"
                properties_label_dir ="./images/details_rect.png"
                self.value_label_dir = "./images/value_labels.png"
                self.value_label_sel_dir = "./images/value_labels_selected.png"
                self.value_label_hov_dir = "./images/value_labels_hovered.png"
                icon = QtGui.QIcon("./images/icon.ico")

                # Init stylesheet
                transparent_bg_col = "background-color: rgba(255, 255, 255, 0);"
                transparent_col = "color: rgba(255, 255, 255, 0);"

                stylesheet_version_text = "background-color: rgb(48, 48, 48);\ncolor: rgb(217, 217, 217);"
                style_3d3d3d = "background-color: rgb(61, 61, 61);\ncolor: rgb(217, 217, 217);"
                
                # Initialise UI font
                self.font = QtGui.QFont()
                self.font.setFamily("MS Shell Dlg 2")
                self.font.setPointSize(9)

                details_tab_font = QtGui.QFont()
                details_tab_font.setPointSize(8)

                self.m_window.setObjectName("MainWindow")
                self.m_window.setGeometry(0, 0, 1920, 1080)
                self.m_window.showMaximized()  
                self.m_window.setAutoFillBackground(True)
                self.m_window.setStyleSheet("background-color: rgb(22, 22, 22);")
                self.m_window.setWindowIcon(icon)
                
                # Create a layout for the central widget
                self.centralwidget = QtWidgets.QWidget(self.m_window)
                self.centralwidget.setObjectName("centralwidget")
                
                # Horizontal Frame
                self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
                self.horizontalLayoutWidget.setGeometry(QtCore.QRect(19, 10, 1891, 941))
                self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

                self.window_HL1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
                self.window_HL1.setContentsMargins(0, 0, 0, 0)
                self.window_HL1.setObjectName("window_HL1")

                # VTK Frame
                self.vtk_frame = QtWidgets.QFrame(self.horizontalLayoutWidget)
                self.vtk_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.vtk_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.vtk_frame.setAutoFillBackground(True)
                self.vtk_frame.setStyleSheet(transparent_bg_col)
                self.vtk_frame.setObjectName("vtk_frame")

                self.vtk_image_label = QtWidgets.QLabel(self.vtk_frame)
                self.vtk_image_label.setGeometry(QtCore.QRect(0, 0, 1506, 935))
                self.vtk_image_label.setAutoFillBackground(True)
                self.vtk_image_label.setStyleSheet(transparent_col)
                self.vtk_image_label.setText("")
                self.vtk_image_label.setPixmap(QtGui.QPixmap(vtk_label_dir))
                self.vtk_image_label.setScaledContents(True)
                self.vtk_image_label.setObjectName("vtk_image_label")
                self.window_HL1.addWidget(self.vtk_frame)

                self.vtk_viewport = QtVtkFrame()
                self.vtk_widget = CustomQVTKRenderWindowInteractor(main_window = self, parent = self.vtk_frame, 
                                                        rw = self.vtk_viewport.getRenderWindow())
                self.vtk_widget.setGeometry(QtCore.QRect(5, 5, 1496, 925))
                self.axes_actor = vtkAxesActor()
                self.vtk_viewport.loadAxis(self.axes_actor)

                # style = myInteractorStyle()
                # self.vtk_widget.SetInteractorStyle(style)

                self.vtk_widget.Initialize()
                self.vtk_widget.Start()

                # Initialise Camera
                self.camera = Camera()
                self.camera.setCamera(self.vtk_viewport.getRenderer().GetActiveCamera())
                self.camera.setClipping(0.01, 1000)
                self.camera.setFOV(20)
                self.vtk_camera = self.camera.getCamera()
                self.ori_cam_settings = self.camera.get_orientation(self.vtk_viewport)
                # self.vtk_render_environment.activateCamera(self.vtk_camera)
                self.vtk_viewport.updateRenderer()

                self.vtk_widget.initViewportCam(self.camera, self.ori_cam_settings)
                # print(self.vtk_render_environment.getRenderer().GetActiveCamera())

                # Initialise current actor
                self.actor = actor.Actor()
                current_actor = self.actor.mapSourceToActor(vtkConeSource(), vtkActor())
                current_actor_source = vtkConeSource()
                self.vtk_viewport.addActor(current_actor)

                self.has_actors = True

                # self.actor.setActorGuide(vtkCubeSource())
                # self.actor_guide = self.actor.getActorGuide()
                # self.vtk_viewport.addActor(self.actor_guide)

                # Actors in VTK scene
                self.scene_actors = actorsdictlist.ActorsDictList()
                self.scene_actors.createDictList(current_actor, 
                                                   current_actor_source) 
                self.actor.setActorDict(dictionary_list = self.scene_actors)

                self.light_source = vtkLight()
                self.light_source.SetPosition(3, 3, -3)
                self.light_source.SetLightTypeToSceneLight()
                self.light_source.SetPositional(True)
                self.light_source.SetConeAngle(60)

                self.light_actor = vtkLightActor()
                self.light_actor.SetLight (self.light_source)
                self.vtk_viewport.getRenderer().AddViewProp(self.light_actor)
                self.vtk_viewport.getRenderer().AddLight(self.light_source)

                # Vertical Frame
                self.window_VL1 = QtWidgets.QVBoxLayout()
                self.window_VL1.setSpacing(10)
                self.window_VL1.setObjectName("window_VL1")

                # Outline Frame
                self.outliner_frame = QtWidgets.QFrame(self.horizontalLayoutWidget)
                self.outliner_frame.setAutoFillBackground(True)
                self.outliner_frame.setStyleSheet(transparent_bg_col) 

                self.outliner_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.outliner_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.outliner_frame.setObjectName("outliner_frame")
                self.outliner_image_label = QtWidgets.QLabel(self.outliner_frame)
                self.outliner_image_label.setGeometry(QtCore.QRect(0, 0, 374, 309))
                self.outliner_image_label.setAutoFillBackground(True)
                self.outliner_image_label.setStyleSheet(transparent_col)
                self.outliner_image_label.setText("")
                self.outliner_image_label.setPixmap(QtGui.QPixmap(outl_label_dir))
                self.outliner_image_label.setScaledContents(True)
                self.outliner_image_label.setObjectName("outliner_image_label")

                self.outliner_text_label = QtWidgets.QLabel(self.outliner_frame)
                self.outliner_text_label.setGeometry(QtCore.QRect(25, 30, 311, 251))
                self.outliner_text_label.setFont(self.font)
                self.outliner_text_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.outliner_text_label.setAutoFillBackground(True)
                self.outliner_text_label.setStyleSheet("background-color: rgb(40, 40, 40);\n"
                                                "color: rgb(217, 217, 217);")
                self.outliner_text_label.setTextFormat(QtCore.Qt.AutoText)
                self.outliner_text_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
                self.outliner_text_label.setObjectName("outliner_text_label")
                self.updateOutliner()
                self.window_VL1.addWidget(self.outliner_frame)

                # Tab Widget
                self.tab_widget = QtWidgets.QTabWidget(self.horizontalLayoutWidget)    
                self.tab_widget.setFont(details_tab_font)
                self.tab_widget.setAutoFillBackground(True)
                self.tab_widget.setStyleSheet("QTabWidget::pane { border: 0; }"
                                        "QTabBar::tab:selected {background: rgb(48, 48, 48);color: rgb(217, 217, 217);border :1px solid ; border-top-color : rgb(217, 217, 217); border-left-color :rgb(217, 217, 217);border-right-color :rgb(217, 217, 217); min-width: 100px;}"
                                        "QTabBar::tab {background: rgb(61, 61, 61);color: rgb(217, 217, 217); min-width: 100px;}")
                self.tab_widget.setObjectName("tab_widget")

                # Property Tab
                self.properties_tab = QtWidgets.QWidget()
                self.properties_tab.setObjectName("properties_tab")
                self.properties_frame = QtWidgets.QFrame(self.properties_tab)
                self.properties_frame.setGeometry(QtCore.QRect(0, 0, 381, 591))
                self.properties_frame.setAutoFillBackground(True)
                self.properties_frame.setStyleSheet(transparent_bg_col)
                self.properties_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.properties_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.properties_frame.setObjectName("properties_frame")
                self.properties_label_image = QtWidgets.QLabel(self.properties_frame)
                self.properties_label_image.setGeometry(QtCore.QRect(0, 0, 371, 591))
                self.properties_label_image.setAutoFillBackground(True)
                self.properties_label_image.setStyleSheet(transparent_col)
                self.properties_label_image.setText("")
                self.properties_label_image.setPixmap(QtGui.QPixmap(properties_label_dir))
                self.properties_label_image.setScaledContents(True)
                self.properties_label_image.setObjectName("properties_label_image")

                self.version_stat_label_2 = QtWidgets.QLabel(self.properties_frame)
                self.version_stat_label_2.setGeometry(QtCore.QRect(300, 560, 55, 16))
                self.version_stat_label_2.setFont(self.font)
                self.version_stat_label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.version_stat_label_2.setAutoFillBackground(True)

                self.version_stat_label_2.setStyleSheet(stylesheet_version_text)
                self.version_stat_label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.version_stat_label_2.setObjectName("version_stat_label_2")

                # Actor Selector Dropdown
                self.actor_dropdown_selector = ActorDropdownSelector(self.properties_frame, self)
                self.actor_dropdown_selector.setGeometry(QtCore.QRect(15, 10, 150, 30))
                self.actor_dropdown_selector.setFont(self.font)
                self.actor_dropdown_selector.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.actor_dropdown_selector.setAutoFillBackground(True)
                self.actor_dropdown_selector.setStyleSheet(
                       "QComboBox {background-color: rgb(40, 40, 40);\ncolor: rgb(217, 217, 217);"
                       "padding: 5px 10px; selection-background-color: rgb(40, 40, 40);}"
                       "QComboBox QAbstractItemView {background-color: rgb(20, 20, 20);\ncolor: rgb(217, 217, 217);"
                       "padding: 5px 10px; selection-background-color: rgb(71, 114, 179);}"
                #        "QComboBox::drop-down {  border: 0px;  }"
                #        "QComboBox::down-arrow { background-color: rgb(20, 20, 20); \ncolor: rgb(217, 217, 217);}"
                       
                )
                # self.actor_dropdown_selector.setTextFormat(QtCore.Qt.AutoText)
                # self.actor_dropdown_selector.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.actor_dropdown_selector.setObjectName("actor_dropdown_selector")

                self.actor_dropdown_selector.addItems(self.scene_actors.getActorNames())
                self.actor_dropdown_selector.activated.connect(lambda: self.changeActor(self.actor_dropdown_selector.currentText()))

                self.frame_2 = QtWidgets.QFrame(self.properties_frame)
                self.frame_2.setGeometry(QtCore.QRect(15, 52, 341, 491))
                self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
                self.frame_2.setObjectName("frame_2")

                # Resolution
                self.resolution_label = QtWidgets.QLabel(self.frame_2)
                self.resolution_label.setGeometry(QtCore.QRect(10, 3, 281, 20))
                self.resolution_label.setFont(self.font)
                self.resolution_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.resolution_label.setAutoFillBackground(True)
                self.resolution_label.setStyleSheet(stylesheet_version_text)
                self.resolution_label.setTextFormat(QtCore.Qt.AutoText)
                self.resolution_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.resolution_label.setObjectName("resolution_label")

                self.resolution_slider = QtWidgets.QLabel(self.frame_2)
                self.resolution_slider.setGeometry(QtCore.QRect(114, 0, 207, 25))
                self.resolution_slider.setAutoFillBackground(True)
                self.resolution_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.resolution_slider.setText("")
                self.resolution_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.resolution_slider.setScaledContents(True)
                self.resolution_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.resolution_slider.setObjectName("resolution_value")

                self.resolution_dispvalue = SliderDisVal(self.frame_2, self.resolution_slider, 10, 0, self)
                self.resolution_dispvalue.setGeometry(QtCore.QRect(114, 0, 207, 25))
                self.resolution_dispvalue.setFont(self.font)
                self.resolution_dispvalue.setAutoFillBackground(True)
                self.resolution_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.resolution_dispvalue.setText(f"{self.actor.getResolution()}")
                self.resolution_dispvalue.setScaledContents(True)
                self.resolution_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.resolution_dispvalue.setObjectName("resolution_dispvalue")
                self.resolution_dispvalue.clicked.connect(lambda: self.updateActorDetails(0, 
                                                                                          self.resolution_dispvalue,
                                                                                          self.resolution_dispvalue.prev_offset,
                                                                                          False))

                self.label = QtWidgets.QLabel(self.frame_2)
                self.label.setGeometry(QtCore.QRect(0, 38, 341, 441))
                self.label.setAutoFillBackground(True)
                self.label.setStyleSheet(transparent_bg_col)
                self.label.setText("")
                self.label.setPixmap(QtGui.QPixmap(properties_rect_dir))
                self.label.setScaledContents(True)
                self.label.setObjectName("label")

                # Transform Heading
                self.transform_label = QtWidgets.QLabel(self.frame_2)
                self.transform_label.setGeometry(QtCore.QRect(20, 48, 81, 31))
                self.transform_label.setFont(self.font)
                self.transform_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.transform_label.setAutoFillBackground(True)
                self.transform_label.setStyleSheet(style_3d3d3d)
                self.transform_label.setTextFormat(QtCore.Qt.AutoText)
                self.transform_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.transform_label.setObjectName("transform_label")

                # Transparent
                self.wireframe_checkbox = WireframeCheckBox(self.frame_2, self.actor, self.vtk_viewport, self)
                self.wireframe_checkbox.setGeometry(QtCore.QRect(220, 55, 110, 20))
                self.wireframe_checkbox.setFont(self.font)
                self.wireframe_checkbox.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.wireframe_checkbox.setAutoFillBackground(True)
                self.wireframe_checkbox.setStyleSheet( "QCheckBox { spacing : 12px; \n"
                                                      "background-color: rgb(61, 61, 61);"
                                                        "color: rgb(217, 217, 217); }")
                self.wireframe_checkbox.setObjectName("wireframe_checkbox")
                self.vtk_widget.setWireframeCheckbox(self.wireframe_checkbox)

                # Location X
                self.location_x_label = QtWidgets.QLabel(self.frame_2)
                self.location_x_label.setGeometry(QtCore.QRect(10, 101, 79, 18))
                self.location_x_label.setFont(self.font)
                self.location_x_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.location_x_label.setAutoFillBackground(True)
                self.location_x_label.setStyleSheet(style_3d3d3d)
                self.location_x_label.setTextFormat(QtCore.Qt.AutoText)
                self.location_x_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.location_x_label.setObjectName("location_x_label")

                self.location_x_slider = QtWidgets.QLabel(self.frame_2)
                self.location_x_slider.setGeometry(QtCore.QRect(114, 98, 207, 25))
                self.location_x_slider.setAutoFillBackground(True)
                self.location_x_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.location_x_slider.setText("")
                self.location_x_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.location_x_slider.setScaledContents(True)
                self.location_x_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.location_x_slider.setObjectName("location_x_slider")

                # 0 = res 1, 2, 3 = loc 4, 5, 6 = rot, 7, 8 ,9 = scale
                self.location_x_dispvalue = SliderDisVal(self.frame_2, self.location_x_slider, 20, 1, self)
                self.location_x_dispvalue.setGeometry(QtCore.QRect(114, 98, 207, 25))
                self.location_x_dispvalue.setFont(self.font)
                self.location_x_dispvalue.setAutoFillBackground(True)
                self.location_x_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.location_x_dispvalue.setText(f"{self.actor.getLocation(1)}")
                self.location_x_dispvalue.setScaledContents(True)
                self.location_x_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.location_x_dispvalue.setObjectName("location_x_dispvalue")
                self.location_x_dispvalue.clicked.connect(lambda: self.updateActorDetails(1, 
                                                                                          self.location_x_dispvalue,
                                                                                          self.location_x_dispvalue.prev_offset,
                                                                                          False))

                # Location Y
                self.location_y_label = QtWidgets.QLabel(self.frame_2)
                self.location_y_label.setGeometry(QtCore.QRect(10, 133, 79, 18))
                self.location_y_label.setFont(self.font)
                self.location_y_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.location_y_label.setAutoFillBackground(True)
                self.location_y_label.setStyleSheet(style_3d3d3d)
                self.location_y_label.setTextFormat(QtCore.Qt.AutoText)
                self.location_y_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.location_y_label.setObjectName("location_y_label")

                self.location_y_slider = QtWidgets.QLabel(self.frame_2)
                self.location_y_slider.setGeometry(QtCore.QRect(114, 130, 207, 25))
                self.location_y_slider.setAutoFillBackground(True)
                self.location_y_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.location_y_slider.setText("")
                self.location_y_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.location_y_slider.setScaledContents(True)
                self.location_y_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.location_y_slider.setObjectName("location_y_slider")

                self.location_y_dispvalue = SliderDisVal(self.frame_2, self.location_y_slider, 20, 2, self)
                self.location_y_dispvalue.setGeometry(QtCore.QRect(114, 130, 207, 25))
                self.location_y_dispvalue.setFont(self.font)
                self.location_y_dispvalue.setAutoFillBackground(True)
                self.location_y_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.location_y_dispvalue.setText(f"{self.actor.getLocation(2)}")
                self.location_y_dispvalue.setScaledContents(True)
                self.location_y_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.location_y_dispvalue.setObjectName("location_y_dispvalue")
                self.location_y_dispvalue.clicked.connect(lambda: self.updateActorDetails(2, 
                                                                                          self.location_y_dispvalue,
                                                                                          self.location_y_dispvalue.prev_offset,
                                                                                          False))

                # Location Z
                self.location_z_label = QtWidgets.QLabel(self.frame_2)
                self.location_z_label.setGeometry(QtCore.QRect(10, 165, 79, 18))
                self.location_z_label.setFont(self.font)
                self.location_z_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.location_z_label.setAutoFillBackground(True)
                self.location_z_label.setStyleSheet(style_3d3d3d)
                self.location_z_label.setTextFormat(QtCore.Qt.AutoText)
                self.location_z_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.location_z_label.setObjectName("location_z_label")

                self.location_z_slider = QtWidgets.QLabel(self.frame_2)
                self.location_z_slider.setGeometry(QtCore.QRect(114, 162, 207, 25))
                self.location_z_slider.setAutoFillBackground(True)
                self.location_z_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.location_z_slider.setText("")
                self.location_z_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.location_z_slider.setScaledContents(True)
                self.location_z_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.location_z_slider.setObjectName("location_z_slider")

                self.location_z_dispvalue = SliderDisVal(self.frame_2, self.location_z_slider, 20, 3, self)
                self.location_z_dispvalue.setGeometry(QtCore.QRect(114, 162, 207, 25))
                self.location_z_dispvalue.setFont(self.font)
                self.location_z_dispvalue.setAutoFillBackground(True)
                self.location_z_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.location_z_dispvalue.setText(f"{self.actor.getLocation(3)}")
                self.location_z_dispvalue.setScaledContents(True)
                self.location_z_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.location_z_dispvalue.setObjectName("location_z_dispvalue")
                self.location_z_dispvalue.clicked.connect(lambda: self.updateActorDetails(3, 
                                                                                          self.location_z_dispvalue,
                                                                                          self.location_z_dispvalue.prev_offset,
                                                                                          False))
                # Rotation 
                self.rotation_x_label = QtWidgets.QLabel(self.frame_2)
                self.rotation_x_label.setGeometry(QtCore.QRect(10, 203, 79, 18))
                self.rotation_x_label.setFont(self.font)
                self.rotation_x_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.rotation_x_label.setAutoFillBackground(True)
                self.rotation_x_label.setStyleSheet(style_3d3d3d)
                self.rotation_x_label.setTextFormat(QtCore.Qt.AutoText)
                self.rotation_x_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.rotation_x_label.setObjectName("rotation_x_label")
                
                self.rotation_x_slider = QtWidgets.QLabel(self.frame_2)
                self.rotation_x_slider.setGeometry(QtCore.QRect(114, 199, 207, 25))
                self.rotation_x_slider.setAutoFillBackground(True)
                self.rotation_x_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.rotation_x_slider.setText("")
                self.rotation_x_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.rotation_x_slider.setScaledContents(True)
                self.rotation_x_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.rotation_x_slider.setObjectName("rotation_x_slider")

                self.rotation_x_dispvalue = SliderDisVal(self.frame_2, self.rotation_x_slider, 5, 4, self)
                self.rotation_x_dispvalue.setGeometry(QtCore.QRect(114, 199, 207, 25))
                self.rotation_x_dispvalue.setFont(self.font)
                self.rotation_x_dispvalue.setAutoFillBackground(True)
                self.rotation_x_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.rotation_x_dispvalue.setText(f"{self.actor.getRotation(4)}")
                self.rotation_x_dispvalue.setScaledContents(True)
                self.rotation_x_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.rotation_x_dispvalue.setObjectName("rotation_x_dispvalue")
                self.rotation_x_dispvalue.clicked.connect(lambda: self.updateActorDetails(4, 
                                                                                          self.rotation_x_dispvalue,
                                                                                          self.rotation_x_dispvalue.prev_offset,
                                                                                          False))

                # Rotation Y
                self.rotation_y_label = QtWidgets.QLabel(self.frame_2)
                self.rotation_y_label.setGeometry(QtCore.QRect(10, 235, 79, 18))
                self.rotation_y_label.setFont(self.font)
                self.rotation_y_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.rotation_y_label.setAutoFillBackground(True)
                self.rotation_y_label.setStyleSheet(style_3d3d3d)
                self.rotation_y_label.setTextFormat(QtCore.Qt.AutoText)
                self.rotation_y_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.rotation_y_label.setObjectName("rotation_y_label")
                
                self.rotation_y_slider = QtWidgets.QLabel(self.frame_2)
                self.rotation_y_slider.setGeometry(QtCore.QRect(114, 231, 207, 25))
                self.rotation_y_slider.setAutoFillBackground(True)
                self.rotation_y_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.rotation_y_slider.setText("")
                self.rotation_y_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.rotation_y_slider.setScaledContents(True)
                self.rotation_y_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.rotation_y_slider.setObjectName("rotation_y_value")

                self.rotation_y_dispvalue = SliderDisVal(self.frame_2, self.rotation_y_slider, 5, 5, self)
                self.rotation_y_dispvalue.setGeometry(QtCore.QRect(114, 231, 207, 25))
                self.rotation_y_dispvalue.setFont(self.font)
                self.rotation_y_dispvalue.setAutoFillBackground(True)
                self.rotation_y_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.rotation_y_dispvalue.setText(f"{self.actor.getRotation(5)}")
                self.rotation_y_dispvalue.setScaledContents(True)
                self.rotation_y_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.rotation_y_dispvalue.setObjectName("rotation_y_dispvalue")
                self.rotation_y_dispvalue.clicked.connect(lambda: self.updateActorDetails(5, 
                                                                                          self.rotation_y_dispvalue,
                                                                                          self.rotation_y_dispvalue.prev_offset,
                                                                                          False))

                # Rotation Z
                self.rotation_z_label = QtWidgets.QLabel(self.frame_2)
                self.rotation_z_label.setGeometry(QtCore.QRect(10, 267, 79, 18))
                self.rotation_z_label.setFont(self.font)
                self.rotation_z_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.rotation_z_label.setAutoFillBackground(True)
                self.rotation_z_label.setStyleSheet(style_3d3d3d)
                self.rotation_z_label.setTextFormat(QtCore.Qt.AutoText)
                self.rotation_z_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.rotation_z_label.setObjectName("rotation_z_label")
                
                self.rotation_z_slider = QtWidgets.QLabel(self.frame_2)
                self.rotation_z_slider.setGeometry(QtCore.QRect(114, 263, 207, 25))
                self.rotation_z_slider.setAutoFillBackground(True)
                self.rotation_z_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.rotation_z_slider.setText("")
                self.rotation_z_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.rotation_z_slider.setScaledContents(True)
                self.rotation_z_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.rotation_z_slider.setObjectName("rotation_z_value")

                self.rotation_z_dispvalue = SliderDisVal(self.frame_2, self.rotation_z_slider, 5, 6, self)
                self.rotation_z_dispvalue.setGeometry(QtCore.QRect(114, 263, 207, 25))
                self.rotation_z_dispvalue.setFont(self.font)
                self.rotation_z_dispvalue.setAutoFillBackground(True)
                self.rotation_z_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.rotation_z_dispvalue.setText(f"{self.actor.getRotation(6)}")
                self.rotation_z_dispvalue.setScaledContents(True)
                self.rotation_z_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.rotation_z_dispvalue.setObjectName("rotation_z_dispvalue")
                self.rotation_z_dispvalue.clicked.connect(lambda: self.updateActorDetails(6, 
                                                                                          self.rotation_z_dispvalue,
                                                                                          self.rotation_z_dispvalue.prev_offset,
                                                                                          False))

                # Scale X
                self.scale_x_label = QtWidgets.QLabel(self.frame_2)
                self.scale_x_label.setGeometry(QtCore.QRect(10, 304, 79, 18))
                self.scale_x_label.setFont(self.font)
                self.scale_x_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.scale_x_label.setAutoFillBackground(True)
                self.scale_x_label.setStyleSheet(style_3d3d3d)
                self.scale_x_label.setTextFormat(QtCore.Qt.AutoText)
                self.scale_x_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.scale_x_label.setObjectName("scale_x_label")
                
                self.scale_x_slider = QtWidgets.QLabel(self.frame_2)
                self.scale_x_slider.setGeometry(QtCore.QRect(114, 300, 207, 25))
                self.scale_x_slider.setAutoFillBackground(True)
                self.scale_x_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.scale_x_slider.setText("")
                self.scale_x_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.scale_x_slider.setScaledContents(True)
                self.scale_x_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.scale_x_slider.setObjectName("scale_x_slider")

                self.scale_x_dispvalue = SliderDisVal(self.frame_2, self.scale_x_slider, 20, 7, self)
                self.scale_x_dispvalue.setGeometry(QtCore.QRect(114, 300, 207, 25))
                self.scale_x_dispvalue.setFont(self.font)
                self.scale_x_dispvalue.setAutoFillBackground(True)
                self.scale_x_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.scale_x_dispvalue.setText(f"{self.actor.getScale(7)}")
                self.scale_x_dispvalue.setScaledContents(True)
                self.scale_x_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.scale_x_dispvalue.setObjectName("scale_x_dispvalue")
                self.scale_x_dispvalue.clicked.connect(lambda: self.updateActorDetails(7, 
                                                                                          self.scale_x_dispvalue,
                                                                                          self.scale_x_dispvalue.prev_offset,
                                                                                          False))

                # Scale Y
                self.scale_y_label = QtWidgets.QLabel(self.frame_2)
                self.scale_y_label.setGeometry(QtCore.QRect(10, 336, 79, 18))
                self.scale_y_label.setFont(self.font)
                self.scale_y_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.scale_y_label.setAutoFillBackground(True)
                self.scale_y_label.setStyleSheet(style_3d3d3d)
                self.scale_y_label.setTextFormat(QtCore.Qt.AutoText)
                self.scale_y_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.scale_y_label.setObjectName("scale_y_label")

                self.scale_y_slider = QtWidgets.QLabel(self.frame_2)
                self.scale_y_slider.setEnabled(True)
                self.scale_y_slider.setGeometry(QtCore.QRect(114, 332, 207, 25))
                self.scale_y_slider.setAutoFillBackground(True)
                self.scale_y_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.scale_y_slider.setText("")
                self.scale_y_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.scale_y_slider.setScaledContents(True)
                self.scale_y_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.scale_y_slider.setObjectName("scale_y_slider")

                self.scale_y_dispvalue = SliderDisVal(self.frame_2, self.scale_y_slider, 20, 8, self)
                self.scale_y_dispvalue.setGeometry(QtCore.QRect(114, 332, 207, 25))
                self.scale_y_dispvalue.setFont(self.font)
                self.scale_y_dispvalue.setAutoFillBackground(True)
                self.scale_y_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.scale_y_dispvalue.setText(f"{self.actor.getScale(8)}")
                self.scale_y_dispvalue.setScaledContents(True)
                self.scale_y_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.scale_y_dispvalue.setObjectName("scale_y_dispvalue")
                self.scale_y_dispvalue.clicked.connect(lambda: self.updateActorDetails(8, 
                                                                                          self.scale_y_dispvalue,
                                                                                          self.scale_y_dispvalue.prev_offset,
                                                                                          False))

                # Scale Z
                self.scale_z_label = QtWidgets.QLabel(self.frame_2)
                self.scale_z_label.setGeometry(QtCore.QRect(10, 368, 79, 18))
                self.scale_z_label.setFont(self.font)
                self.scale_z_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.scale_z_label.setAutoFillBackground(True)
                self.scale_z_label.setStyleSheet(style_3d3d3d)
                self.scale_z_label.setTextFormat(QtCore.Qt.AutoText)
                self.scale_z_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.scale_z_label.setObjectName("scale_z_label")

                self.scale_z_slider = QtWidgets.QLabel(self.frame_2)
                self.scale_z_slider.setGeometry(QtCore.QRect(114, 364, 207, 25))
                self.scale_z_slider.setAutoFillBackground(True)
                self.scale_z_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.scale_z_slider.setText("")
                self.scale_z_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.scale_z_slider.setScaledContents(True)
                self.scale_z_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.scale_z_slider.setObjectName("scale_z_slider")

                self.scale_z_dispvalue = SliderDisVal(self.frame_2, self.scale_z_slider, 20, 9, self)
                self.scale_z_dispvalue.setGeometry(QtCore.QRect(114, 364, 207, 25))
                self.scale_z_dispvalue.setFont(self.font)
                self.scale_z_dispvalue.setAutoFillBackground(True)
                self.scale_z_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.scale_z_dispvalue.setText(f"{self.actor.getScale(9)}")
                self.scale_z_dispvalue.setScaledContents(True)
                self.scale_z_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.scale_z_dispvalue.setObjectName("scale_z_dispvalue")
                self.scale_z_dispvalue.clicked.connect(lambda: self.updateActorDetails(9, 
                                                                                          self.scale_z_dispvalue,
                                                                                          self.scale_z_dispvalue.prev_offset,
                                                                                          False))

                # Colour 
                self.colour_label = QtWidgets.QLabel(self.frame_2)
                self.colour_label.setGeometry(QtCore.QRect(10, 426, 79, 18))
                self.colour_label.setFont(self.font)
                self.colour_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.colour_label.setAutoFillBackground(True)
                
                self.colour_label.setStyleSheet(style_3d3d3d)
                self.colour_label.setTextFormat(QtCore.Qt.AutoText)
                self.colour_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.colour_label.setObjectName("colour_label")
                
                self.colour_value_label = ColourButton(parent = self.frame_2, text = "",
                                                       actor = self.actor)
                self.colour_value_label.setGeometry(QtCore.QRect(114, 423, 207, 25))
                self.colour_value_label.setText("")
                # self.colour_value_label.setPixmap(QtGui.QPixmap(colour_label_dir))
                self.colour_value_label.setScaledContents(True)
                self.colour_value_label.setAlignment(QtCore.Qt.AlignCenter)
                self.colour_value_label.setObjectName("colour_value_label")

                self.properties_label_image.raise_()
                self.actor_dropdown_selector.raise_()
                self.version_stat_label_2.raise_()
                self.frame_2.raise_()
                
                # Stat Tab
                self.statistics_tab = QtWidgets.QWidget()
                self.statistics_tab.setObjectName("statistics_tab")

                self.stats_frame = QtWidgets.QFrame(self.statistics_tab)
                self.stats_frame.setGeometry(QtCore.QRect(0, 0, 371, 591))
                self.stats_frame.setAutoFillBackground(True)
                self.stats_frame.setStyleSheet(transparent_bg_col)
                self.stats_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.stats_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.stats_frame.setObjectName("stats_frame")
                self.stats_label_image_2 = QtWidgets.QLabel(self.stats_frame)
                self.stats_label_image_2.setGeometry(QtCore.QRect(0, 0, 371, 591))
                self.stats_label_image_2.setAutoFillBackground(True)
                self.stats_label_image_2.setStyleSheet(transparent_col)
                self.stats_label_image_2.setText("")
                self.stats_label_image_2.setPixmap(QtGui.QPixmap(stat_label_dir))
                self.stats_label_image_2.setScaledContents(True)
                self.stats_label_image_2.setObjectName("stats_label_image_2")

                self.version_stat_label = QtWidgets.QLabel(self.stats_frame)
                self.version_stat_label.setGeometry(QtCore.QRect(300, 560, 55, 16))
                self.version_stat_label.setFont(self.font)
                self.version_stat_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.version_stat_label.setAutoFillBackground(True)
                self.version_stat_label.setStyleSheet(stylesheet_version_text)
                self.version_stat_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.version_stat_label.setObjectName("version_stat_label")

                self.stats_heading = QtWidgets.QLabel(self.stats_frame)
                self.stats_heading.setGeometry(QtCore.QRect(25, 30, 311, 51))
                self.stats_heading.setFont(self.font)
                self.stats_heading.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.stats_heading.setAutoFillBackground(True)
                self.stats_heading.setStyleSheet("background-color: rgb(48, 48, 48);\n"
        "color: rgb(217, 217, 217);")
                self.stats_heading.setTextFormat(QtCore.Qt.AutoText)
                self.stats_heading.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
                self.stats_heading.setObjectName("stats_heading")
                
                self.stats_category_label = QtWidgets.QLabel(self.stats_frame)
                self.stats_category_label.setGeometry(QtCore.QRect(25, 100, 91, 441))
                self.stats_category_label.setFont(self.font)
                self.stats_category_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.stats_category_label.setAutoFillBackground(True)
                self.stats_category_label.setStyleSheet("background-color: rgb(48, 48, 48);\n"
        "color: rgb(217, 217, 217);")
                self.stats_category_label.setTextFormat(QtCore.Qt.AutoText)
                self.stats_category_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
                self.stats_category_label.setObjectName("stats_category_label")

                self.stats_category_value = QtWidgets.QLabel(self.stats_frame)
                self.stats_category_value.setGeometry(QtCore.QRect(125, 100, 221, 441))
                self.stats_category_value.setFont(self.font)
                self.stats_category_value.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.stats_category_value.setAutoFillBackground(True)
                self.stats_category_value.setStyleSheet("background-color: rgb(48, 48, 48);\n"
        "color: rgb(217, 217, 217);")
                self.stats_category_value.setTextFormat(QtCore.Qt.AutoText)
                self.stats_category_value.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
                self.stats_category_value.setObjectName("stats_category_value")
                
                self.window_VL1.addWidget(self.tab_widget)
                self.window_VL1.setStretch(0, 1)
                self.window_VL1.setStretch(1, 2)
                self.window_HL1.addLayout(self.window_VL1)
                self.window_HL1.setStretch(0, 4)
                self.window_HL1.setStretch(1, 1)
                self.m_window.setCentralWidget(self.centralwidget)

                # Menu Bar
                self.menu_bar = QtWidgets.QMenuBar(self.m_window)
                self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
                self.menu_bar.setAutoFillBackground(True)
                self.menu_bar.setStyleSheet("QMenuBar {background-color: rgb(29, 29, 29);\ncolor: rgb(169, 169, 169);}"
                                        "QMenuBar::item { background-color: transparent; }"
                                        "QMenuBar::item:selected { background-color: #4772b3;"
                                                "color: rgb(200, 200, 200);}"
                                        "QMenu {background-color: rgb(29, 29, 29); color: white;"
                                                        "padding: 5px 10px}"
                                        "QMenu::item { background-color: transparent; }"
                                        "QMenu::item:selected { background-color: #4772b3;"
                                                                "color: rgb(200, 200, 200);}"
                )
                self.menu_bar.setObjectName("menu_bar")

                # File
                self.menu_file = QtWidgets.QMenu(self.menu_bar)
                self.menu_file.setAutoFillBackground(True)
                self.menu_file.setStyleSheet("")
                self.menu_file.setObjectName("menu_file")

                self.file_new = QtWidgets.QAction(self.m_window)
                self.file_new.setObjectName("file_new")
                self.file_new.triggered.connect(self.resetViewport)
                self.file_open = QtWidgets.QAction(self.m_window)
                self.file_open.setObjectName("file_open")
                self.file_open.triggered.connect(self.open3dScene)

                self.file_save = QtWidgets.QMenu(self.m_window)
                self.file_save.setObjectName("file_save")
                self.ex_all_ply = self.file_save.addAction("Stanford (.ply)")
                self.ex_all_ply.triggered.connect(lambda: self.exportAll(format = 1))
                self.ex_all_stl = self.file_save.addAction("Stl (.stl)")
                self.ex_all_stl.triggered.connect(lambda: self.exportAll(format = 2))
                self.ex_all_obj = self.file_save.addAction("Wavefront (.obj)")
                self.ex_all_obj.triggered.connect(lambda: self.exportAll(format = 3)) 
                self.ex_all_vtp = self.file_save.addAction("Vtp (.vtp)")
                self.ex_all_vtp.triggered.connect(lambda: self.exportAll(format = 4))
                self.ex_all_vtk = self.file_save.addAction("Vtk (.vtk)")
                self.ex_all_vtk.triggered.connect(lambda: self.exportAll(format = 5))

                self.file_import = QtWidgets.QMenu(self.m_window)
                self.file_import.setObjectName("file_import")
                # self.file_import.triggered.connect(vtk_reader.VtkReader)
                self.im_ply = self.file_import.addAction("Stanford (.ply)")
                self.im_ply.triggered.connect(lambda: self.importActor(format = 1))
                self.im_stl = self.file_import.addAction("Stl (.stl)")
                self.im_stl.triggered.connect(lambda: self.importActor(format = 2))
                self.im_obj = self.file_import.addAction("Wavefront (.obj)")
                self.im_obj.triggered.connect(lambda: self.importActor(format = 3)) 
                self.im_vtp = self.file_import.addAction("Vtp (.vtp)")
                self.im_vtp.triggered.connect(lambda: self.importActor(format = 4))
                self.im_vtk = self.file_import.addAction("Vtk (.vtk)")
                self.im_vtk.triggered.connect(lambda: self.importActor(format = 5))
                self.file_import.addSeparator()
                self.im_dcm = self.file_import.addAction("DICOM (.dcm)")
                self.im_dcm.triggered.connect(lambda: self.importActor(format = 6))
                self.im_mhd = self.file_import.addAction("MetaImage (.mhd)")
                self.im_mhd.triggered.connect(lambda: self.importActor(format = 7))

                self.file_export = QtWidgets.QMenu(self.m_window)
                self.file_export.setObjectName("file_export")
                self.ex_ply = self.file_export.addAction("Stanford (.ply)")
                self.ex_ply.triggered.connect(lambda: self.exportActor(format = 1))
                self.ex_stl = self.file_export.addAction("Stl (.stl)")
                self.ex_stl.triggered.connect(lambda: self.exportActor(format = 2))
                self.ex_obj = self.file_export.addAction("Wavefront (.obj)")
                self.ex_obj.triggered.connect(lambda: self.exportActor(format = 3)) 
                self.ex_vtp = self.file_export.addAction("Vtp (.vtp)")
                self.ex_vtp.triggered.connect(lambda: self.exportActor(format = 4))
                self.ex_vtk = self.file_export.addAction("Vtk (.vtk)")
                self.ex_vtk.triggered.connect(lambda: self.exportActor(format = 5))

                self.file_exit = QtWidgets.QAction(self.m_window)
                self.file_exit.setObjectName("file_exit")
                self.file_exit.triggered.connect(self.exit)

                self.menu_file.addAction(self.file_new)
                self.menu_file.addAction(self.file_open)
                self.menu_file.addSeparator()
                self.menu_file.addMenu(self.file_save)
                self.menu_file.addSeparator()
                self.menu_file.addMenu(self.file_import)
                self.menu_file.addMenu(self.file_export)
                self.menu_file.addSeparator()
                self.menu_file.addAction(self.file_exit)

                # Edit
                self.menuEdit = QtWidgets.QMenu(self.menu_bar)
                self.menuEdit.setAutoFillBackground(True)
                self.menuEdit.setStyleSheet("")
                self.menuEdit.setObjectName("menuEdit")

                self.actionUndo = QtWidgets.QAction(self.m_window)
                self.actionUndo.setObjectName("actionUndo")
                self.actionRedo = QtWidgets.QAction(self.m_window)
                self.actionRedo.setObjectName("actionRedo")

                self.menuEdit.addAction(self.actionUndo)
                self.menuEdit.addAction(self.actionRedo)

                # Window
                self.menuWindow = QtWidgets.QMenu(self.menu_bar)
                self.menuWindow.setAutoFillBackground(True)
                self.menuWindow.setStyleSheet("")
                self.menuWindow.setObjectName("menuWindow")

                self.actionSave_Screenshot = QtWidgets.QAction(self.m_window)
                self.actionSave_Screenshot.setObjectName("actionSave_Screenshot")
                self.actionSave_Screenshot.triggered.connect(self.windowScreenshot)

                self.reset_camera_action = QtWidgets.QAction(self.m_window)
                self.reset_camera_action.setObjectName("reset_camera_action")
                self.reset_camera_action.triggered.connect(lambda: self.camera.reset_orientation(self.vtk_viewport,
                                                                                                 self.ori_cam_settings))

                self.menu_geometric = QtWidgets.QMenu(self.m_window)
                self.menu_geometric.setObjectName("menu_mesh")

                self.menu_cell = QtWidgets.QMenu(self.m_window)
                self.menu_cell.setObjectName("menu_cell")

                self.menu_implicit = QtWidgets.QMenu(self.m_window)
                self.menu_implicit.setObjectName("menu_implicit")

                self.menu_isosurface = QtWidgets.QMenu(self.m_window)
                self.menu_isosurface.setObjectName("menu_isosurface") 

                self.menu_para = QtWidgets.QMenu(self.m_window)
                self.menu_para.setObjectName("menu_para")

                self.menuWindow.addMenu(self.menu_geometric)
                self.menuWindow.addMenu(self.menu_cell)
                self.menuWindow.addMenu(self.menu_implicit)
                self.menuWindow.addMenu(self.menu_isosurface)
                self.menuWindow.addMenu(self.menu_para)
                self.menuWindow.addSeparator()
                self.menuWindow.addAction(self.reset_camera_action)
                self.menuWindow.addSeparator()
                self.menuWindow.addAction(self.actionSave_Screenshot) 
                
                # Add Menu Bar to window
                self.m_window.setMenuBar(self.menu_bar)

                # # Test
                # self.test_window = QtWidgets.QMenu(self.menu_bar)
                # self.test_window.setAutoFillBackground(True)
                # self.test_window.setStyleSheet("")
                # self.test_window.setObjectName("test_window")
                # self.test_window.triggered.connect(self.testing)

                # Add Menu Bar to window
                self.m_window.setMenuBar(self.menu_bar)

                self.menu_bar.addAction(self.menu_file.menuAction())
                self.menu_bar.addAction(self.menuEdit.menuAction())
                self.menu_bar.addAction(self.menuWindow.menuAction())
                
                self.cube_mesh = self.menu_geometric.addAction("Cube")
                self.cube_mesh.triggered.connect(lambda: self.addNewActor(vtkTessellatedBoxSource()))
                self.sphere_mesh = self.menu_geometric.addAction("Sphere")
                self.sphere_mesh.triggered.connect(lambda: self.addNewActor(vtkSphereSource()))
                self.cylinder_mesh = self.menu_geometric.addAction("Cylinder")
                self.cylinder_mesh.triggered.connect(lambda: self.addNewActor(vtkCylinderSource()))
                self.cone_mesh = self.menu_geometric.addAction("Cone")
                self.cone_mesh.triggered.connect(lambda: self.addNewActor(vtkConeSource()))
                self.disk_mesh = self.menu_geometric.addAction("Disk")
                self.disk_mesh.triggered.connect(lambda: self.addNewActor(vtkDiskSource()))
                
                self.hp_cell = self.menu_cell.addAction("Hexagonal Prism")
                self.hp_cell.triggered.connect(lambda: self.addCellFunc(mode = 1))
                self.hexahedron_cell = self.menu_cell.addAction("Hexahedron")
                self.hexahedron_cell.triggered.connect(lambda: self.addCellFunc(mode = 2))
                self.pp_cell = self.menu_cell.addAction("Pentagonal Prism")
                self.pp_cell.triggered.connect(lambda: self.addCellFunc(mode = 3))
                self.ph_cell = self.menu_cell.addAction("Polyhedron")
                self.ph_cell.triggered.connect(lambda: self.addCellFunc(mode = 4))
                self.pyramid_cell = self.menu_cell.addAction("Pyramid")
                self.pyramid_cell.triggered.connect(lambda: self.addCellFunc(mode = 5))
                self.tetrahedron_cell = self.menu_cell.addAction("Tetrahedron")
                self.tetrahedron_cell.triggered.connect(lambda: self.addCellFunc(mode = 6))

                self.bool_imp = self.menu_implicit.addAction("Boolean")
                self.bool_imp.triggered.connect(lambda: self.addImplicitFunc(mode = 1))
                self.quadric_imp = self.menu_implicit.addAction("Quadric")
                self.quadric_imp.triggered.connect(lambda: self.addImplicitFunc(mode = 2))
                self.sphere_imp = self.menu_implicit.addAction("Sphere")
                self.sphere_imp.triggered.connect(lambda: self.addImplicitFunc(mode = 3))

                self.contour_iso = self.menu_isosurface.addAction("Contour Filter")
                self.contour_iso.triggered.connect(lambda: self.addIsoSurface(mode = 1))
                self.mc_iso = self.menu_isosurface.addAction("Marching Cubes")
                self.mc_iso.triggered.connect(lambda: self.addIsoSurface(mode = 2))

                self.bd_para = self.menu_para.addAction("Bohemian Dome")
                self.bd_para.triggered.connect(lambda: self.addParaFunc(mode = 1))
                self.cm_para = self.menu_para.addAction("Catalan Minimal")
                self.cm_para.triggered.connect(lambda: self.addParaFunc(mode = 2))
                self.cs_para = self.menu_para.addAction("Conic Spiral")
                self.cs_para.triggered.connect(lambda: self.addParaFunc(mode = 3))
                self.ellipsoid_para = self.menu_para.addAction("Ellipsoid")
                self.ellipsoid_para.triggered.connect(lambda: self.addParaFunc(mode = 4))
                self.mobius_para = self.menu_para.addAction("Mobius")
                self.mobius_para.triggered.connect(lambda: self.addParaFunc(mode = 5))
                self.pseudosphere_para = self.menu_para.addAction("Pseudosphere")
                self.pseudosphere_para.triggered.connect(lambda: self.addParaFunc(mode = 6))
                self.random_hills_para = self.menu_para.addAction("Random Hills")
                self.random_hills_para.triggered.connect(lambda: self.addParaFunc(mode = 7))
                self.spills_para = self.menu_para.addAction("Spline")
                self.spills_para.triggered.connect(lambda: self.addParaFunc(mode = 8))
                self.superellipsoid_para = self.menu_para.addAction("Super Ellipsoid")
                self.superellipsoid_para.triggered.connect(lambda: self.addParaFunc(mode = 9))
                self.supertoroid_para = self.menu_para.addAction("Super Toroid")
                self.supertoroid_para.triggered.connect(lambda: self.addParaFunc(mode = 10))
                self.torus_para = self.menu_para.addAction("Torus")
                self.torus_para.triggered.connect(lambda: self.addParaFunc(mode = 11))
                
                # Status Bar
                self.statusbar = QtWidgets.QStatusBar(self.m_window)
                self.statusbar.setObjectName("statusbar")
                self.m_window.setStatusBar(self.statusbar)

                # Scene Tab
                self.scene_tab = QtWidgets.QWidget()
                self.scene_tab.setObjectName("scene_tab")

                self.scene_frame = QtWidgets.QFrame(self.scene_tab)
                self.scene_frame.setGeometry(QtCore.QRect(0, 0, 371, 591))
                self.scene_frame.setAutoFillBackground(True)
                self.scene_frame.setStyleSheet(transparent_bg_col)
                self.scene_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.scene_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.scene_frame.setObjectName("scene_frame")
                self.scene_label_image_2 = QtWidgets.QLabel(self.scene_frame)
                self.scene_label_image_2.setGeometry(QtCore.QRect(0, 0, 371, 591))
                self.scene_label_image_2.setAutoFillBackground(True)
                self.scene_label_image_2.setStyleSheet(transparent_col)
                self.scene_label_image_2.setText("")
                self.scene_label_image_2.setPixmap(QtGui.QPixmap(stat_label_dir))
                self.scene_label_image_2.setScaledContents(True)
                self.scene_label_image_2.setObjectName("scene_label_image_2")

                self.frame_3 = QtWidgets.QFrame(self.scene_frame)
                self.frame_3.setGeometry(QtCore.QRect(15, 0, 341, 491))
                self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
                self.frame_3.setObjectName("frame_3")

                self.scene_frame_label = QtWidgets.QLabel(self.frame_3)
                self.scene_frame_label.setGeometry(QtCore.QRect(0, 38, 341, 361))
                self.scene_frame_label.setAutoFillBackground(True)
                self.scene_frame_label.setStyleSheet(transparent_bg_col)
                self.scene_frame_label.setText("")
                self.scene_frame_label.setPixmap(QtGui.QPixmap(properties_rect_dir))
                self.scene_frame_label.setScaledContents(True)
                self.scene_frame_label.setObjectName("scene_frame_label")

                # Transform Heading
                self.light_label = QtWidgets.QLabel(self.frame_3)
                self.light_label.setGeometry(QtCore.QRect(20, 48, 81, 31))
                self.light_label.setFont(self.font)
                self.light_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_label.setAutoFillBackground(True)
                self.light_label.setStyleSheet(style_3d3d3d)
                self.light_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.light_label.setObjectName("light_label")

                # Transparent
                self.light_checkbox = LightingCheckBox(self.frame_3, self.light_source, self.vtk_viewport)
                self.light_checkbox.setGeometry(QtCore.QRect(220, 55, 110, 20))
                self.light_checkbox.setFont(self.font)
                self.light_checkbox.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_checkbox.setAutoFillBackground(True)
                self.light_checkbox.setStyleSheet( "QCheckBox { spacing : 12px; \n"
                                                      "background-color: rgb(61, 61, 61);"
                                                        "color: rgb(217, 217, 217); }")
                self.light_checkbox.setObjectName("light_checkbox")
                self.vtk_widget.setLightingCheckbox(self.light_checkbox)
                self.light_checkbox.setChecked(True)

                # Location X
                self.light_location_x_label = QtWidgets.QLabel(self.frame_3)
                self.light_location_x_label.setGeometry(QtCore.QRect(10, 101, 79, 18))
                self.light_location_x_label.setFont(self.font)
                self.light_location_x_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_location_x_label.setAutoFillBackground(True)
                self.light_location_x_label.setStyleSheet(style_3d3d3d)
                self.light_location_x_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_location_x_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_location_x_label.setObjectName("location_x_label")

                self.light_location_x_slider = QtWidgets.QLabel(self.frame_3)
                self.light_location_x_slider.setGeometry(QtCore.QRect(114, 98, 207, 25))
                self.light_location_x_slider.setAutoFillBackground(True)
                self.light_location_x_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_location_x_slider.setText("")
                self.light_location_x_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.light_location_x_slider.setScaledContents(True)
                self.light_location_x_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.light_location_x_slider.setObjectName("light_location_x_slider")

                # 0 = res 1, 2, 3 = loc 4, 5, 6 = rot, 7, 8 ,9 = scale
                self.light_location_x_dispvalue = SliderDisVal(self.frame_3, self.light_location_x_slider, 20, 1, self, forLight = True)
                self.light_location_x_dispvalue.setGeometry(QtCore.QRect(114, 98, 207, 25))
                self.light_location_x_dispvalue.setFont(self.font)
                self.light_location_x_dispvalue.setAutoFillBackground(True)
                self.light_location_x_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_location_x_dispvalue.setText(f"{self.actor.getLocation(1)}")
                self.light_location_x_dispvalue.setScaledContents(True)
                self.light_location_x_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.light_location_x_dispvalue.setObjectName("light_location_x_dispvalue")
                self.light_location_x_dispvalue.clicked.connect(lambda: self.updateLightDetails(1, 
                                                                                          self.light_location_x_dispvalue,
                                                                                          self.light_location_x_dispvalue.prev_offset,
                                                                                          False))

                # Location Y
                self.light_location_y_label = QtWidgets.QLabel(self.frame_3)
                self.light_location_y_label.setGeometry(QtCore.QRect(10, 133, 79, 18))
                self.light_location_y_label.setFont(self.font)
                self.light_location_y_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_location_y_label.setAutoFillBackground(True)
                self.light_location_y_label.setStyleSheet(style_3d3d3d)
                self.light_location_y_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_location_y_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_location_y_label.setObjectName("light_location_y_label")

                self.light_location_y_slider = QtWidgets.QLabel(self.frame_3)
                self.light_location_y_slider.setGeometry(QtCore.QRect(114, 130, 207, 25))
                self.light_location_y_slider.setAutoFillBackground(True)
                self.light_location_y_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_location_y_slider.setText("")
                self.light_location_y_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.light_location_y_slider.setScaledContents(True)
                self.light_location_y_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.light_location_y_slider.setObjectName("light_location_y_slider")

                self.light_location_y_dispvalue = SliderDisVal(self.frame_3, self.light_location_y_slider, 20, 2, self, forLight = True)
                self.light_location_y_dispvalue.setGeometry(QtCore.QRect(114, 130, 207, 25))
                self.light_location_y_dispvalue.setFont(self.font)
                self.light_location_y_dispvalue.setAutoFillBackground(True)
                self.light_location_y_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_location_y_dispvalue.setText(f"{self.actor.getLocation(2)}")
                self.light_location_y_dispvalue.setScaledContents(True)
                self.light_location_y_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.light_location_y_dispvalue.setObjectName("light_location_y_dispvalue")
                self.light_location_y_dispvalue.clicked.connect(lambda: self.updateLightDetails(2, 
                                                                                          self.light_location_y_dispvalue,
                                                                                          self.light_location_y_dispvalue.prev_offset,
                                                                                          False))

                # Location Z
                self.light_location_z_label = QtWidgets.QLabel(self.frame_3)
                self.light_location_z_label.setGeometry(QtCore.QRect(10, 165, 79, 18))
                self.light_location_z_label.setFont(self.font)
                self.light_location_z_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_location_z_label.setAutoFillBackground(True)
                self.light_location_z_label.setStyleSheet(style_3d3d3d)
                self.light_location_z_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_location_z_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_location_z_label.setObjectName("light_location_z_label")

                self.light_location_z_slider = QtWidgets.QLabel(self.frame_3)
                self.light_location_z_slider.setGeometry(QtCore.QRect(114, 162, 207, 25))
                self.light_location_z_slider.setAutoFillBackground(True)
                self.light_location_z_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_location_z_slider.setText("")
                self.light_location_z_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.light_location_z_slider.setScaledContents(True)
                self.light_location_z_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.light_location_z_slider.setObjectName("light_location_z_slider")

                self.light_location_z_dispvalue = SliderDisVal(self.frame_3, self.light_location_z_slider, 20, 3, self, forLight = True)
                self.light_location_z_dispvalue.setGeometry(QtCore.QRect(114, 162, 207, 25))
                self.light_location_z_dispvalue.setFont(self.font)
                self.light_location_z_dispvalue.setAutoFillBackground(True)
                self.light_location_z_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_location_z_dispvalue.setText(f"{self.actor.getLocation(3)}")
                self.light_location_z_dispvalue.setScaledContents(True)
                self.light_location_z_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.light_location_z_dispvalue.setObjectName("light_location_z_dispvalue")
                self.light_location_z_dispvalue.clicked.connect(lambda: self.updateLightDetails(3, 
                                                                                          self.light_location_z_dispvalue,
                                                                                          self.light_location_z_dispvalue.prev_offset,
                                                                                          False))

                # Ambient
                self.light_ambient_label = QtWidgets.QLabel(self.frame_3)
                self.light_ambient_label.setGeometry(QtCore.QRect(10, 213, 79, 18))
                self.light_ambient_label.setFont(self.font)
                self.light_ambient_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_ambient_label.setAutoFillBackground(True)
                self.light_ambient_label.setStyleSheet(style_3d3d3d)
                self.light_ambient_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_ambient_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_ambient_label.setObjectName("light_ambient_label")

                self.ambient_colour_value_label = ColourButton(parent = self.frame_3, text = "",
                                                       light = self.light_source, mode = 1)
                self.ambient_colour_value_label.setGeometry(QtCore.QRect(114, 213, 207, 25))
                self.ambient_colour_value_label.setText("")
                self.ambient_colour_value_label.setScaledContents(True)
                self.ambient_colour_value_label.setAlignment(QtCore.Qt.AlignCenter)
                self.ambient_colour_value_label.setObjectName("ambient_colour_value_label")

                # Diffuse
                self.light_diffuse_label = QtWidgets.QLabel(self.frame_3)
                self.light_diffuse_label.setGeometry(QtCore.QRect(10, 255, 79, 18))
                self.light_diffuse_label.setFont(self.font)
                self.light_diffuse_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_diffuse_label.setAutoFillBackground(True)
                self.light_diffuse_label.setStyleSheet(style_3d3d3d)
                self.light_diffuse_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_diffuse_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_diffuse_label.setObjectName("light_diffuse_label")

                self.diffuse_colour_value_label = ColourButton(parent = self.frame_3, text = "",
                                                       light = self.light_source, mode = 2)
                self.diffuse_colour_value_label.setGeometry(QtCore.QRect(114, 255, 207, 25))
                self.diffuse_colour_value_label.setText("")
                self.diffuse_colour_value_label.setScaledContents(True)
                self.diffuse_colour_value_label.setAlignment(QtCore.Qt.AlignCenter)
                self.diffuse_colour_value_label.setObjectName("diffuse_colour_value_label")

                # Specular
                self.light_specular_label = QtWidgets.QLabel(self.frame_3)
                self.light_specular_label.setGeometry(QtCore.QRect(10, 297, 79, 18))
                self.light_specular_label.setFont(self.font)
                self.light_specular_label.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_specular_label.setAutoFillBackground(True)
                self.light_specular_label.setStyleSheet(style_3d3d3d)
                self.light_specular_label.setTextFormat(QtCore.Qt.AutoText)
                self.light_specular_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_specular_label.setObjectName("light_specular_label")

                self.specular_colour_value_label = ColourButton(parent = self.frame_3, text = "",
                                                       light = self.light_source, mode = 3)
                self.specular_colour_value_label.setGeometry(QtCore.QRect(114, 297, 207, 25))
                self.specular_colour_value_label.setText("")
                self.specular_colour_value_label.setScaledContents(True)
                self.specular_colour_value_label.setAlignment(QtCore.Qt.AlignCenter)
                self.specular_colour_value_label.setObjectName("specular_colour_value_label")


                # Power
                self.light_power = QtWidgets.QLabel(self.frame_3)
                self.light_power.setGeometry(QtCore.QRect(10, 348, 79, 18))
                self.light_power.setFont(self.font)
                self.light_power.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.light_power.setAutoFillBackground(True)
                self.light_power.setStyleSheet(style_3d3d3d)
                self.light_power.setTextFormat(QtCore.Qt.AutoText)
                self.light_power.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.light_power.setObjectName("light_power")

                self.light_power_slider = QtWidgets.QLabel(self.frame_3)
                self.light_power_slider.setGeometry(QtCore.QRect(114, 348, 207, 25))
                self.light_power_slider.setAutoFillBackground(True)
                self.light_power_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_power_slider.setText("")
                self.light_power_slider.setPixmap(QtGui.QPixmap(self.value_label_dir))
                self.light_power_slider.setScaledContents(True)
                self.light_power_slider.setAlignment(QtCore.Qt.AlignCenter)
                self.light_power_slider.setObjectName("light_power_slider")

                self.light_power_dispvalue = SliderDisVal(self.frame_3, self.light_power_slider, 500, 0, self, forLight = True)
                self.light_power_dispvalue.setGeometry(QtCore.QRect(114, 348, 207, 25))
                self.light_power_dispvalue.setFont(self.font)
                self.light_power_dispvalue.setAutoFillBackground(True)
                self.light_power_dispvalue.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                self.light_power_dispvalue.setText(f"{self.actor.getLocation(3)}")
                self.light_power_dispvalue.setScaledContents(True)
                self.light_power_dispvalue.setAlignment(QtCore.Qt.AlignCenter)
                self.light_power_dispvalue.setObjectName("light_power_dispvalue")
                self.light_power_dispvalue.clicked.connect(lambda: self.updateLightDetails(0, 
                                                                                          self.light_power_dispvalue,
                                                                                          self.light_power_dispvalue.prev_offset,
                                                                                          False))

                self.version_stat_label3 = QtWidgets.QLabel(self.scene_frame)
                self.version_stat_label3.setGeometry(QtCore.QRect(300, 560, 55, 16))
                self.version_stat_label3.setFont(self.font)
                self.version_stat_label3.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.version_stat_label3.setAutoFillBackground(True)
                self.version_stat_label3.setStyleSheet(stylesheet_version_text)
                self.version_stat_label3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.version_stat_label3.setObjectName("version_stat_label3")

                self.tab_widget.addTab(self.properties_tab, "")
                self.tab_widget.addTab(self.scene_tab, "")
                self.tab_widget.addTab(self.statistics_tab, "")

                self.retranslateUi(self.m_window)
                self.resetWidgetValues()

                # Starts at Properties Tab
                self.tab_widget.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(self.m_window)

        def open3dScene(self):
                actor_list = vtk_reader.VtkReader().reader(format = 8)
                if actor_list != []:
                        if self.checkMessageBox():
                                self.vtk_viewport.getRenderer().RemoveAllViewProps()
                                self.vtk_viewport.getRenderer().RemoveAllLights()
                                self.camera.reset_orientation(self.vtk_viewport, self.ori_cam_settings)
                                self.setHasActors(True)

                                for i in range(len(actor_list)):
                                        actor = actor_list[i]
                                        source = "3DS_Import"
                                        self.vtk_viewport.addActor(actor)
                                        self.actor.setActor(actor)
                                        self.actor.setSource(source)

                                        if i == 0:
                                                self.scene_actors = actorsdictlist.ActorsDictList()
                                                self.scene_actors.createDictList(actor, source) 
                                                self.actor.setActorDict(dictionary_list = self.scene_actors)
                                        else:  
                                                self.scene_actors.generateActorDict(actor = actor, source = source)
                                                self.actor.setActorDict(dictionary_list = self.scene_actors)

                                self.light_source = vtkLight()
                                self.light_source.SetPosition(3, 3, -3)
                                self.light_source.SetLightTypeToSceneLight()
                                self.light_source.SetPositional(True)
                                self.light_source.SetConeAngle(60)
                                self.ambient_colour_value_label.resetLight(self.light_source)
                                self.diffuse_colour_value_label.resetLight(self.light_source)
                                self.specular_colour_value_label.resetLight(self.light_source)
                                self.light_checkbox.resetLight(self.light_source)
                                self.light_checkbox.setChecked(True)
                                self.light_actor = vtkLightActor()
                                self.light_actor.SetLight(self.light_source)
                                self.vtk_viewport.getRenderer().AddViewProp(self.light_actor)
                                self.vtk_viewport.getRenderer().AddLight(self.light_source)
                                
                                self.updateActorSelector()
                                self.resetWidgetValues()

        def addNewActor(self, source = None):
                if source is not None:
                        if self.getHasActors() is True:
                                actor = self.actor.getActor()
                                actor.GetProperty().EdgeVisibilityOff()
                                self.actor.getActor().GetProperty().SetOpacity(1.0)
                                self.actor.setActor(actor)
                                self.scene_actors.updateDictList(self.actor.getID(), self.actor.getActorDict())
                        
                        self.setHasActors(True)

                        current_actor = self.actor.mapSourceToActor(source, vtkActor())
                        self.vtk_viewport.addActor(current_actor)

                        self.scene_actors.generateActorDict(actor = self.actor.getActor(), source = self.actor.getSource())
                        self.actor.setActorDict(dictionary_list = self.scene_actors)

                        self.resetWidgetValues()
                        self.updateActorSelector()

        def addCellFunc(self, mode = None):
                """
                Creating an unstructured grid representation from points to form cells
                """
                if mode is not None:
                        ug = vtkUnstructuredGrid()
                        if mode == 1:
                                source = "VTK_HexPrism"
                                numberOfVertices = 12
                                points = vtkPoints()

                                points.InsertNextPoint(0.0, 0.0, 1.0)
                                points.InsertNextPoint(1.0, 0.0, 1.0)
                                points.InsertNextPoint(1.5, 0.5, 1.0)
                                points.InsertNextPoint(1.0, 1.0, 1.0)
                                points.InsertNextPoint(0.0, 1.0, 1.0)
                                points.InsertNextPoint(-0.5, 0.5, 1.0)

                                points.InsertNextPoint(0.0, 0.0, 0.0)
                                points.InsertNextPoint(1.0, 0.0, 0.0)
                                points.InsertNextPoint(1.5, 0.5, 0.0)
                                points.InsertNextPoint(1.0, 1.0, 0.0)
                                points.InsertNextPoint(0.0, 1.0, 0.0)
                                points.InsertNextPoint(-0.5, 0.5, 0.0)

                                hexagonalPrism = vtkHexagonalPrism()
                                for i in range(0, numberOfVertices):
                                        hexagonalPrism.GetPointIds().SetId(i, i)     
                                ug.InsertNextCell(hexagonalPrism.GetCellType(),
                                                hexagonalPrism.GetPointIds())
                                ug.SetPoints(points)
                        if mode == 2:
                                source = "VTK_Hexadron"
                                numberOfVertices = 8
                                points = vtkPoints()
                                points.InsertNextPoint(0.0, 0.0, 0.0)
                                points.InsertNextPoint(1.0, 0.0, 0.0)
                                points.InsertNextPoint(1.0, 1.0, 0.0)
                                points.InsertNextPoint(0.0, 1.0, 0.0)
                                points.InsertNextPoint(0.0, 0.0, 1.0)
                                points.InsertNextPoint(1.0, 0.0, 1.0)
                                points.InsertNextPoint(1.0, 1.0, 1.0)
                                points.InsertNextPoint(0.0, 1.0, 1.0)

                                # Create a hexahedron from the points
                                hex_ = vtkHexahedron()
                                for i in range(0, numberOfVertices):
                                        hex_.GetPointIds().SetId(i, i)

                                # Add the points and hexahedron to an unstructured grid
                                ug.SetPoints(points)
                                ug.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())
                        if mode == 3:
                                source = "VTK_PentagonalPrism"
                                numberOfVertices = 10
                                # Create the points
                                points = vtkPoints()
                                radius = 1.0
                                height = 2
                                num_sides = 5

                                for i in range(num_sides):
                                        theta = 2.0 * vtkMath.Pi() * i / num_sides
                                        x = radius * math.cos(theta)
                                        y = radius * math.sin(theta)
                                        points.InsertNextPoint(x, y, 0.0)  # Bottom face points

                                for i in range(num_sides):
                                        theta = 2.0 * vtkMath.Pi() * i / num_sides
                                        x = radius * math.cos(theta)
                                        y = radius * math.sin(theta)
                                        points.InsertNextPoint(x, y, height)

                                # Pentagonal Prism
                                pentagonalPrism = vtkPentagonalPrism()
                                for i in range(0, numberOfVertices):
                                        pentagonalPrism.GetPointIds().SetId(i, i)
                                # Add the points and hexahedron to an unstructured grid
                                ug.SetPoints(points)
                                ug.InsertNextCell(pentagonalPrism.GetCellType(),
                                                        pentagonalPrism.GetPointIds())
                        if mode == 4:
                                source = "VTK_Polyhedron"
                                numberOfFaces = 12
                                points = vtkPoints()
                                points.InsertNextPoint(1.21412, 0, 1.58931)
                                points.InsertNextPoint(0.375185, 1.1547, 1.58931)
                                points.InsertNextPoint(-0.982247, 0.713644, 1.58931)
                                points.InsertNextPoint(-0.982247, -0.713644, 1.58931)
                                points.InsertNextPoint(0.375185, -1.1547, 1.58931)
                                points.InsertNextPoint(1.96449, 0, 0.375185)
                                points.InsertNextPoint(0.607062, 1.86835, 0.375185)
                                points.InsertNextPoint(-1.58931, 1.1547, 0.375185)
                                points.InsertNextPoint(-1.58931, -1.1547, 0.375185)
                                points.InsertNextPoint(0.607062, -1.86835, 0.375185)
                                points.InsertNextPoint(1.58931, 1.1547, -0.375185)
                                points.InsertNextPoint(-0.607062, 1.86835, -0.375185)
                                points.InsertNextPoint(-1.96449, 0, -0.375185)
                                points.InsertNextPoint(-0.607062, -1.86835, -0.375185)
                                points.InsertNextPoint(1.58931, -1.1547, -0.375185)
                                points.InsertNextPoint(0.982247, 0.713644, -1.58931)
                                points.InsertNextPoint(-0.375185, 1.1547, -1.58931)
                                points.InsertNextPoint(-1.21412, 0, -1.58931)
                                points.InsertNextPoint(-0.375185, -1.1547, -1.58931)
                                points.InsertNextPoint(0.982247, -0.713644, -1.58931)

                                # Dimensions are [numberOfFaces][numberOfFaceVertices]
                                dodechedronFace = [
                                        [0, 1, 2, 3, 4],
                                        [0, 5, 10, 6, 1],
                                        [1, 6, 11, 7, 2],
                                        [2, 7, 12, 8, 3],
                                        [3, 8, 13, 9, 4],
                                        [4, 9, 14, 5, 0],
                                        [15, 10, 5, 14, 19],
                                        [16, 11, 6, 10, 15],
                                        [17, 12, 7, 11, 16],
                                        [18, 13, 8, 12, 17],
                                        [19, 14, 9, 13, 18],
                                        [19, 18, 17, 16, 15]
                                ]

                                dodechedronFacesIdList = vtkIdList()
                                # Number faces that make up the cell.
                                dodechedronFacesIdList.InsertNextId(numberOfFaces)
                                for face in dodechedronFace:
                                        # Number of points in the face == numberOfFaceVertices
                                        dodechedronFacesIdList.InsertNextId(len(face))
                                        # Insert the pointIds for that face.
                                        [dodechedronFacesIdList.InsertNextId(i) for i in face]
                                ug.InsertNextCell(VTK_POLYHEDRON, dodechedronFacesIdList)
                                ug.SetPoints(points)

                        if mode == 5:
                                source = "VTK_Pyramid"
                                numberOfVertices = 5
                                points = vtkPoints()
                                p = [
                                        [1.0, 1.0, 0.0],
                                        [-1.0, 1.0, 0.0],
                                        [-1.0, -1.0, 0.0],
                                        [1.0, -1.0, 0.0],
                                        [0.0, 0.0, 1.0]
                                ]
                                for pt in p:
                                        points.InsertNextPoint(pt)

                                pyramid = vtkPyramid()
                                for i in range(0, numberOfVertices):
                                        pyramid.GetPointIds().SetId(i, i)

                                ug.SetPoints(points)
                                ug.InsertNextCell(pyramid.GetCellType(), pyramid.GetPointIds())

                        if mode == 6:
                                source = "VTK_Tetrahedron"
                                numberOfVertices = 4
                                points = vtkPoints()
                                points.InsertNextPoint(0, 0, 0)
                                points.InsertNextPoint(1, 0, 0)
                                points.InsertNextPoint(1, 1, 0)
                                points.InsertNextPoint(0, 1, 1)

                                tetra = vtkTetra()
                                for i in range(0, numberOfVertices):
                                        tetra.GetPointIds().SetId(i, i)

                                cellArray = vtkCellArray()
                                cellArray.InsertNextCell(tetra)

                                ug.SetPoints(points)
                                ug.SetCells(VTK_TETRA, cellArray)

                        mapper = vtkDataSetMapper()
                        mapper.SetInputData(ug)
                        actor = vtkActor()
                        actor.SetMapper(mapper)
                        self.vtk_viewport.addActor(actor)

                        self.actor.setActor(actor)
                        self.actor.setSource(source)

                        self.scene_actors.generateActorDict(actor = actor, source = source)
                        self.actor.setActorDict(dictionary_list = self.scene_actors)

                        self.resetWidgetValues()
                        self.updateActorSelector()

        def addParaFunc(self, mode = None):
                source = vtkParametricFunctionSource()
                if mode is not None:
                        if mode == 1:
                                func = vtkParametricBohemianDome()
                        if mode == 2:
                                func = vtkParametricCatalanMinimal()
                        if mode == 3:
                                func = vtkParametricConicSpiral()
                        if mode == 4:
                                func = vtkParametricEllipsoid()
                        if mode == 5:
                                func = vtkParametricMobius()
                        if mode == 6:
                                func = vtkParametricPseudosphere()
                        if mode == 7:
                                func = vtkParametricRandomHills()
                        if mode == 8:
                                func = vtkParametricSpline()
                        if mode == 9:
                                func = vtkParametricSuperEllipsoid()
                        if mode == 10:
                                func = vtkParametricSuperToroid()
                        if mode == 11:
                                func = vtkParametricTorus()
                        source.SetParametricFunction(func)
                        self.addNewActor(source)

        def addImplicitFunc(self, mode = None):
                if mode is not None:
                        if self.getHasActors() is True:
                                actor = self.actor.getActor()
                                actor.GetProperty().EdgeVisibilityOff()
                                self.actor.getActor().GetProperty().SetOpacity(1.0)
                                self.actor.setActor(actor)
                                self.scene_actors.updateDictList(self.actor.getID(), self.actor.getActorDict())
                        self.setHasActors(True)

                        if mode == 1:
                                # create a sphere
                                sphere = vtkSphere()
                                sphere.SetRadius(1)
                                sphere.SetCenter(1, 0, 0)
                                # create a box
                                box = vtkBox()
                                box.SetBounds(-1, 1, -1, 1, -1, 1)

                                # combine the two implicit functions
                                boolean = vtkImplicitBoolean()
                                boolean.SetOperationTypeToDifference()
                                # boolean.SetOperationTypeToUnion()
                                # boolean.SetOperationTypeToIntersection()
                                boolean.AddFunction(box)
                                boolean.AddFunction(sphere)

                                # The sample function generates a distance function from the implicit
                                # function. This is then contoured to get a polygonal surface.
                                sample = vtkSampleFunction()
                                sample.SetImplicitFunction(boolean)
                                sample.SetModelBounds(-1, 2, -1, 1, -1, 1)
                                source = "VTK_Implicit_Bool"

                        if mode == 2:
                                quadric = vtkQuadric()
                                quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)
                                sample = vtkSampleFunction()
                                sample.SetImplicitFunction(quadric)
                                sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
                                source = "VTK_Implicit_Quadric"

                        if mode == 3:
                                sphere = vtkSphere()
                                sphere.SetCenter(0, 0, 0)
                                sphere.SetRadius(0.5)
                                sample = vtkSampleFunction()
                                sample.SetImplicitFunction(sphere)
                                source = "VTK_Implicit_Sphere"
                        sample.SetSampleDimensions(40, 40, 40)
                        sample.ComputeNormalsOff()

                        # contour
                        surface = vtkContourFilter()
                        surface.SetInputConnection(sample.GetOutputPort())
                        surface.SetValue(0, 0.0)

                        # mapper
                        mapper = vtkPolyDataMapper()
                        mapper.SetInputConnection(surface.GetOutputPort())
                        mapper.ScalarVisibilityOff()
                        actor = vtkActor()
                        actor.SetMapper(mapper)
                        self.vtk_viewport.addActor(actor)

                        self.actor.setActor(actor)
                        self.actor.setSource(source)

                        self.scene_actors.generateActorDict(actor = actor, source = source)
                        self.actor.setActorDict(dictionary_list = self.scene_actors)

                        self.resetWidgetValues()
                        self.updateActorSelector()

        def addIsoSurface(self, mode = None):
                if mode is not None:
                        if mode == 1:
                                import_actor, name, source = vtk_reader.VtkReader().reader(format = 9)
                        elif mode == 2:
                                import_actor, name, source = vtk_reader.VtkReader().reader(format = 10)
                        if import_actor is not None:
                                if self.getHasActors() is True:
                                        actor = self.actor.getActor()
                                        actor.GetProperty().EdgeVisibilityOff()
                                        self.actor.getActor().GetProperty().SetOpacity(1.0)
                                        self.actor.setActor(actor)
                                        self.scene_actors.updateDictList(self.actor.getID(), self.actor.getActorDict())
                                actor = import_actor
                                self.setHasActors(True)
                                self.vtk_viewport.addActor(actor)

                                self.actor.setActor(actor)
                                self.actor.setSource(source)

                                self.scene_actors.generateActorDict(actor = actor, source = source, name = name)
                                self.actor.setActorDict(dictionary_list = self.scene_actors)

                                self.resetWidgetValues()
                                self.updateActorSelector()
                
        def deleteActor(self):
               self.vtk_viewport.getRenderer().RemoveActor(self.actor.getActor())
               new_dict = self.scene_actors.deleteActorDict(self.actor.getID())
               self.actor.setActorDict(dictionary = new_dict)
               self.updateActorSelector()      

        def exportAll(self, format = None):
                if format is not None:
                        actors_list = self.scene_actors.getActorProperties()
                        name_list = self.scene_actors.getActorNames()
                        if actors_list != ["Null"]:
                                for i in range(len(actors_list)):
                                        actor = actors_list[i]
                                        if actor.GetClassName() != "vtkVolume":  
                                                actor.GetProperty().EdgeVisibilityOff()
                                                actor.GetProperty().SetOpacity(1.0)
                                vtk_writer.VtkWriter().multipleWriter(actors_list = actors_list, name_list = name_list, 
                                                        format = format)
                                        
        def exportActor(self, format = None):
                if format is not None:
                        if self.getHasActors() is True:
                                actor = self.actor.getActor()
                                if actor.GetClassName() != "vtkVolume":  
                                        actor.GetProperty().EdgeVisibilityOff()
                                        self.actor.getActor().GetProperty().SetOpacity(1.0)
                                self.actor.setActor(actor)
                                self.scene_actors.updateDictList(self.actor.getID(), self.actor.getActorDict())
                                vtk_writer.VtkWriter().singleWriter(actor = self.actor.getActor(), name = self.actor.getName(), 
                                                     format = format)
        
        def importActor(self, e = None, format = None):
                if format is not None: 
                        if self.getHasActors() is True:
                                actor = self.actor.getActor()
                                actor.GetProperty().EdgeVisibilityOff()
                                self.actor.getActor().GetProperty().SetOpacity(1.0)
                                self.actor.setActor(actor)
                                self.scene_actors.updateDictList(self.actor.getID(), self.actor.getActorDict())
                        
                        actor, name, source = vtk_reader.VtkReader().reader(format = format)
                        if actor is not None:
                                self.setHasActors(True)

                                # current_actor = self.actor.mapSourceToActor(source, vtkActor())
                                self.vtk_viewport.addActor(actor)

                                self.actor.setActor(actor)
                                self.actor.setSource(source)

                                self.scene_actors.generateActorDict(actor = actor, source = source, name = name)
                                self.actor.setActorDict(dictionary_list = self.scene_actors)

                                self.resetWidgetValues()
                                self.updateActorSelector()

        def setHasActors(self, bool):
               self.has_actors = bool

        def getHasActors(self):
                return self.has_actors

        def resetWidgetValues(self):
                # print(self.vtk_viewport.getRenderer().VisibleActorCount())
                self.wireframe_checkbox.setChecked(False)
                self.vtk_viewport.updateRenderer()
                if self.getHasActors() is True:
                        #       Reset button values
                        if (self.actor.getSource() is None or isinstance(self.actor.getSource(), str)):
                                self.resolution_dispvalue.setText("Null")
                        else:
                                self.resolution_dispvalue.setText(f"{self.actor.getResolution()}")
                        self.location_x_dispvalue.setText(f"{self.actor.getLocation(1):.3f}")
                        self.location_y_dispvalue.setText(f"{self.actor.getLocation(2):.3f}")
                        self.location_z_dispvalue.setText(f"{self.actor.getLocation(3):.3f}")

                        self.rotation_x_dispvalue.setText(f"{self.actor.getRotation(4):.3f}")
                        self.rotation_y_dispvalue.setText(f"{self.actor.getRotation(5):.3f}")
                        self.rotation_z_dispvalue.setText(f"{self.actor.getRotation(6):.3f}")

                        self.scale_x_dispvalue.setText(f"{self.actor.getScale(7):.3f}")
                        self.scale_y_dispvalue.setText(f"{self.actor.getScale(8):.3f}")
                        self.scale_z_dispvalue.setText(f"{self.actor.getScale(9):.3f}")

                        current_colour = self.actor.getColour()
                        self.colour_value_label.setAutoFillBackground(True)
                        self.colour_value_label.setStyleSheet("background-color: "
                                                        f"{self.colour_value_label.rgbToHex((current_colour))};"
                                                        "border-radius: 0.3125rem;"
                                                        "padding: 0.625rem 2.875rem;"
                                                        "border-style: solid; border-width: 0.125rem;"
                                                        "border-color: #d9d9d9;")
                else:
                        self.resolution_dispvalue.setText("Null")
                        self.location_x_dispvalue.setText("Null")
                        self.location_y_dispvalue.setText("Null")
                        self.location_z_dispvalue.setText("Null")

                        self.rotation_x_dispvalue.setText("Null")
                        self.rotation_y_dispvalue.setText("Null")
                        self.rotation_z_dispvalue.setText("Null")

                        self.scale_x_dispvalue.setText("Null")
                        self.scale_y_dispvalue.setText("Null")
                        self.scale_z_dispvalue.setText("Null")

                        current_colour = self.actor.getColour()
                        self.colour_value_label.setAutoFillBackground(True)
                        self.colour_value_label.setStyleSheet("background-color: #ffffff;"
                                                        "border-radius: 0.3125rem;"
                                                        "padding: 0.625rem 2.875rem;"
                                                        "border-style: solid; border-width: 0.125rem;"
                                                        "border-color: #d9d9d9;")
                self.light_location_x_dispvalue.setText(f"{self.light_source.GetPosition()[0]:.3f}")
                self.light_location_y_dispvalue.setText(f"{self.light_source.GetPosition()[1]:.3f}")
                self.light_location_z_dispvalue.setText(f"{self.light_source.GetPosition()[2]:.3f}")
                self.light_power_dispvalue.setText(f"{self.light_source.GetIntensity() * 1000 :.3f}")

                current_colour = self.light_source.GetAmbientColor()
                current_colour = tuple(int(value * 255) for value in current_colour)
                self.ambient_colour_value_label.setStyleSheet(f"background-color: {self.ambient_colour_value_label.rgbToHex((current_colour))};"
                                                "border-radius: 0.3125rem;"
                                                "padding: 0.625rem 2.875rem;"
                                                "border-style: solid; border-width: 0.125rem;"
                                                "border-color: #d9d9d9;")
                
                current_colour = self.light_source.GetSpecularColor()
                current_colour = tuple(int(value * 255) for value in current_colour)
                self.specular_colour_value_label.setStyleSheet(f"background-color: {self.specular_colour_value_label.rgbToHex((current_colour))};"
                                                "border-radius: 0.3125rem;"
                                                "padding: 0.625rem 2.875rem;"
                                                "border-style: solid; border-width: 0.125rem;"
                                                "border-color: #d9d9d9;")
                
                current_colour = self.light_source.GetDiffuseColor()
                current_colour = tuple(int(value * 255) for value in current_colour)
                self.diffuse_colour_value_label.setStyleSheet(f"background-color: {self.diffuse_colour_value_label.rgbToHex((current_colour))};"
                                                "border-radius: 0.3125rem;"
                                                "padding: 0.625rem 2.875rem;"
                                                "border-style: solid; border-width: 0.125rem;"
                                                "border-color: #d9d9d9;")
                
                self.updateOutliner()
                self.updateSceneStats()

        def updateActorDetails(self, mode, disp_val_label, value, keyboard_bool):
                if (mode == 0):
                        self.actor.setResolution(float(value), keyboard_bool)
                        self.vtk_viewport.updateRenderer()
                        text = disp_val_label.textIntChecker(f"{self.actor.getResolution()}")
                        disp_val_label.setText(text)

                elif (mode == 1 or mode == 2 or mode == 3):
                        self.actor.setLocation(mode, float(value), keyboard_bool)
                        self.vtk_viewport.updateRenderer()
                        text = disp_val_label.textIntChecker(f"{self.actor.getLocation(mode)}")
                        disp_val_label.setText(text)

                elif (mode == 4 or mode == 5 or mode == 6):
                        self.actor.setRotation(mode, float(value), keyboard_bool)
                        self.vtk_viewport.updateRenderer()
                        value = self.actor.getRotation(mode)
                        # print(value)
                        if (value < 0) or (value < 0 and int(value) != 0):
                                value += 360
                        elif round(value) == 360:
                                value = 0
                        text = disp_val_label.textIntChecker(f"{value}")
                        disp_val_label.setText(text)

                elif (mode == 7 or mode == 8 or mode == 9):
                        self.actor.setScale(mode, float(value), keyboard_bool)
                        self.vtk_viewport.updateRenderer()
                        value = self.actor.getScale(mode)
                        text = disp_val_label.textIntChecker(f"{value}")
                        disp_val_label.setText(text)

                self.updateSceneStats()

        def updateLightDetails(self, mode, disp_val_label, value, keyboard_bool):

                if (mode == 1):
                        if (keyboard_bool is True):
                                self.light_source.SetPosition(float(value), 
                                                self.light_source.GetPosition()[1], 
                                                self.light_source.GetPosition()[2]) 
                        else:
                                self.light_source.SetPosition(self.light_source.GetPosition()[0]+float(value), 
                                                self.light_source.GetPosition()[1], 
                                                self.light_source.GetPosition()[2]) 
                        self.light_source.SetFocalPoint(self.light_source.GetPosition()[0]-3, 
                                        self.light_source.GetPosition()[1]-3, 
                                        self.light_source.GetPosition()[2]+3) 
                        self.vtk_viewport.updateRenderer()
                        text = disp_val_label.textIntChecker(f"{self.light_source.GetPosition()[0]}")
                        disp_val_label.setText(text)
                
                elif (mode == 2):
                        if (keyboard_bool is True):
                                self.light_source.SetPosition(self.light_source.GetPosition()[0], 
                                                float(value), 
                                                self.light_source.GetPosition()[2]) 
                        else:
                                self.light_source.SetPosition(self.light_source.GetPosition()[0], 
                                                self.light_source.GetPosition()[1]+float(value), 
                                                self.light_source.GetPosition()[2]) 
                        self.light_source.SetFocalPoint(self.light_source.GetPosition()[0]-3, 
                                        self.light_source.GetPosition()[1]-3, 
                                        self.light_source.GetPosition()[2]+3) 
                        self.vtk_viewport.updateRenderer()
                        text = disp_val_label.textIntChecker(f"{self.light_source.GetPosition()[1]}")
                        disp_val_label.setText(text)
                
                elif (mode == 3):
                        if (keyboard_bool is True):
                                self.light_source.SetPosition(self.light_source.GetPosition()[0], 
                                                self.light_source.GetPosition()[1], 
                                                float(value)) 
                        else:
                                self.light_source.SetPosition(self.light_source.GetPosition()[0], 
                                                self.light_source.GetPosition()[1], 
                                                self.light_source.GetPosition()[2]+float(value)) 
                        self.light_source.SetFocalPoint(self.light_source.GetPosition()[0]-3, 
                                        self.light_source.GetPosition()[1]-3, 
                                        self.light_source.GetPosition()[2]+3) 
                        self.vtk_viewport.updateRenderer()
                        text = disp_val_label.textIntChecker(f"{self.light_source.GetPosition()[2]}")
                        disp_val_label.setText(text)

                elif (mode == 0):
                        if (keyboard_bool is True):
                                input = float(value) / 1000
                                if input < 0:
                                        input = 0
                                elif input > 1:
                                        input = 1
                        else:
                                input = self.light_source.GetIntensity() + float(value)
                                if input < 0:
                                        input = 0
                                elif input > 1:
                                        input = 1
                        self.light_source.SetIntensity(input)
                        self.vtk_viewport.updateRenderer()
                        text = disp_val_label.textIntChecker(f"{self.light_source.GetIntensity() * 1000}")
                        disp_val_label.setText(text)

        def updateSceneStats(self):
                _translate = QtCore.QCoreApplication.translate
                actor_list = self.scene_actors.getActorProperties()
                total_obj = 0
                total_vert = 0
                total_edge = 0
                total_face = 0
                current_obj = 1
                if actor_list != ["Null"]:
                        for i in range(len(actor_list)):
                                total_obj += 1

                                polydata = vtkPolyData()
                                polydata.ShallowCopy(actor_list[i].GetMapper().GetInput())

                                total_vert += self.scene_actors.getVertices(polydata)
                                total_edge += self.scene_actors.getEdges(polydata)
                                total_face += self.scene_actors.getFaces(polydata)

                        polydata = vtkPolyData()
                        current_actor = self.actor
                        polydata.ShallowCopy(current_actor.getActor().GetMapper().GetInput())
                        current_vert = self.scene_actors.getVertices(polydata)
                        current_edge = self.scene_actors.getEdges(polydata)
                        current_face = self.scene_actors.getFaces(polydata)
                        current_name = current_actor.getName()
                else:
                        total_obj = "Null"
                        total_vert = "Null"
                        total_edge = "Null"
                        total_face = "Null"
                        current_obj = "Null"
                        current_vert = "Null"
                        current_edge = "Null"
                        current_face = "Null"
                        current_name = "Null"
                if len(current_name) > 15:
                        current_name = current_name[:15-2] + "..."
                self.stats_heading.setText(_translate("MainWindow", f"Scene | {current_name}"))
                self.stats_category_value.setText(_translate("MainWindow", f"<html><head/><body><p>{current_obj}/ {total_obj} </p><p>{current_vert}/ {total_vert}</p><p>{current_edge}/ {total_edge}</p><p>{current_face}/ {total_face}</p><p><br/></p><p><br/></p><p><br/></p><p>20</p><p>396</p><p>0.01</p><p>1000</p></body></html>"))

        def switchLabelImage(self, bool, image_label: QtWidgets.QLabel, 
                             disp_val_label): # True = selected False = not selected
                if (bool == -1):
                        image_label.setPixmap(QtGui.QPixmap(self.value_label_hov_dir)) 
                
                elif (bool == True):
                        # print("selected")
                        disp_val_label.setStyleSheet("padding-left: 30px;\n"
                                                     "background-color: rgba(255, 255, 255, 0);\ncolor: rgb(22, 22, 22);")
                        disp_val_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        image_label.setPixmap(QtGui.QPixmap(self.value_label_sel_dir))
                else:
                        # print("deselected")
                        disp_val_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(217, 217, 217);")
                        disp_val_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                        image_label.setPixmap(QtGui.QPixmap(self.value_label_dir))

        def changeActor(self, text: str):
                if text != "Null":
                        self.actor.getActor().GetProperty().EdgeVisibilityOff()
                        self.actor.getActor().GetProperty().SetOpacity(1.0)
                        new_dict = self.scene_actors.getActorDict(text, True)
                        self.actor.setActorDict(dictionary = new_dict)
                        self.resetWidgetValues()

        def updateActorSelector(self):
                self.actor_dropdown_selector.clear()
                self.actor_dropdown_selector.addItems(self.scene_actors.getActorNames())
                if self.actor_dropdown_selector.currentText() != "Null":
                        i = self.actor_dropdown_selector.findText(self.actor.getName())
                        if i != -1:
                                self.actor_dropdown_selector.setCurrentIndex(i)

        def updateOutliner(self):
                _translate = QtCore.QCoreApplication.translate
                
                name_list = self.scene_actors.getActorNames()
                source_list = self.scene_actors.getActorSources()
                # print(source_list)
                if name_list == [ "Null" ]:
                        self.outliner_text_label.setText(_translate("MainWindow", "Scene"))        
                else:     
                        text = "Scene"
                        for i in range(len(name_list)):
                                name_text = name_list[i]
                                if len(name_text) > 10:
                                        name_text = name_text[:10-2] + "..."
                                text += f"\n\n>     {name_text:<25}{self.scene_actors.getActorType(source_list[i])}" 
                        self.outliner_text_label.setText(_translate("MainWindow", text))

        def resetViewport(self):
                if self.checkMessageBox() is True:
                        self.vtk_viewport.getRenderer().RemoveAllViewProps()
                        self.vtk_viewport.getRenderer().RemoveAllLights()
                        
                        # Initialise Camera
                        self.camera.reset_orientation(self.vtk_viewport, self.ori_cam_settings)
                        self.vtk_viewport.getRenderer().AddActor(self.axes_actor)

                        # Initialise current actor
                        self.actor = actor.Actor()
                        current_actor_source = vtkConeSource()
                        current_actor = self.actor.mapSourceToActor(current_actor_source, vtkActor())
                        self.vtk_viewport.addActor(current_actor)
                        self.setHasActors(True)
                        self.colour_value_label.resetActor(self.actor)
                        
                        # Actors in VTK scene
                        self.scene_actors = actorsdictlist.ActorsDictList()
                        self.scene_actors.createDictList(current_actor, 
                                                        current_actor_source) 
                        self.actor.setActorDict(dictionary_list = self.scene_actors)

                        self.light_source = vtkLight()
                        self.light_source.SetPosition(3, 3, -3)
                        self.light_source.SetLightTypeToSceneLight()
                        self.light_source.SetPositional(True)
                        self.light_source.SetConeAngle(60)
                        self.ambient_colour_value_label.resetLight(self.light_source)
                        self.diffuse_colour_value_label.resetLight(self.light_source)
                        self.specular_colour_value_label.resetLight(self.light_source)
                        self.light_checkbox.resetLight(self.light_source)
                        self.light_checkbox.setChecked(True)
                        self.light_actor = vtkLightActor()
                        self.light_actor.SetLight(self.light_source)
                        self.vtk_viewport.getRenderer().AddViewProp(self.light_actor)
                        self.vtk_viewport.getRenderer().AddLight(self.light_source)
                        
                        self.updateActorSelector()
                        self.resetWidgetValues()

        def checkMessageBox(self):
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(msg_box.Question)
                msg_box.setWindowTitle("Save")
                msg_box.setText("Save before closing?")
                msg_box.setStandardButtons(msg_box.Yes | msg_box.No | msg_box.Cancel)
                reply = msg_box.exec_()
                if reply == msg_box.Yes:
                        self.exportAll(format = 3)
                        return True
                elif reply == msg_box.No:
                        return True
                elif reply == msg_box.Cancel:
                        return False
        def exit(self):
                if self.checkMessageBox() is True:
                        sys.exit()

        def windowScreenshot(self):
                options = QtWidgets.QFileDialog.Options()
                options |= QtWidgets.QFileDialog.DontUseNativeDialog
                file_filter = "PNG (*.png);;JPEG (*.jpeg)"
                selected_filter, selected_file = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "./export/MyScene", 
                                                                                       file_filter, options=options)
                if selected_filter == "":
                        return
                
                if selected_file == 'PNG (*.png)':
                        writer = vtkPNGWriter()
                        writer.SetFileName(selected_filter + ".png")
                elif selected_file == 'JPEG (*.jpeg)':
                        writer = vtkJPEGWriter()
                        writer.SetFileName(selected_filter + ".jpeg")
                else:
                        return
                
                self.vtk_viewport.getRenderer().RemoveActor(self.axes_actor)

                window_to_image_filter = vtkWindowToImageFilter()
                window_to_image_filter.SetInput(self.vtk_viewport.getRenderWindow())
                window_to_image_filter.SetScale(5)
                window_to_image_filter.Update()

                writer.SetInputConnection(window_to_image_filter.GetOutputPort())
                writer.Write()

                self.vtk_viewport.getRenderer().AddActor(self.axes_actor)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "GeoGrafiX"))
                self.version_stat_label_2.setText(_translate("MainWindow", "v1.0"))
                self.version_stat_label3.setText(_translate("MainWindow", "v1.0"))
                self.resolution_label.setText(_translate("MainWindow", "Resolution"))
                self.transform_label.setText(_translate("MainWindow", "Transform"))
                self.light_label.setText(_translate("MainWindow", "Light"))
                self.wireframe_checkbox.setText(_translate("MainWindow", "Wireframe"))
                self.light_checkbox.setText(_translate("MainWindow", "Enable"))
                self.scale_z_label.setText(_translate("MainWindow", "Z"))
                self.location_x_label.setText(_translate("MainWindow", "Location X"))
                self.location_y_label.setText(_translate("MainWindow", "Y"))
                self.rotation_z_label.setText(_translate("MainWindow", "Z"))
                self.light_location_x_label.setText(_translate("MainWindow", "Location X"))
                self.light_location_y_label.setText(_translate("MainWindow", "Y"))
                self.light_location_z_label.setText(_translate("MainWindow", "Z"))
                self.light_ambient_label.setText(_translate("MainWindow", "Ambient"))
                self.light_diffuse_label.setText(_translate("MainWindow", "Diffuse"))
                self.light_specular_label.setText(_translate("MainWindow", "Specular"))
                self.light_power.setText(_translate("MainWindow", "Power (W)"))
                self.rotation_y_label.setText(_translate("MainWindow", "Y"))
                self.location_z_label.setText(_translate("MainWindow", "Z"))
                self.scale_x_label.setText(_translate("MainWindow", "Scale X"))
                self.scale_y_label.setText(_translate("MainWindow", "Y"))
                self.rotation_x_label.setText(_translate("MainWindow", "Rotation X"))
                self.colour_label.setText(_translate("MainWindow", "Colour"))
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.properties_tab), _translate("MainWindow", "Properties"))
                self.version_stat_label.setText(_translate("MainWindow", "v1.0"))
                self.stats_category_label.setText(_translate("MainWindow", "<html><head/><body><p>Objects</p><p>Vertices</p><p>Edges</p><p>Faces<br/></p><p><br/></p><p><span style=\" font-weight:600;\">Camera</span></p><p><br/></p><p>FOV</p><p>Focal Length</p><p>Clip Start</p><p>Clip End</p></body></html>"))
                # self.stats_category_value.setText(_translate("MainWindow", "<html><head/><body><p>num_actor_selected/ total_actors </p><p>num_vert_selected/ total_vert</p><p>num_edg_selected/ total_edg</p><p>num_face_selected/ total_face</p><p><br/></p><p><br/></p><p><br/></p><p>20</p><p>396</p><p>0.01</p><p>1000</p></body></html>"))
                # self.stats_heading.setText(_translate("MainWindow", "Scene | actor_name"))
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.scene_tab), _translate("MainWindow", "Scene"))
                self.tab_widget.setTabText(self.tab_widget.indexOf(self.statistics_tab), _translate("MainWindow", "Statistics"))
                self.menu_file.setTitle(_translate("MainWindow", "File"))
                self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
                self.menuWindow.setTitle(_translate("MainWindow", "Viewport"))
                self.file_new.setText(_translate("MainWindow", "New"))
                self.file_open.setText(_translate("MainWindow", "Open"))
                self.file_save.setTitle(_translate("MainWindow", "Save"))
                self.file_import.setTitle(_translate("MainWindow", "Import"))
                self.file_export.setTitle(_translate("MainWindow", "Export"))
                self.file_exit.setText(_translate("MainWindow", "Exit"))
                self.actionUndo.setText(_translate("MainWindow", "Undo"))
                self.actionRedo.setText(_translate("MainWindow", "Redo"))
                self.actionSave_Screenshot.setText(_translate("MainWindow", "Save Screenshot"))

                # self.test_window.setTitle(_translate("MainWindow", "Testing"))
                self.reset_camera_action.setText(_translate("MainWindow", "Reset Camera"))
                self.menu_geometric.setTitle(_translate("MainWindow", "Geometric"))
                self.menu_implicit.setTitle(_translate("MainWindow", "Implicit Function"))
                self.menu_isosurface.setTitle(_translate("MainWindow", "Iso-Surface"))
                self.menu_para.setTitle(_translate("MainWindow", "Parametric"))
                self.menu_cell.setTitle(_translate("MainWindow", "Cell"))

class QtVtkFrame:
        def __init__(self):
            self.setRenderer()
            self.setRenderWindow()
            # self.setInteractor()

        # def loadAxis(self, vtk_widget):
        def loadAxis(self, axes):
            # parent_actor = vtkAssembly()
            self.addActor(axes)
              
        # Add actor to scene
        def addActor(self, actor: vtkActor):
                if actor.GetClassName() == "vtkAxesActor" or actor.GetClassName() == "vtkOpenGLActor" or actor.GetClassName() == "vtkActor":
                        self.getRenderer().AddActor(actor)
                elif actor.GetClassName() == "vtkVolume":      
                        self.getRenderer().AddVolume(actor) 
                self.updateRenderer()

        def setRenderer(self):
            # Initialise Renderer
            self.renderer = vtkRenderer()
            self.renderer.SetBackground(0.239, 0.239, 0.239)
            self.renderer.ResetCamera()

        def getRenderer(self):
            return self.renderer

        def setRenderWindow(self):
            self.render_window = vtkRenderWindow()
            self.render_window.AddRenderer(self.getRenderer())
        
        def getRenderWindow(self):
            return self.render_window
        
        def updateRenderer(self):
            self.getRenderWindow().Render()

class Camera:
        """
        Initialises Scene camera.
        """
        def setCamera(self, camera):
                self.camera = camera

                self.camera.SetPosition(9.0, 5.0, 7.0)
                self.camera.SetFocalPoint(0, 0, 0)
        
        def getCamera(self):
                return self.camera
        
        def setClipping(self, near, far):
                self.camera.SetClippingRange(near, far)
                
        def setFOV(self, zoom):
                self.camera.SetViewAngle(zoom)

        def get_orientation(self, qvtkFrame: QtVtkFrame):
                """
                Get the camera orientation.
                :param ren: The renderer.
                :return: The orientation parameters.
                """
                cam_settings = dict()
                renderer = qvtkFrame.getRenderer()
                camera = renderer.GetActiveCamera()
                cam_settings['position'] = camera.GetPosition()
                cam_settings['focal point'] = camera.GetFocalPoint()
                cam_settings['view up'] = camera.GetViewUp()
                cam_settings['distance'] = camera.GetDistance()
                cam_settings['clipping range'] = camera.GetClippingRange()
                cam_settings['orientation'] = camera.GetOrientation()
                return cam_settings
        
        def reset_orientation(self, qvtkFrame: QtVtkFrame, cam_settings: dict):
                """
                Set the orientation of the camera.
                :param ren: The renderer.
                :param p: The orientation parameters.
                :return:
                """
                renderer = qvtkFrame.getRenderer()
                camera = renderer.GetActiveCamera()
                camera.SetPosition(cam_settings['position'])
                camera.SetFocalPoint(cam_settings['focal point'])
                camera.SetViewUp(cam_settings['view up'])
                camera.SetDistance(cam_settings['distance'])
                camera.SetClippingRange(cam_settings['clipping range'])

                qvtkFrame.render_window.Render()

class CustomQVTKRenderWindowInteractor(QVTKRenderWindowInteractor):
        def __init__(self, parent, main_window: GuiWindow, rw: QtVtkFrame, checkbox: QtWidgets.QCheckBox = None):
                super().__init__(parent, rw = rw)
                self.setWireframeCheckbox(checkbox)
                self.GetRenderWindow().GetInteractor().SetInteractorStyle(vtkInteractorStyleTrackballCamera())
                # self.render_window = rw
                self.main_window = main_window

        def initViewportCam(self, camera: Camera, ori_cam_settings: dict):
                """
                Initialise Camera & Save original setting reference
                """
                self.camera = camera
                self.ori_cam_settings = ori_cam_settings

        def keyPressEvent(self, event):
                key = event.key()
                if key == QtCore.Qt.Key_W or key == QtCore.Qt.Key_S:
                        return
                elif key == QtCore.Qt.Key_Escape:
                        if (self.wireframe_checkbox is not None):
                                self.wireframe_checkbox.setChecked(not self.wireframe_checkbox.isChecked())
                                self.wireframe_checkbox.checkbox_state_changed()
                                return        
                elif key == QtCore.Qt.Key_L:
                        if (self.light_checkbox is not None):
                                self.light_checkbox.setChecked(not self.light_checkbox.isChecked())
                                self.light_checkbox.checkbox_state_changed()
                                return
                elif key == QtCore.Qt.Key_Delete:
                        number_of_actors = self.main_window.vtk_viewport.getRenderer().VisibleActorCount() - 2 # light and axes
                        
                        if (number_of_actors > 0 or self.main_window.getHasActors() is True):
                                self.main_window.deleteActor()
                                if number_of_actors == 1:
                                        self.main_window.setHasActors(False)
                                else:
                                       self.main_window.setHasActors(True)
                        else:
                               self.main_window.setHasActors(False) 
                        self.main_window.resetWidgetValues()

                elif key == QtCore.Qt.Key_R:
                        self.camera.reset_orientation(self.main_window.vtk_viewport, self.ori_cam_settings)
                                         
        def setWireframeCheckbox(self, checkbox):
                """
                Initialise WireframeCheckbox
                """
                self.wireframe_checkbox = checkbox

        def setLightingCheckbox(self, checkbox):
                """
                Initialise LightingCheckbox
                """
                self.light_checkbox = checkbox

class ActorDropdownSelector(QtWidgets.QComboBox):
        """
        Creates dropdown to select actor
        """
        def __init__(self, parent, m_win: GuiWindow):
                super().__init__(parent)
                self.setEditable(True)
                self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
                self.typing = False
                self.main_window = m_win

        def leaveEvent(self, event):
                self.clearFocus()
                self.setName()

        def focusInEvent(self, event):
                if self.currentText() != "Null":
                        self.setEditable(True)
                        self.typing = True
                        super().focusInEvent(event)

        def keyPressEvent(self, event):
                if self.typing is True:   
                        key = event.key()     
                        if (key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Escape): 
                                self.clearFocus()
                                self.setName()
                        super().keyPressEvent(event)

        def setName(self):
                name = self.currentText()
                self.main_window.actor.setName(name)
                self.main_window.scene_actors.updateDictList(self.main_window.actor.getID(), 
                                                             self.main_window.actor.getActorDict())
                self.main_window.updateOutliner()
                self.main_window.updateActorSelector()
                self.main_window.updateSceneStats()
           
class SliderDisVal(QtWidgets.QLabel):
        """
        Creates sliders that can take keyboard input when clicked.
        """
        clicked = QtCore.pyqtSignal()
        def __init__(self, parent, image_label, factor, mode, gui_win: GuiWindow, forLight: bool = False):
                super().__init__(parent)
                self.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.image_label = image_label
                self.factor = factor
                self.mode = mode
                self.main_win = gui_win
                self.forLightBool = forLight
                self.resetVariables()

        def resetVariables(self):
                self.mouse_down = False
                self.is_typing = False
                self.will_type = False
                self.will_drag = False

                self.ori_mouse_pos = 0
                self.prev_offset = 0
                self.hide_mouse_pos = (0,0)

                self.setMouseTracking(True)
                self.hovered = False
               
        def enterEvent(self, event):
                if (self.is_typing is False and self.mouse_down is False 
                        and self.will_type is False and self.is_typing is False):
                        self.main_win.switchLabelImage(-1, self.image_label, self)

        def leaveEvent(self, event):
                if (self.is_typing is False and self.mouse_down is False 
                        and self.will_type is False and self.is_typing is False):
                        self.main_win.switchLabelImage(False, self.image_label, self)
                else:
                        self.setSliderValue(self.text())

        def mouseMoveEvent(self, event: QtGui.QMouseEvent):
                if self.main_win.getHasActors() is True:
                        if (self.text() != "Null" and event.buttons() == QtCore.Qt.LeftButton):
                                # Exit mouse press and enter mouse move
                                if (self.will_drag == False): 
                                        self.main_win.switchLabelImage(False, self.image_label, self)
                                        self.will_drag = True
                                        self.mouse_down = False
                                        return
                                
                                # Take drag ori input to allow start at 0
                                if (self.will_drag == True and self.mouse_down == False):
                                        user32 = ctypes.windll.user32
                                        user32.ShowCursor(False)
                                        self.hide_mouse_pos = (event.globalX(), event.globalY())
                                        self.ori_mouse_pos = event.globalX()
                                        # self.will_drag = True
                                        self.mouse_down = True
                                        self.is_typing is False
                                        self.will_type = False
                                        return
                                offset = (event.globalX()-self.ori_mouse_pos) / self.factor
                                if (offset < 0 and event.globalX() <= 2):
                                        pyautogui.moveTo(1918, event.globalY())
                                        self.prev_offset = 0
                                        self.ori_mouse_pos = 1920
                                        return
                                elif (offset > 0 and event.globalX() >= 1918):
                                        pyautogui.moveTo(2, event.globalY())
                                        self.prev_offset = 0
                                        self.ori_mouse_pos = 0
                                        return
                                if (offset == self.prev_offset):
                                        return
                        
                                self.prev_offset = offset
                                self.ori_mouse_pos = event.globalX()
                                self.clicked.emit()

        def mousePressEvent(self, event: QtGui.QMouseEvent):
                if self.main_win.getHasActors() is True:
                        if (self.text() != "Null" and event.buttons() == QtCore.Qt.LeftButton):
                                self.mouse_down = True
                                self.will_drag = False
                                self.is_typing is False
                                self.will_type = True

        def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
                if self.main_win.getHasActors() is True:
                        if (self.text() != "Null" and self.will_drag is False and self.will_type is True): # ready to type
                                self.main_win.switchLabelImage(True, self.image_label, self)

                                self.setText(f"{self.textIntChecker(self.text())}")
                                self.is_typing = True
                                self.mouse_down = False

                        if (self.text() != "Null" and self.will_drag is True and self.will_type is False): # exit dragging
                                pyautogui.moveTo(self.hide_mouse_pos[0], self.hide_mouse_pos[1])
                                user32 = ctypes.windll.user32
                                user32.ShowCursor(True)
                                self.mouse_down = False
                                self.is_typing = False

                        self.will_type = False
                        self.will_drag = False
                        self.ori_mouse_pos = 0
                        self.prev_offset = 0
                        self.hide_mouse_pos = (0,0)

        def keyPressEvent(self, event):
                if (self.is_typing is True):
                        text = self.text()
                        key = event.key()

                        if QtCore.Qt.Key_0 <= key <= QtCore.Qt.Key_9:  # Accept numbers
                                if (text == "0"):
                                        text = str(key - QtCore.Qt.Key_0)
                                else:
                                        text += str(key - QtCore.Qt.Key_0)
                                self.setText(text)

                        elif key == QtCore.Qt.Key_Plus:    # + - * / ^ = 
                                if (text == "0"):
                                        text = "+"
                                else:
                                        text += " + "
                                self.setText(text)
                        elif key == QtCore.Qt.Key_Minus:    
                                if (text == "0"):
                                        text = "-"
                                else:
                                        text += " - "
                                self.setText(text)
                        elif key == QtCore.Qt.Key_Asterisk:    
                                text += " * "
                                self.setText(text)
                        elif key == QtCore.Qt.Key_Slash:    
                                text += " / "
                                self.setText(text)
                        elif key == QtCore.Qt.Key_AsciiCircum:    
                                text += " ^ "
                                self.setText(text)

                        elif key == QtCore.Qt.Key_Backspace:    # Backspace to delete
                                if (len(text) == 1):
                                        text = "0"
                                        self.setText(text)
                                elif (text[-1] == " "):
                                        text = text[:-3]
                                        self.setText(text)
                                elif (text != ""):
                                        text = text[:-1]
                                        self.setText(text)

                        elif key == QtCore.Qt.Key_Period:       # Allow full stop
                                if(self.decimalChecker(text) is False):
                                        if (self.numChecker(text[-1]) is False):
                                                text += "0."
                                        else:
                                                text += "."
                                        self.setText(text)

                        # Enter to finish typing
                        elif (key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Equal
                              or key == QtCore.Qt.Key_Escape):       
                                self.setSliderValue(text)

        def setSliderValue(self, text):
                self.is_typing = False
                text = self.evalStringToExpression(text)
                self.main_win.switchLabelImage(False, self.image_label, self)
                if self.forLightBool is False:
                        self.main_win.updateActorDetails(self.mode, self, text, True)
                else:
                        self.main_win.updateLightDetails(self.mode, self, text, True)

        def evalStringToExpression(self, expression):
                # Get the rightmost character
                expression = expression.replace(" ", "")
                rightmost_char = expression[-1]
                if rightmost_char in "+-*/^.":
                        expression = expression[:-1]
                if "^" in expression:
                        expression = expression.replace("^", "**")
                try:
                        return f"{eval(expression)}"
                except SyntaxError:
                        return f"{0}"
        
        def decimalChecker(self, text):
                for char in reversed(text):
                        if char == ".":
                                return True # Encounter decimal
                        elif char == " ":
                                return False # Encounter space
                return False # No decimal
        
        def numChecker(self,text):
                try:
                        float(text)
                        return True
                except ValueError:
                        return False
                
        def textIntChecker(self, text):
                eval_text = eval(text)
                if abs(eval_text) <= 0.0009:
                       eval_text = 0
                if eval_text == int(eval_text):
                        text = f"{int(eval_text)}"
                else:
                        text =  f"{eval_text:.3f}"
                return text

class WireframeCheckBox(QtWidgets.QCheckBox):
        """
        Creates checkbox to display wireframe.
        """
        def __init__(self, parent, actor, viewport, main_window: GuiWindow):
                super().__init__(parent)
                self.clicked.connect(self.checkbox_state_changed)
                self.main_window = main_window
                self.viewport = viewport
                self.actor = actor

        def checkbox_state_changed(self):
                if self.main_window.getHasActors() is True:
                        actor = self.actor.getActor()
                        if self.isChecked():
                                actor.GetProperty().EdgeVisibilityOn()
                                actor.GetProperty().SetOpacity(0.5)
                        else:
                                actor.GetProperty().EdgeVisibilityOff()
                                actor.GetProperty().SetOpacity(1.0)
                        self.viewport.updateRenderer()

class LightingCheckBox(QtWidgets.QCheckBox):
        """
        Creates checkbox to display lights.
        """
        def __init__(self, parent, light: vtkLight, viewport: QtVtkFrame):
                super().__init__(parent)
                self.clicked.connect(self.checkbox_state_changed)
                self.viewport = viewport
                self.light = light

        def resetLight(self, light: vtkLight):
                self.light = light         

        def checkbox_state_changed(self):
                if self.isChecked():
                        self.light.SwitchOn()
                else:
                        self.light.SwitchOff()
                self.viewport.updateRenderer()

class ColourButton(QtWidgets.QLabel):
        """
        Creates button to change actor or light colour.
        """
        def __init__(self, parent, text, actor = None, light: vtkLight = None, mode = None):
                super().__init__(parent = parent, text = text)
                self.actor = actor
                self.light =light
                self.mode = mode
                current_colour = (255, 255, 255)

                if self.actor is not None and self.actor.getActor().GetClassName() != "vtkVolume":
                        current_colour = self.actor.getColour()
                elif self.light is not None:
                        if self.mode == 1:
                                current_colour = self.light.GetAmbientColor()
                        elif self.mode == 2:
                                current_colour = self.light.GetDiffuseColor()
                        elif self.mode == 3:
                                current_colour = self.light.GetSpecularColor()
                        current_colour = tuple(int(value * 255) for value in current_colour)
                self.setAutoFillBackground(True)
                self.setStyleSheet(f"background-color: {self.rgbToHex((current_colour))};"
                                                "border-radius: 0.3125rem;"
                                                "padding: 0.625rem 2.875rem;"
                                                "border-style: solid; border-width: 0.125rem;"
                                                "border-color: #d9d9d9;")

        def mousePressEvent(self, event):
                if self.actor is not None and self.actor.getActor().GetClassName() != "vtkVolume":
                        current_colour = self.actor.getColour()
                        
                elif self.light is not None:
                        if self.mode == 1:
                                current_colour = self.light.GetAmbientColor()
                        elif self.mode == 2:
                                current_colour = self.light.GetDiffuseColor()
                        elif self.mode == 3:
                                current_colour = self.light.GetSpecularColor()
                        current_colour = tuple(int(value * 255) for value in current_colour)

                else:
                        return

                colour = QtWidgets.QColorDialog(self)
                colour.setCurrentColor(QtGui.QColor(*current_colour))
                colour = colour.getColor() 
                self.setAutoFillBackground(True)
                self.setStyleSheet(f"background-color: {colour.name()};"
                                                "border-radius: 0.3125rem;"
                                                "padding: 0.625rem 2.875rem;"
                                                "border-style: solid; border-width: 0.125rem;"
                                                "border-color: #d9d9d9;")
                selected_colour = (colour.red(), colour.green(), colour.blue())
                selected_colour = tuple((value / 255) for value in selected_colour)

                if self.actor is not None and self.actor.getActor().GetClassName() != "vtkVolume":
                        self.actor.setColour(selected_colour)
                        

                elif self.light is not None:

                        if self.mode == 1:
                                current_colour = self.light.SetAmbientColor(*selected_colour)
                        elif self.mode == 2:
                                current_colour = self.light.SetDiffuseColor(*selected_colour)
                        elif self.mode == 3:
                                current_colour = self.light.SetSpecularColor(*selected_colour)

        def resetLight(self, light: vtkLight):
                self.light = light  

        def resetActor(self, actor: actor.Actor):
                self.actor = actor

        def rgbToHex(self, rgb):
                return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


