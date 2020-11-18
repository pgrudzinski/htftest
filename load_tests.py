from importlib import import_module
from inspect import getfile
import logging
from pathlib import Path
from pkgutil import iter_modules

import openhtf as htf
from openhtf.output.servers import station_server
from openhtf.plugs import user_input
from openhtf.util import conf


@htf.plug(prompt=user_input.UserInput)
@htf.measures(htf.Measurement('next_test'))
def next_test(test,prompt):
    test.measurements.next_test = prompt.prompt('Select next test',text_input=True)

def gather_tests():
    test_scripts = import_module('test_scripts')
    tests_path = Path(test_scripts.__path__[0])
    test_modules = {}
    for _, name, ispkg in iter_modules([tests_path]):
        if not ispkg:
            try:
                test_module = import_module('.'.join(('test_scripts',name)))
                get_test = test_module.get_test
            except Exception:
                logging.exception('Error loading test %s. Skipping.', name)
                continue
            test_modules[name] = get_test
    return test_modules

class GetMeasurement:
    def __init__(self, measurement_name):
        self.measurement_name = measurement_name
        self.measurement = None

    def __call__(self, record):
        for phase in record.phases:
            if measurement_name in measurments.keys():
                self.measurement = phase.measurements[measurement_name].measured_value.stored_value
                break


def get_next_test():
    test = htf.Test(next_test,
                    test_name='Select Test',
                    test_description='Choose one of available tests from the list',
                    test_version='0.1.0')
    next_test_callback = GetMeasurement('next_test')
    test.add_output_callbacks(next_test_callback)
    test.execute()
    return next_test_callback.measurement


def main():
    conf.load(station_server_port='4444')
    with station_server.StationServer() as server:
        while True:
            tests = gather_tests()
            next_test = get_next_test()
            test = tests[next_test]
            #test.add_output_callbacks(publish_to_db)
            test.add_output_callbacks(server.publish_final_state)
            test.execute(test_start=user_input.prompt_for_test_start())

if __name__ == '__main__':
    main()


