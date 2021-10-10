import numpy as np
from PyMPDATA.boundary_conditions import Constant
from PyMPDATA import ScalarField, VectorField, Solver, Stepper


class Simulation:
    def __init__(self, settings):
        self.settings = settings
        s = settings

        halo = settings.options.n_halo
        grid = (s.nx, s.ny)
        bcs = [Constant(value=0)] * len(grid)

        self.advector = VectorField((
            np.zeros((s.nx + 1, s.ny)),
            np.zeros((s.nx, s.ny + 1))
        ), halo, bcs)

        A = 1 / s.lx0 / s.ly0
        xi, yi = np.indices(grid, dtype=float)
        xi += .5 - s.nx // 2
        yi += .5 - s.ny // 2
        x = xi * s.dx
        y = yi * s.dy
        h0 = A * (1 - (x / s.lx0) ** 2 - (y / s.ly0) ** 2)
        h0 = np.where(h0 > 0, h0, 0)

        advectees = {
            'h': ScalarField(h0, halo, bcs),
            'uh': ScalarField(np.zeros(grid), halo, bcs),
            'vh': ScalarField(np.zeros(grid), halo, bcs)
        }

        stepper = Stepper(options=s.options, grid=grid)
        self.solvers = {
            k: Solver(stepper, advectees[k], self.advector)
            for k in advectees
        }

    @staticmethod
    def interpolate(psi, axis):
        idx = (
            (slice(None, -1), slice(None, None)),
            (slice(None, None), slice(None, -1))
        )
        return np.diff(psi, axis=axis) / 2 + psi[idx[axis]]

    def run(self):
        s = self.settings
        grid_step = (s.dx, s.dy)
        idx = (
            (slice(1, -1), slice(None, None)),
            (slice(None, None), slice(1, -1))
        )
        output = []
        for it in range(s.nt + 1):
            if it != 0:
                h = self.solvers['h'].advectee.get()
                for xy, k in enumerate(('uh', 'vh')):
                    # TODO #273: extrapolate in time
                    self.advector.get_component(xy)[idx[xy]] = self.interpolate(
                        np.where(h > s.eps, np.divide(
                            self.solvers[k].advectee.get(),
                            h,
                            where=h > s.eps
                        ), 0), axis=xy
                    ) * s.dt / grid_step[xy]
                self.solvers['h'].advance(1)
                assert h.ctypes.data == self.solvers['h'].advectee.get().ctypes.data
                for xy, k in enumerate(('uh', 'vh')):
                    psi = self.solvers[k].advectee.get()
                    psi[:] -= s.dt / 2 * h * np.gradient(h, grid_step[xy], axis=xy)
                    self.solvers[k].advance(1)
                    psi[:] -= s.dt / 2 * h * np.gradient(h, grid_step[xy], axis=xy)
            if it % s.outfreq == 0:
                output.append({
                    k: self.solvers[k].advectee.get().copy()
                    for k in self.solvers.keys()
                })
        return output