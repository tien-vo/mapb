""" Add plotting procedures to existing data class (not standalone) """


__all__ = ["PlotProcedures"]


from .spiral import reconstruct_footprint
import matplotlib.pyplot as plt
import astropy.constants as c
import astropy.units as u
import numpy as np
import datetime


_params = dict(direction="in", top=True, bottom=True, left=True, right=True)
_colors = ["r", "b", "g"]


def find_ts_plotables(l, sid):
    return [s for s in l if s.startswith(sid) and (not s.endswith("epoch"))]


def find_fp_plotables(l):
    return [s for s in l if s.endswith("footprint")]


def nearest_date(dates, date):
    return min(dates, key=lambda x: abs(x - date))


class PlotProcedures:

    def plot_time_series(self, sc, save=False):
        if sc not in self.sc:
            print(f"STEREO {sc}: Data not loaded.")
        else:
            time = self.data[f"st{sc.lower()}_epoch"]
            plotables = find_ts_plotables(self.data.keys(), f"st{sc.lower()}")
            panel_size = 2
            N_panels = len(plotables)

            fig, axes = plt.subplots(
                N_panels, 1, figsize=(12, panel_size * N_panels), sharex=True
            )
            fig.subplots_adjust(hspace=0.05)
            fig.suptitle(f"STEREO {sc}", y=0.9)
            for (ii, plotable) in enumerate(plotables):
                data = self.data[plotable]
                attrs = self.attrs[plotable]
                if len(data.shape) == 1:
                    axes[ii].plot(time, data, "-k")
                else:
                    Ndim = data.shape[1]
                    legends = attrs["legends"]
                    for jj in range(Ndim):
                        axes[ii].plot(time, data[:, jj],
                                      c=_colors[jj], label=legends[jj])

                    axes[ii].legend(loc=3, bbox_to_anchor=(1.0, 0.0),
                                    handlelength=0, frameon=False,
                                    labelcolor=_colors[:Ndim])
                unit = attrs["UNITS"] if attrs["UNITS"] != "Na" else "unitless"
                axes[ii].set_ylabel(f"{attrs['FIELDNAM']}\n({unit})")

            fig.align_ylabels(axes)
            for (ii, ax) in enumerate(axes):
                ax.tick_params(**_params)
                ax.set_xlim(time[0], time[-1])

        if save: fig.savefig(f"st{sc.lower()}_time_series.png")

    def plot_footprints(self, save=False):

        b = self.b

        plotables = find_fp_plotables(self.data.keys())
        if len(plotables) == 0:
            print("No footprint data loaded.")
        else:
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            fig.suptitle(
                f"Parker spiral footprints "
                f"(traced to $b$ = {(b / c.R_sun).decompose():.0f}) R_sun")
            for (ii, plotable) in enumerate(plotables):
                label = plotable.split("_")[0]
                data = self.data[plotable]
                lat = data[:, 0]
                lon = data[:, 1]
                ax.plot(lon, lat, color=_colors[ii], label=label.upper())

            ax.legend(
                handlelength=0, frameon=False,
                labelcolor=_colors[:len(plotables)]
            )
            ax.set_aspect("equal")
            ax.tick_params(**_params)
            ax.set_xlim(0, 360)
            ax.set_ylim(-30, 30)
            ax.set_xlabel("Longitude (deg)")
            ax.set_ylabel("Latitude (deg)")

        if save: fig.savefig("footprints.png")

    def plot_spirals(self, time=None, save=False):

        b = self.b

        plotables = find_fp_plotables(self.data.keys())
        if len(plotables) == 0:
            print("No footprint data loaded.")
        else:

            if time is None:
                it = 0
            else:
                tmp = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
                tmp = nearest_date(self.data["sta_epoch"], tmp)
                it = np.where(self.data["sta_epoch"] == tmp)[0][0]

            time = self.data["sta_epoch"][it]

            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
            fig.suptitle(f"{time}", y=0.95)
            for (ii, plotable) in enumerate(plotables):
                label = plotable.split("_")[0]
                fp = self.data[plotable][it, :]
                # Get other variables
                x, y, _ = self.data[f"{label}_HEEQ"][it, :]
                Vr = self.data[f"{label}_Vp"][it]

                r_arr = np.linspace(b, 1.1 * u.au, 1000)
                phi_arr = reconstruct_footprint(r_arr, fp, Vr, b=b)

                xs = r_arr * np.cos(fp[0]) * np.cos(phi_arr)
                ys = r_arr * np.cos(fp[0]) * np.sin(phi_arr)

                ax.plot(xs, ys, "--k")
                ax.scatter(x, y, color=_colors[ii], label=label.upper())

            ax.scatter(0, 0, color="y", s=70, label="Sun")
            ax.scatter(1, 0, color="k", s=70, label="Earth")
            ax.legend(
                handlelength=0, frameon=False,
                labelcolor=_colors[:len(plotables)] + ["y", "k"]
            )
            ax.set_aspect("equal")
            ax.tick_params(**_params)
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_xlabel("X HEEQ (AU)")
            ax.set_ylabel("Y HEEQ (AU)")

        if save: fig.savefig(f"spirals_{time}.png")

    def show(self):
        plt.show()

