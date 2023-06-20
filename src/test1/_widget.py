"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""

from distutils.command.install_egg_info import safe_name
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

if TYPE_CHECKING:
    import napari

import json
import os
from enum import Enum
from functools import partial

import napari
import numpy as np
from magicgui import magic_factory
from napari.utils import progress
from napari.layers import Labels, Points, Image
from qtpy.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QDialog,
    QMessageBox,
)
from skimage.filters import (
    threshold_isodata,
    threshold_li,
    threshold_otsu,
    threshold_triangle,
    threshold_yen,
)

from magicgui.widgets import PushButton, Slider, Label, FileEdit, Container, ComboBox
from glob import glob
# import nest_asyncio
# nest_asyncio.apply()



@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")



class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.setLayout(QHBoxLayout())

        # self.btn = QPushButton("Normalize")
        # self.btn.clicked.connect(self._normalize)

        # self.btn_ch = QPushButton("Annotate")
        # self.btn_ch.clicked.connect(self._annotate)

        # self.btn_sv = QPushButton("save")
        # self.btn_sv.clicked.connect(self.save_stk_json)

        # self.btn_ld = QPushButton("visual")
        # self.btn_ld.clicked.connect(self.show_anno)

        self.layer_combos = []
        self.gt_layer_combo = self.add_labels_combo_box("Label")
        # self.sv_layer_combo = self.add_labels_combo_box("Anno")

        self.viewer.layers.events.inserted.connect(self._reset_layer_options)
        self.viewer.layers.events.removed.connect(self._reset_layer_options)
        # self.layout().addWidget(self.btn)
        # self.layout().addWidget(self.btn_ch)
        # self.layout().addWidget(self.btn_sv)
        # self.layout().addWidget(self.btn_ld)
        # self.layout().addStretch()



        self.c_controller = Container(layout = "horizontal", widgets= [
            ComboBox(label='Layer', choices= [layer for layer in self.viewer.layers if isinstance(layer, Image)], name = "combox"), 
            PushButton(value=True, text="Normalize",    name="btn"),
            PushButton(value=True, text="Annotate",name="btn_ch"),
            PushButton(value=True, text="Save",    name="btn_sv"),
            PushButton(value=True, text="Visualize",   name="btn_ld"),
            ])
        # self.c_file_manager = Container(layout="horizontal", widgets=[
        #     FileEdit(value="dataset/", label="Image File: ",      name="txt_img_file",  filter="*.png"),
        #     FileEdit(value="dataset/", label="Annotation File: ", name="txt_annt_file", filter="*.json"),
        # ])
        container = Container(widgets=[
            # self.c_file_manager, 
            self.c_controller], labels=False)
        self.viewer.window.add_dock_widget(container, area= "bottom")
        
        # self.c_file_manager.txt_img_file.changed.connect(self.load_img_file)
        # self.c_file_manager.txt_annt_file.changed.connect(self.load_annot_file)
        
        self.c_controller.btn.clicked.connect(self._normalize)
        self.c_controller.btn_ch.clicked.connect(self._annotate)
        self.c_controller.btn_sv.clicked.connect(self.save_stk_json)
        self.c_controller.btn_ld.clicked.connect(self.show_anno)


    def add_labels_combo_box(self, label_text):
        combo_row = QWidget()
        combo_row.setLayout(QHBoxLayout())
        combo_row.layout().setContentsMargins(0, 0, 0, 0)
        new_combo_label = QLabel(label_text)
        combo_row.layout().addWidget(new_combo_label)
        new_layer_combo = QComboBox(self)
        new_layer_combo.addItems(
            [
                layer.name
                for layer in self.viewer.layers
                if isinstance(layer, Points)
                # if isinstance(layer, Labels)
            ]
        )
        combo_row.layout().addWidget(new_layer_combo)
        self.layer_combos.append(new_layer_combo)
        self.layout().addWidget(combo_row)
        return new_layer_combo

    def _normalize(self):
        
        print("napari has", len(self.viewer.layers), "layers")
        
        gt_layer = self.viewer.layers[self.c_controller.combox.value.name]
        # gt_layer = self.viewer.layers[self.sv_layer_combo.currentText()]

        labels_layer = self.viewer.add_image(
            gt_layer.data, name=f"{gt_layer.name}_norm"
        )  # self.viewer.layers[0]
        
        da = labels_layer.data
        p_max = np.max(da, axis = None).compute()
        p_min = np.min(da, axis = None).compute()
        
        print(labels_layer.contrast_limits_range)
        labels_layer.contrast_limits_range = (p_min, p_max)
        print(labels_layer.contrast_limits_range)

        

    def _annotate(self):
        
        # print(type(self.c_controller.combox.value.name))
        
        gt_layer = self.viewer.layers[self.c_controller.combox.value.name]
        # gt_layer = self.viewer.layers[self.sv_layer_combo.currentText()]

        # print(gt_layer.name)

        # new_points = self.viewer.add_layer(napari.layers.Points(name = f"{gt_layer.name}_lab", face_color = "transparent",
        #                         edge_color = "blue", size = 30))

        # pts_layer = self.viewer.add_points(np.empty((0, 3)), ndim = 3, name = f"{gt_layer.name}_lab", face_color = "transparent", edge_color = "blue", size = 20)

        self.viewer.add_points(
            np.empty((0, 3)),
            ndim=3,
            name=f"{gt_layer.name}_lab",
            face_color="red",
            size=5,
        )

        # test_points = np.random.randint(0,1000,size=(20000,3))
        # self.viewer.add_points(test_points, size=30, face_color="red")

    def show_anno(self):
        
        gt_layer = self.viewer.layers[self.gt_layer_combo.currentText()]

        # data_points = np.array(self.viewer.layers[f"{gt_layer.name}_lab"].data)

        # if f"{gt_layer.name}_lab2" not in self.viewer.layers:
        #     self.viewer.add_points(
        #         data_points,
        #         ndim=3,
        #         name=f"{gt_layer.name}_lab2",
        #         face_color="transparent",
        #         edge_color="blue",
        #         size=20,
        #     )

        # else:
        #     self.viewer.layers[f"{gt_layer.name}_lab2"].data = data_points
            
        data_points = np.array(self.viewer.layers[f"{gt_layer.name}"].data)

        if f"{gt_layer.name}_vis" not in self.viewer.layers:
            self.viewer.add_points(
                data_points,
                ndim=3,
                name=f"{gt_layer.name}_vis",
                face_color="transparent",
                edge_color="blue",
                size=20,
            )

        else:
            self.viewer.layers[f"{gt_layer.name}_vis"].data = data_points
                       
            

    def save_stk_json(self):

        print(self.c_controller.combox.value.name)
        print(self.viewer.layers)
        print(self.viewer.layers[self.c_controller.combox.value.name])
        
   
        dlg = QMessageBox()
        dlg.setWindowTitle("I have a question!")
        dlg.setText("Do you want to save annotation for layer: " + f"{self.viewer.layers[self.c_controller.combox.value.name].name}")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            print("Yes!")
            self.save_fl()
        else:
            print("No!")

   
    def save_fl(self):   
        sv_layer = self.viewer.layers[self.c_controller.combox.value.name]
        # sv_layer = self.viewer.layers[self.sv_layer_combo.currentText()]
        inp_path = sv_layer.source.path
        print(inp_path)

        
        gt_layer = self.viewer.layers[self.gt_layer_combo.currentText()]
        
        if gt_layer.name.endswith("_lab") or gt_layer.name.endswith("_GT"):  
            if sv_layer.name  == gt_layer.name.replace("_lab", ""):
                save_name = gt_layer.name.replace("_lab", "_GT")
                save_name2 = gt_layer.name.replace("_lab", "_GT_all")
            elif sv_layer.name  == gt_layer.name.replace("_GT", ""):
                save_name = f"{gt_layer.name}"
                save_name2 = f"{gt_layer.name}_all"
            else:
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("The annotation and image folder names not matched")
                msg.exec()
                return
        else:
            save_name = f"{gt_layer.name}_GT"
            save_name2 = f"{gt_layer.name}_GT_all"


        # print(save_name)
        # print(inp_path)

        save_folder = os.path.join(os.path.dirname(inp_path), save_name)

        # save_folder = (
        #     inp_path.replace(inp_path.split("/")[-1], "")
        #     + save_name
        # )
        
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)        
            
        label_stk = gt_layer.data

        files_name = os.listdir(inp_path)
        # files_name = glob('*.png') + glob('*.tiff') + glob('*.tif')
        
        for i in range(sv_layer.data.shape[0]):
            ext = os.path.splitext(files_name[i])[1][1:]
            if ext in ["tiff", "tif", "png"]:
                outFile = os.path.join(save_folder, files_name[i].replace(ext , "json"))

            # if files_name[i].endswith(".tif"):
            #     outFile = save_folder + files_name[i].replace(
            #         ".tif", ".json"
            #     )
            # elif files_name[i].endswith(".tiff"):
            #     outFile = save_folder + files_name[i].replace(
            #         ".tiff", ".json"
            #     )
                
            # elif files_name[i].endswith(".png"):
            #     outFile = save_folder + files_name[i].replace(
            #         ".png", ".json"
            #     )
            else:
                continue
                
            data = {"img_name": files_name[i]}
            if len(label_stk[label_stk[:, 0] == i][:, 1:].tolist()) != 0:
                data["labels"] = label_stk[label_stk[:, 0] == i][
                    :, 1:
                ].tolist()
                with open(outFile, "w") as fo:
                    json.dump(data, fo)

        # also save the annotation of the entire stack
        save_folder2 = os.path.join(os.path.dirname(inp_path), save_name2)

        # save_folder2 = (
        #     inp_path.replace(inp_path.split("/")[-1], "")
        #     + save_name2
        # )
        if not os.path.exists(save_folder2):
            os.makedirs(save_folder2)

        stk_file = os.path.join(save_folder2, "annotation.json")
        stk_data = {"folder_name": inp_path}
        stk_data["labels"] = label_stk.tolist()
        with open(stk_file, "w") as fo:
            json.dump(stk_data, fo)




    def _reset_layer_options(self, event):
        for combo in self.layer_combos:
            combo.clear()
            combo.addItems(
                [
                    layer.name
                    for layer in self.viewer.layers
                    if isinstance(layer, Points)
                    # if isinstance(layer, Labels)
                ]
            )
            
        self.c_controller.combox.choices = [layer for layer in self.viewer.layers if isinstance(layer, Image)]
        





# https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/
# https://stackoverflow.com/questions/33618656/python-windowserror-error-123-the-filename-directory-name-or-volume-label-s
# https://forum.image.sc/t/adding-empty-shapes-layer-after-adding-rgb-image-causes-runtimewarning/75676/3

# fix invalid cast value:
# Downgrading numpy to <1.24.0 works as a temporary fix:
# pip install numpy==1.23.5