# Copyright 2018 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Simple OpenHTF test which launches the web GUI client."""

import openhtf as htf
from openhtf.util import conf
from openhtf.util import validators

from openhtf.output.servers import station_server
from openhtf.output.web_gui import web_launcher
from openhtf.plugs import user_input


@htf.measures(htf.Measurement('hello_world_measurement'))
def hello_world(test):
  test.logger.info('Hello World!')
  test.measurements.hello_world_measurement = 'Hello Again!'

@htf.measures('inline_kwargs', docstring='This measurement is declared inline!',
              units=htf.units.HERTZ, validators=[validators.in_range(0, 10)])
@htf.measures('another_inline', docstring='Because why not?')
def inline_phase(test):
  # This measurement will have an outcome of FAIL, because the set value of 15
  # will not pass the 0 <= x <= 10 validator.
  test.measurements.inline_kwargs = 15
  test.measurements.another_inline = 'This one is unvalidated.'

  # Let's log a message so the operator knows the test should fail.
  test.logger.info('Set inline_kwargs to a failing value, test should FAIL!')

@htf.measures('first_measurement', 'second_measurement')
@htf.measures(htf.Measurement('third'), htf.Measurement('fourth'))
def lots_of_measurements(test):
  test.measurements.first_measurement = 'First!'
  # Measurements can also be access via indexing rather than attributes.
  test.measurements['second_measurement'] = 'Second :('
  # This can be handy for iterating over measurements.
  for measurement in ('third', 'fourth'):
    test.measurements[measurement] = measurement + ' is the best!'

def get_test():
    return htf.Test(hello_world,inline_phase,lots_of_measurements)

if __name__ == '__main__':
  conf.load(station_server_port='4444')
  with station_server.StationServer() as server:
    for i in range(5):
      test = get_test()
      test.add_output_callbacks(server.publish_final_state)
      test.execute(test_start=user_input.prompt_for_test_start())
