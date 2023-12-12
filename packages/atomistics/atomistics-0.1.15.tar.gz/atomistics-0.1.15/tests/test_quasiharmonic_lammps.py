import os

from ase.build import bulk
from phonopy.units import VaspToTHz
import unittest

from atomistics.workflows import QuasiHarmonicWorkflow, optimize_positions_and_volume

try:
    from atomistics.calculators import (
        evaluate_with_lammps, get_potential_by_name
    )

    skip_lammps_test = False
except ImportError:
    skip_lammps_test = True


@unittest.skipIf(
    skip_lammps_test, "LAMMPS is not installed, so the LAMMPS tests are skipped."
)
class TestPhonons(unittest.TestCase):
    def test_calc_phonons(self):
        structure = bulk("Al", a=4.05, cubic=True)
        df_pot_selected = get_potential_by_name(
            potential_name='1999--Mishin-Y--Al--LAMMPS--ipr1',
            resource_path=os.path.join(os.path.dirname(__file__), "static", "lammps"),
        )
        task_dict = optimize_positions_and_volume(structure=structure)
        result_dict = evaluate_with_lammps(
            task_dict=task_dict,
            potential_dataframe=df_pot_selected,
        )
        workflow = QuasiHarmonicWorkflow(
            structure=result_dict["structure_with_optimized_positions_and_volume"],
            num_points=11,
            vol_range=0.05,
            interaction_range=10,
            factor=VaspToTHz,
            displacement=0.01,
            dos_mesh=20,
            primitive_matrix=None,
            number_of_snapshots=None,
        )
        task_dict = workflow.generate_structures()
        result_dict = evaluate_with_lammps(
            task_dict=task_dict,
            potential_dataframe=df_pot_selected,
        )
        eng_internal_dict, mesh_collect_dict, dos_collect_dict = workflow.analyse_structures(output_dict=result_dict)
        tp_collect_dict = workflow.get_thermal_properties(t_min=1, t_max=1500, t_step=50, temperatures=None)
        temperatures_qh_qm, volumes_qh_qm = workflow.get_thermal_expansion(
            output_dict=result_dict,
            temperatures=[100, 1000],
            quantum_mechanical=True
        )
        temperatures_qh_cl, volumes_qh_cl = workflow.get_thermal_expansion(
            output_dict=result_dict,
            temperatures=[100, 1000],
            quantum_mechanical=False
        )
        self.assertEqual(len(eng_internal_dict.keys()), 11)
        self.assertEqual(len(tp_collect_dict.keys()), 11)
        self.assertEqual(len(temperatures_qh_qm), 2)
        self.assertEqual(len(volumes_qh_qm), 2)
        self.assertTrue(volumes_qh_qm[0] < volumes_qh_qm[-1])
        self.assertEqual(len(temperatures_qh_cl), 2)
        self.assertEqual(len(volumes_qh_cl), 2)
        self.assertTrue(volumes_qh_cl[0] < volumes_qh_cl[-1])
