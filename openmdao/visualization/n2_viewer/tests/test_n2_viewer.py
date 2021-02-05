"""Unit Tests for n2_viewer"""
import unittest

import numpy as np

import openmdao.api as om
from openmdao.test_suite.components.paraboloid import Paraboloid
from openmdao.visualization.n2_viewer.n2_viewer import _get_viewer_data

class TestN2Viewer(unittest.TestCase):

    def test_root_case(self):
        prob = om.Problem()
        model = prob.model

        model.add_subsystem('p1', om.IndepVarComp('x', 0.0), promotes=['x'])
        model.add_subsystem('p2', om.IndepVarComp('y', 0.0), promotes=['y'])
        model.add_subsystem('comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])

        model.add_design_var('x', lower=0.0, upper=1.0)
        model.add_design_var('y', lower=0.0, upper=1.0)
        model.add_objective('f_xy')

        recorder = om.SqliteRecorder("cases.sql")
        prob.driver = om.DOEDriver(om.PlackettBurmanGenerator())
        prob.driver.add_recorder(recorder)
        # prob.model.add_recorder(recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        data_dict = _get_viewer_data("cases.sql",
                                     case_id='rank0:DOEDriver_PlackettBurman|3')

        vals = data_dict['tree']['children'][2]['children']
        x_val = vals[0]['value']
        y_val = vals[1]['value']
        f_xy_val = vals[2]['value']

        self.assertEqual(x_val, np.array([0.]))
        self.assertEqual(y_val, np.array([0.]))
        self.assertEqual(f_xy_val, np.array([27.]))

    def test_index_number(self):
        prob = om.Problem()
        model = prob.model

        model.add_subsystem('p1', om.IndepVarComp('x', 0.0), promotes=['x'])
        model.add_subsystem('p2', om.IndepVarComp('y', 0.0), promotes=['y'])
        model.add_subsystem('comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])

        model.add_design_var('x', lower=0.0, upper=1.0)
        model.add_design_var('y', lower=0.0, upper=1.0)
        model.add_objective('f_xy')

        recorder = om.SqliteRecorder("cases.sql")
        prob.driver = om.DOEDriver(om.PlackettBurmanGenerator())
        prob.driver.add_recorder(recorder)
        prob.model.add_recorder(recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        data_dict = _get_viewer_data("cases.sql", case_id=3)

        vals = data_dict['tree']['children'][2]['children']
        x_val = vals[0]['value']
        y_val = vals[1]['value']
        f_xy_val = vals[2]['value']

        self.assertEqual(x_val, np.array([0.]))
        self.assertEqual(y_val, np.array([0.]))
        self.assertEqual(f_xy_val, np.array([27.]))

    def test_invalid_case(self):
        prob = om.Problem()
        model = prob.model

        model.add_subsystem('p1', om.IndepVarComp('x', 0.0), promotes=['x'])
        model.add_subsystem('p2', om.IndepVarComp('y', 0.0), promotes=['y'])
        model.add_subsystem('comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])

        model.add_design_var('x', lower=0.0, upper=1.0)
        model.add_design_var('y', lower=0.0, upper=1.0)
        model.add_objective('f_xy')

        recorder = om.SqliteRecorder("cases.sql")
        prob.driver = om.DOEDriver(om.PlackettBurmanGenerator())
        prob.driver.add_recorder(recorder)
        prob.model.add_recorder(recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()



        with self.assertRaises(ValueError) as cm:
            _get_viewer_data("cases.sql", case_id='rank0:DOEDriver_PlackettBurman|3|root')

        msg = ("case_id is not a driver case. Find valid case_id with "
               "om.CaseReader('cases.sql').list_cases()")
        self.assertEqual(str(cm.exception), msg)