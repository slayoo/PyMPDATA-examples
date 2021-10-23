import numpy as np
from PyMPDATA import ScalarField, VectorField, Solver, Stepper
from PyMPDATA.boundary_conditions import Constant


class Simulation:
    def __init__(self, settings, options):
        bcs = tuple([Constant(0) for _ in settings.grid])

        advector = VectorField(
            data=settings.advector,
            halo=options.n_halo,
            boundary_conditions=bcs
        )

        advectee = ScalarField(
            data=np.asarray(settings.advectee, dtype=options.dtype),
            halo=options.n_halo,
            boundary_conditions=bcs
        )

        stepper = Stepper(options=options, grid=settings.grid)
        self.solver = Solver(stepper=stepper, advectee=advectee, advector=advector)

    def run(self, nt):
        _ = self.solver.advance(nt)
