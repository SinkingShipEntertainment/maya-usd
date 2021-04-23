#!/usr/bin/env mayapy
#
# Copyright 2021 Autodesk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import fixturesUtils
import imageUtils
import mayaUtils
import usdUtils
import testUtils

from mayaUsd import lib as mayaUsdLib
from mayaUsd import ufe as mayaUsdUfe

from maya import cmds

import ufe

import os


class testVP2RenderDelegatePerInstanceInheritedData(imageUtils.ImageDiffingTestCase):
    """
    Tests imaging using the Viewport 2.0 render delegate when using per-instance
    inherited data on instances.
    """

    @classmethod
    def setUpClass(cls):
        # The test USD data is authored Z-up, so make sure Maya is configured
        # that way too.
        # cmds.upAxis(axis='z')

        inputPath = fixturesUtils.setUpClass(__file__,
            initializeStandalone=False, loadPlugin=False)

        cls._baselineDir = os.path.join(inputPath,
            'VP2RenderDelegatePerInstanceInheritedDataTest', 'baseline')

        cls._testDir = os.path.abspath('.')

    def assertSnapshotClose(self, imageName):
        baselineImage = os.path.join(self._baselineDir, imageName)
        snapshotImage = os.path.join(self._testDir, imageName)
        imageUtils.snapshot(snapshotImage, width=960, height=540)
        return self.assertImagesClose(baselineImage, snapshotImage)

    def _StartTest(self, testName):
        cmds.file(force=True, new=True)
        mayaUtils.loadPlugin("mayaUsdPlugin")
        self._testName = testName
        testFile = testUtils.getTestScene("instances", self._testName + ".usda")
        mayaUtils.createProxyFromFile(testFile)
        globalSelection = ufe.GlobalSelection.get()
        globalSelection.clear()
        self.assertSnapshotClose('%s_unselected.png' % self._testName)

    def testPerInstanceInheritedData(self):
        self._StartTest('perInstanceInheritedData')
        # do some tests to check that selection hi-lights works as expected
        mayaPathSegment = mayaUtils.createUfePathSegment('|stage|stageShape')

        ball_01PathSegment = usdUtils.createUfePathSegment('/root/group/ball_01')
        ball_01Path = ufe.Path([mayaPathSegment, ball_01PathSegment])
        ball_01Item = ufe.Hierarchy.createItem(ball_01Path)

        ball_02PathSegment = usdUtils.createUfePathSegment('/root/group/ball_02')
        ball_02Path = ufe.Path([mayaPathSegment, ball_02PathSegment])
        ball_02Item = ufe.Hierarchy.createItem(ball_02Path)

        ball_03PathSegment = usdUtils.createUfePathSegment('/root/group/ball_03')
        ball_03Path = ufe.Path([mayaPathSegment, ball_03PathSegment])
        ball_03Item = ufe.Hierarchy.createItem(ball_03Path)

        newSelection = ufe.Selection()
        globalSelection = ufe.GlobalSelection.get()

        newSelection.append(ball_01Item)
        globalSelection.replaceWith(newSelection)
        self.assertSnapshotClose('%s_select_ball_01.png' % self._testName)
        globalSelection.clear()
        newSelection.clear()

        newSelection.append(ball_02Item)
        globalSelection.replaceWith(newSelection)
        self.assertSnapshotClose('%s_select_ball_02.png' % self._testName)
        globalSelection.clear()
        newSelection.clear()

        newSelection.append(ball_01Item)
        newSelection.append(ball_02Item)
        newSelection.append(ball_03Item)
        globalSelection.replaceWith(newSelection)
        self.assertSnapshotClose('%s_select_ball_01_02_03.png' % self._testName)
        globalSelection.clear()
        newSelection.clear()
    
    def testPerInstanceInheritedDataPartialOverridePxrMtls(self):
        self._StartTest('inheritedDisplayColor_noPxrMtls')

    def testPerInstanceInheritedDataPartialOverride(self):
        self._StartTest('inheritedDisplayColor_pxrSurface')

    def testPerInstanceInheriedDataBasisCurves(self):
        self._StartTest('basisCurveInstance')
        cmds.select("|stage|stageShape,/instanced_2")
        self.assertSnapshotClose('%s_selected.png' % self._testName)



if __name__ == '__main__':
    fixturesUtils.runTests(globals())
