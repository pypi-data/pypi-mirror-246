# Repository: https://gitlab.com/quantify-os/quantify-core
# Licensed according to the LICENCE file on the main branch
import matplotlib.pyplot as plt
import numpy as np

from quantify_core.analysis import base_analysis as ba
from quantify_core.analysis import fitting_models as fm
from quantify_core.visualization import mpl_plotting as qpl
from quantify_core.visualization.SI_utilities import format_value_string


# Custom analysis class for QubitSpectroscopy
class QubitSpectroscopyAnalysis(ba.BaseAnalysis):
    """
    Analysis for a qubit spectroscopy experiment.

    Fits a Lorentzian function to qubit spectroscopy
    data and finds the 0-1 transistion frequency.
    """

    # pylint: disable=invalid-name
    # pylint: disable=no-member

    def process_data(self) -> None:
        """Populate the :code:`.dataset_processed`."""
        # y0 = amplitude, no check for the amplitude unit as the name/label is
        # often different.

        self.dataset_processed["Magnitude"] = self.dataset.y0
        self.dataset_processed.Magnitude.attrs["name"] = "Magnitude"
        self.dataset_processed.Magnitude.attrs["units"] = self.dataset.y0.units
        self.dataset_processed.Magnitude.attrs["long_name"] = "Magnitude, $|S_{21}|$"

        self.dataset_processed["x0"] = self.dataset.x0
        self.dataset_processed = self.dataset_processed.set_coords("x0")
        # replace the default dim_0 with x0
        self.dataset_processed = self.dataset_processed.swap_dims({"dim_0": "x0"})

    def run_fitting(self) -> None:
        """Fit a Lorentzian function to the data."""
        mod = fm.LorentzianModel()

        magnitude = np.array(self.dataset_processed["Magnitude"])
        frequency = np.array(self.dataset_processed.x0)
        guess = mod.guess(magnitude, x=frequency)
        fit_result = mod.fit(magnitude, params=guess, x=frequency)

        self.fit_results.update({"Lorentzian_peak": fit_result})

    def analyze_fit_results(self) -> None:
        """Check fit success and populates :code:`.quantities_of_interest`."""
        fit_result = self.fit_results["Lorentzian_peak"]
        fit_warning = ba.wrap_text(ba.check_lmfit(fit_result))

        # If there is a problem with the fit, display an error message in the text box.
        # Otherwise, display the parameters as normal.
        if fit_warning is None:
            self.quantities_of_interest["fit_success"] = True

            text_msg = "Summary\n"
            text_msg += format_value_string(
                "Frequency 0-1",
                fit_result.params["x0"],
                unit="Hz",
                end_char="\n",
            )
            text_msg += format_value_string(
                "Peak width",
                fit_result.params["width"],
                unit="Hz",
                end_char="\n",
            )
        else:
            text_msg = ba.wrap_text(fit_warning)
            self.quantities_of_interest["fit_success"] = False

        self.quantities_of_interest["frequency_01"] = ba.lmfit_par_to_ufloat(
            fit_result.params["x0"]
        )
        self.quantities_of_interest["fit_msg"] = text_msg

    def create_figures(self) -> None:
        """Create qubit spectroscopy figure."""
        fig_id = "QubitSpectroscopyAnalysis"
        fig, ax = plt.subplots()
        self.figs_mpl[fig_id] = fig  # type: ignore
        self.axs_mpl[fig_id] = ax  # type: ignore

        self.dataset_processed.Magnitude.plot(ax=ax, marker=".", linestyle="")

        qpl.plot_fit(
            ax=ax,
            fit_res=self.fit_results["Lorentzian_peak"],
            plot_init=not self.quantities_of_interest["fit_success"],
            range_casting="real",
        )

        qpl.set_suptitle_from_dataset(fig, self.dataset, "S21")  # type: ignore

        fig.tight_layout()  # type: ignore
        # Add a textbox with the fit_message
        qpl.plot_textbox(ax, self.quantities_of_interest["fit_msg"])  # type: ignore


