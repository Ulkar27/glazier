# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for glazier.lib.actions.tpm."""

from absl.testing import absltest
from glazier.lib.actions import tpm
import mock


class TpmTest(absltest.TestCase):

  @mock.patch.object(tpm.bitlocker, 'Bitlocker', autospec=True)
  def testBitlockerEnable(self, bitlocker):
    b = tpm.BitlockerEnable(['ps_tpm'], None)
    b.Run()
    bitlocker.assert_called_with('ps_tpm')
    self.assertTrue(bitlocker.return_value.Enable.called)
    bitlocker.return_value.Enable.side_effect = tpm.bitlocker.BitlockerError
    self.assertRaises(tpm.ActionError, b.Run)

  def testBitlockerEnableValidate(self):
    b = tpm.BitlockerEnable(30, None)
    self.assertRaises(tpm.ValidationError, b.Validate)
    b = tpm.BitlockerEnable([], None)
    self.assertRaises(tpm.ValidationError, b.Validate)
    b = tpm.BitlockerEnable(['invalid'], None)
    self.assertRaises(tpm.ValidationError, b.Validate)
    b = tpm.BitlockerEnable(['ps_tpm', 'ps_tpm'], None)
    self.assertRaises(tpm.ValidationError, b.Validate)
    b = tpm.BitlockerEnable(['ps_tpm'], None)
    b.Validate()


if __name__ == '__main__':
  absltest.main()
