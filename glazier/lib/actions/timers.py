# Lint as: python3
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

"""Actions to set imaging timers."""

import logging

from glazier.lib import constants
from glazier.lib import errors
from glazier.lib import registry
from glazier.lib.actions.base import BaseAction


class SetTimer(BaseAction):
  """Create an imaging timer."""

  def Run(self):
    timer = str(self._args[0])
    key_path = r'{0}\{1}'.format(constants.REG_ROOT, 'Timers')

    self._build_info.TimerSet(timer)
    value_name = 'TIMER_' + timer
    value_data = str(self._build_info.TimerGet(timer))
    try:
      registry.set_value(value_name, value_data, 'HKLM', key_path, log=False)
      logging.info('Set image timer: %s (%s)', timer, value_data)
    except errors.GlazierError as e:
      raise errors.GRegSetError(str(e))

  def Validate(self):
    self._ListOfStringsValidator(self._args)