class ResonatorSpectroscopyAnalysis(ba.BaseAnalysis):
    """
    Analysis for a spectroscopy experiment of a hanger resonator.
    """

    def process_data(self):
        """
        Verifies that the data is measured as magnitude and phase and casts it to
        a dataset of complex valued transmission :math:`S_{21}`.
        """

        # y0 = amplitude, no check for the amplitude unit as the name/label is
        # often different.
        # y1 = phase in deg, this unit should always be correct
        assert self.dataset.y1.units == "deg"

        S21 = self.dataset.y0 * np.cos(
            np.deg2rad(self.dataset.y1)
        ) + 1j * self.dataset.y0 * np.sin(np.deg2rad(self.dataset.y1))
        self.dataset_processed["S21"] = S21
        self.dataset_processed.S21.attrs["name"] = "S21"
        self.dataset_processed.S21.attrs["units"] = self.dataset.y0.units
        self.dataset_processed.S21.attrs["long_name"] = "Transmission, $S_{21}$"

        self.dataset_processed["x0"] = self.dataset.x0
        self.dataset_processed = self.dataset_processed.set_coords("x0")
        # replace the default dim_0 with x0
        self.dataset_processed = self.dataset_processed.swap_dims({"dim_0": "x0"})

    def run_fitting(self):
        """
        Fits a :class:`~quantify_core.analysis.fitting_models.ResonatorModel` to the data.
        """

        model = fm.ResonatorModel()

        S21 = self.dataset_processed.S21.values
        frequency = self.dataset_processed.x0.values
        guess = model.guess(S21, f=frequency)

        fit_result = model.fit(S21, params=guess, f=frequency)

        self.fit_results.update({"hanger_func_complex_SI": fit_result})

    def analyze_fit_results(self):
        """
        Checks fit success and populates :code:`.quantities_of_interest`.
        """

        fit_result = self.fit_results["hanger_func_complex_SI"]
        fit_warning = ba.wrap_text(ba.check_lmfit(fit_result))

        if fit_warning is None:
            self.quantities_of_interest["fit_success"] = True
            text_msg = "Summary\n"
            text_msg += format_value_string(
                r"$Q_I$", fit_result.params["Qi"], unit="SI_PREFIX_ONLY", end_char="\n"
            )
            text_msg += format_value_string(
                r"$Q_C$", fit_result.params["Qc"], unit="SI_PREFIX_ONLY", end_char="\n"
            )
            text_msg += format_value_string(
                r"$f_{res}$", fit_result.params["fr"], unit="Hz"
            )
        else:
            text_msg = ba.wrap_text(fit_warning)
            self.quantities_of_interest["fit_success"] = False

        for parameter in ["Qi", "Qe", "Ql", "Qc", "fr"]:
            self.quantities_of_interest[parameter] = ba.lmfit_par_to_ufloat(
                fit_result.params[parameter]
            )
        self.quantities_of_interest["fit_msg"] = text_msg

    def create_figures(self):
        """
        Plots the measured and fitted transmission :math:`S_{21}` as the I and Q
        component vs frequency, the magnitude and phase vs frequency,
        and on the complex I,Q plane.
        """
        self._create_fig_s21_real_imag()
        self._create_fig_s21_magn_phase()
        self._create_fig_s21_complex()

    def _create_fig_s21_real_imag(self):
        fig_id = "S21-RealImag"
        fig, axs = plt.subplots(2, 1, sharex=True)
        self.figs_mpl[fig_id] = fig
        self.axs_mpl[fig_id + "_Re"] = axs[0]
        self.axs_mpl[fig_id + "_Im"] = axs[1]

        # Add a textbox with the fit_message
        qpl.plot_textbox(axs[0], self.quantities_of_interest["fit_msg"])

        self.dataset_processed.S21.real.plot(ax=axs[0], marker=".")
        self.dataset_processed.S21.imag.plot(ax=axs[1], marker=".")

        qpl.plot_fit(
            ax=axs[0],
            fit_res=self.fit_results["hanger_func_complex_SI"],
            plot_init=False,
            range_casting="real",
        )

        qpl.plot_fit(
            ax=axs[1],
            fit_res=self.fit_results["hanger_func_complex_SI"],
            plot_init=False,
            range_casting="imag",
        )

        qpl.set_ylabel(r"Re$(S_{21})$", self.dataset_processed.S21.units, axs[0])
        qpl.set_ylabel(r"Im$(S_{21})$", self.dataset_processed.S21.units, axs[1])
        axs[0].set_xlabel("")
        qpl.set_xlabel(
            self.dataset_processed.x0.long_name, self.dataset_processed.x0.units, axs[1]
        )

        qpl.set_suptitle_from_dataset(fig, self.dataset, "S21")

    def _create_fig_s21_magn_phase(self):
        fig_id = "S21-MagnPhase"
        fig, axs = plt.subplots(2, 1, sharex=True)
        self.figs_mpl[fig_id] = fig
        self.axs_mpl[fig_id + "_Magn"] = axs[0]
        self.axs_mpl[fig_id + "_Phase"] = axs[1]

        # Add a textbox with the fit_message
        qpl.plot_textbox(axs[0], self.quantities_of_interest["fit_msg"])

        axs[0].plot(
            self.dataset_processed.x0, np.abs(self.dataset_processed.S21), marker="."
        )
        axs[1].plot(
            self.dataset_processed.x0,
            np.angle(self.dataset_processed.S21, deg=True),
            marker=".",
        )

        qpl.plot_fit(
            ax=axs[0],
            fit_res=self.fit_results["hanger_func_complex_SI"],
            plot_init=False,
            range_casting="abs",
        )

        qpl.plot_fit(
            ax=axs[1],
            fit_res=self.fit_results["hanger_func_complex_SI"],
            plot_init=False,
            range_casting="angle",
        )

        qpl.set_ylabel(r"$|S_{21}|$", self.dataset_processed.S21.units, axs[0])
        qpl.set_ylabel(r"$\angle S_{21}$", "deg", axs[1])
        axs[0].set_xlabel("")
        qpl.set_xlabel(
            self.dataset_processed.x0.long_name, self.dataset_processed.x0.units, axs[1]
        )

        qpl.set_suptitle_from_dataset(fig, self.dataset, "S21")

    def _create_fig_s21_complex(self):
        fig_id = "S21-complex"
        fig, ax = plt.subplots()
        self.figs_mpl[fig_id] = fig
        self.axs_mpl[fig_id] = ax

        # Add a textbox with the fit_message
        qpl.plot_textbox(ax, self.quantities_of_interest["fit_msg"])

        ax.plot(
            self.dataset_processed.S21.real, self.dataset_processed.S21.imag, marker="."
        )

        qpl.plot_fit_complex_plane(
            ax=ax,
            fit_res=self.fit_results["hanger_func_complex_SI"],
            plot_init=False,
        )

        qpl.set_xlabel(r"Re$(S_{21})$", self.dataset_processed.S21.units, ax)
        qpl.set_ylabel(r"Im$(S_{21})$", self.dataset_processed.S21.units, ax)

        qpl.set_suptitle_from_dataset(fig, self.dataset, "S21")
