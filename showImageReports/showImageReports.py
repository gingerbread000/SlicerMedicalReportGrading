import logging
import os
from typing import Annotated, Optional
import json
import copy
import vtk
import qt
import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLScalarVolumeNode


#
# showImageReports
#

class showImageReports(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "showImageReports"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
            This is an example of scripted loadable module bundled in an extension.
            See more information in <a href="https://github.com/organization/projectname#showImageReports">module documentation</a>.
            """
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
            This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
            and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
            """

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#

def registerSampleData():
    """
    Add data sets to Sample Data module.
    """
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData
    iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # showImageReports1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='showImageReports',
        sampleName='showImageReports1',
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, 'showImageReports1.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames='showImageReports1.nrrd',
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums='SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
        # This node name will be used when the data set is loaded
        nodeNames='showImageReports1'
    )

    # showImageReports2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='showImageReports',
        sampleName='showImageReports2',
        thumbnailFileName=os.path.join(iconsPath, 'showImageReports2.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames='showImageReports2.nrrd',
        checksums='SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
        # This node name will be used when the data set is loaded
        nodeNames='showImageReports2'
    )


#
# showImageReportsParameterNode
#

@parameterNodeWrapper
class showImageReportsParameterNode:
    """
    The parameters needed by module.

    inputVolume - The volume to threshold.
    imageThreshold - The value at which to threshold the input volume.
    invertThreshold - If true, will invert the threshold.
    thresholdedVolume - The output volume that will contain the thresholded volume.
    invertedVolume - The output volume that will contain the inverted thresholded volume.
    """
    inputVolume: vtkMRMLScalarVolumeNode
    imageThreshold: Annotated[float, WithinRange(-100, 500)] = 100
    invertThreshold: bool = False
    thresholdedVolume: vtkMRMLScalarVolumeNode
    invertedVolume: vtkMRMLScalarVolumeNode


#
# showImageReportsWidget
#

class showImageReportsWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None
        self.save_score_path = None
        self.text_cn_en = [
            0, {
                0:{
                    "usage":"报告评分说明：上方共显示1份原始影像描述及4个不同AI模型生成的影像描述内容。\n评价主要体现相对性能排序。例如整体印象条目，第一名4分，第二名3分，第三名2分，第四名1分。如果都比较正确难以区分可以都给4分，如果都不正确可以全部给1分。如果描述内容完全不相关请填0.",
                    "label_8":"整体印象", "label_9":"病灶定位", "label_10":"病灶数量", "label_11":"病变种类", "label_12":"边界描述", "label_13":"密度描述", "label_14":"报告完整性", "label_15":"形状描述",   "label_16":"正常结构描述"
                    }, 
                1:{
                    "usage":"Report Scoring Instructions:The above section displays one original image description along with four image descriptions generated by different AI models. The evaluation primarily reflects a relative performance ranking. For example, in the <Overall Impression> category: First place receives 4 points, Second place 3 points, Third place 2 points, Fourth place 1 point. If all descriptions are fairly accurate and difficult to distinguish, you may assign 4 points to all. Conversely, if none are accurate, you may assign 1 point to all. If the description is completely unrelated, please enter 0.",
                    "label_8":"Overall Impression", "label_9":"Lesion localization", "label_10":"Lesion count", "label_11":"Type of lesion", "label_12":"Boundary description", "label_13":"Density description", "label_14":"Report completeness", "label_15":"Shape description",   "label_16":"Normal structure description"
                },
                }
            ]
        self.origin_report = [0, None]

    def setup(self) -> None:
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/showImageReports.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = showImageReportsLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.pushButton.connect('clicked(bool)', self.onApplyButton )
        self.ui.saveButton.connect('clicked(bool)', self.onApplySaveButton )
        self.ui.trans_lang.connect('clicked(bool)', self.onApplyTransButton )
        self.ui.show_origin_reports.connect('clicked(bool)', self.onShowOriginButton )
        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self) -> None:
        """
        Called when the application closes and the module widget is destroyed.
        """
        self.removeObservers()

    def enter(self) -> None:
        """
        Called each time the user opens this module.
        """
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """
        Called each time the user opens a different module.
        """
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)

    def onSceneStartClose(self, caller, event) -> None:
        """
        Called just before the scene is closed.
        """
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """
        Called just after the scene is closed.
        """
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """
        Ensure parameter node exists and observed.
        """
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.inputVolume:
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.inputVolume = firstVolumeNode

    def setParameterNode(self, inputParameterNode: Optional[showImageReportsParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
            self._checkCanApply()

    def _checkCanApply(self, caller=None, event=None) -> None:
        if self._parameterNode and self._parameterNode.inputVolume and self._parameterNode.thresholdedVolume:
            self.ui.saveButton.toolTip = "Compute output volume"
            self.ui.saveButton.enabled = True
        else:
            self.ui.saveButton.toolTip = "Select input and output volume nodes"
            self.ui.saveButton.enabled = True

    def onApplyTransButton(self) -> None:
        """
        Run processing when user clicks "Apply" button.
        """
        if self.text_cn_en[0] == 0:
            self.text_cn_en[0] = 1
            for key in self.text_cn_en[1][1]:
                if hasattr(self.ui, key):
                    attr = getattr(self.ui, key)
                    attr.setText(self.text_cn_en[1][1][key])
        elif self.text_cn_en[0] == 1:
            self.text_cn_en[0] = 0
            for key in self.text_cn_en[1][0]:
                if hasattr(self.ui, key):
                    attr = getattr(self.ui, key)
                    attr.setText(self.text_cn_en[1][0][key])
    def onShowOriginButton(self ) -> None:
        if self.origin_report[1] != None:
            if self.origin_report[0] == 0:
                self.ui.rawReport.setText(self.origin_report[1])
                self.origin_report[0] = 1
            elif self.origin_report[0] == 1:
                self.ui.rawReport.setText("")
                self.origin_report[0] = 0

        return

    def onApplyButton(self) -> None:
        """
        Run processing when user clicks "Apply" button.
        """
        """选择文件路径并加载影像"""
        file_path = qt.QFileDialog.getOpenFileName(None, "Select NIfTI File", "", "NIfTI Files (*.nii *.nii.gz)")
        print(file_path)
        self.save_score_path = os.path.dirname(file_path)
        self.save_res_path = file_path
        if file_path:
            self.loadImage(file_path)
            self.reset_score()
    
        
    def loadImage(self, file_path):
        """加载并显示影像"""
        try:            
            volume_node = slicer.util.loadVolume(file_path)
            if volume_node:
                displayNode = volume_node.GetDisplayNode()
                displayNode.AutoWindowLevelOff()
                # Set window/level for brain window (CT values)
                displayNode.SetWindow(60)
                displayNode.SetLevel(40)
                
                # Optionally, you can check if the changes were applied:
                print("Window:", displayNode.GetWindow())
                print("Level:", displayNode.GetLevel())

                volume_node.SetName(os.path.basename(file_path))  # 设置文件名为节点名称
                slicer.util.setSliceViewerLayers(background=volume_node)
                print(f"Volume {file_path} loaded successfully.")
                with open(f"{os.path.dirname(file_path)}/reports.json", "r") as f:
                    reports = json.load(f)
                self.origin_report[1] = reports["gt"].split("：")[-1]
                
                self.ui.textBrowser_2.setText("Method1: "+ reports["minimed"])
                self.ui.textBrowser_3.setText("Method2: "+ reports["gpt"])
                self.ui.textBrowser_4.setText("Method3:  " + reports["radfm"])
                self.ui.textBrowser_5.setText("Method4: " + reports["brainfound:"].split("：")[-1])               

            else:
                print(f"Failed to load volume: {file_path}")
            
            # 输出信息
            slicer.util.infoDisplay(f"Image loaded: {file_path}")
        
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to load image: {str(e)}")

    def reset_score(self)->None:
        tmp = {"general":0, "complete":0, "pos":0, "num":0, "cls":0, "bian":0, "midu":0, "xing":0, "normal":0}
        key = ["mini", "gpt4", "radfm", "bf"]
        res ={k:tmp for k in key}
        for key in res:
            for item in res[key]:
                attr = getattr(self.ui, f"{key}_{item}")
                attr.setText("-1")
        return

    def onApplySaveButton(self) -> None:
        """
        Run processing when user clicks "Apply" button.
        """
        """选择文件路径并加载影像"""
        tmp = {"general":0, "complete":0, "pos":0, "num":0, "cls":0, "bian":0, "midu":0, "xing":0, "normal":0}
        key = ["mini", "gpt4", "radfm", "bf"]
        res ={k:copy.deepcopy(tmp) for k in key}
        for key in res:
            for item in res[key]:
                attr = getattr(self.ui, f"{key}_{item}")
                if hasattr(attr, "currentText"):
                    res[key][item] = attr.currentText
                elif hasattr(attr, "toPlainText"):
                    res[key][item] = attr.toPlainText()
                else:
                    raise ValueError
        print(res, self.save_score_path)
        if self.save_score_path != None:
            with open(os.path.join(self.save_score_path, "human.json"), "w") as f:
                json.dump(res, f, indent=2, ensure_ascii=False)

#
# showImageReportsLogic
#

class showImageReportsLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self) -> None:
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return showImageReportsParameterNode(super().getParameterNode())

    def process(self,
                inputVolume: vtkMRMLScalarVolumeNode,
                outputVolume: vtkMRMLScalarVolumeNode,
                imageThreshold: float,
                invert: bool = False,
                showResult: bool = True) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget.
        :param inputVolume: volume to be thresholded
        :param outputVolume: thresholding result
        :param imageThreshold: values above/below this threshold will be set to 0
        :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
        :param showResult: show output volume in slice viewers
        """

        if not inputVolume or not outputVolume:
            raise ValueError("Input or output volume is invalid")

        import time
        startTime = time.time()
        logging.info('Processing started')

        # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
        cliParams = {
            'InputVolume': inputVolume.GetID(),
            'OutputVolume': outputVolume.GetID(),
            'ThresholdValue': imageThreshold,
            'ThresholdType': 'Above' if invert else 'Below'
        }
        cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
        # We don't need the CLI module node anymore, remove it to not clutter the scene with it
        slicer.mrmlScene.RemoveNode(cliNode)

        stopTime = time.time()
        logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')


#
# showImageReportsTest
#

class showImageReportsTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_showImageReports1()

    def test_showImageReports1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData
        registerSampleData()
        inputVolume = SampleData.downloadSample('showImageReports1')
        self.delayDisplay('Loaded test data set')

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = showImageReportsLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay('Test passed')
