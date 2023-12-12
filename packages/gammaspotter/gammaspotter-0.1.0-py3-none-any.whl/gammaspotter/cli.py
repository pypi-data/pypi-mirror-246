import click
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from rich.table import Table
from rich.console import Console
from datetime import datetime

from gammaspotter.process_data import ProcessData


@click.group()
def cmd_group():
    """A command line interface tool for gammaspotter."""
    pass


@cmd_group.command()
@click.option(
    "--no-cleaning",
    help="Disable the default removal of last few rows of data usually containing edge effect abnormalities.",
    is_flag=True,
)
@click.option(
    "--detect-peaks",
    help="Display the positions of the detected peaks in the spectrum.",
    is_flag=True,
)
@click.option(
    "--fit-peaks",
    help="Determine the positions of the peaks accurately by fitting a gaussian function to it.",
    is_flag=True,
)
@click.argument(
    "path", type=click.Path("rb", dir_okay=False, executable=False, path_type=Path)
)
@click.option(
    "-c",
    "--calibrate",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
    ),
)
def graph(
    path: click.Path,
    detect_peaks: bool,
    no_cleaning: bool,
    fit_peaks: bool,
    calibrate: bool,
):
    """A measurement in CSV displayed as an interactive matplotlib plot.

    Args:
        path (Path): location of the data file that should be displayed
        no_cleaning (bool): disable removal of edge effect
        detect_peaks (bool): indicate whether the peaks should be detected and displayed in the figure
        fit_peaks (bool): fit a gaussian function over the peaks to determine their positions more accurately
        calibrate (bool): indicate a path where calibration results are stored
    """
    path = Path(path)
    data = pd.read_csv(path)

    if calibrate:
        calibrate_results = pd.read_csv(calibrate, index_col=None)
        scaling = calibrate_results["scaling factor"][0]
        offset = calibrate_results["horizontal offset"][0]

        # apply calibration to first column: pulseheight
        data.iloc[:, 0] = data.iloc[:, 0] * scaling - offset

        x_label = "Energy [keV]"
    else:
        x_label = "Pulseheight [mV]"

    data_process = ProcessData(data=data)

    if not no_cleaning:
        data = data_process.remove_edge_effect()

    fig, ax = plt.subplots()

    if detect_peaks:
        peaks_df = data_process.find_gamma_peaks(width=[3, 7], prominence=300)

        if peaks_df.size > 0:
            peaks_df.plot(
                ax=ax,
                x="x_peaks",
                y="y_peaks",
                label="Detected peaks",
                kind="scatter",
                c="red",
                s=50,
                marker="x",
                zorder=1,
            )
        else:
            click.echo(
                "No peaks have been detected, please adjust your detection parameters if you think this is incorrect."
            )

    data.plot(
        ax=ax,
        x="pulseheight",
        y="counts_ch_A",
        label="Spectrum",
        legend=True,
        xlabel=x_label,
        ylabel="Counts",
        title=path.stem,
        zorder=0,
    )
    if fit_peaks:
        # energies = []

        width = 10
        if calibrate:
            width *= scaling

        fit_results = data_process.fit_peaks(domain_width=width)
        for result in fit_results:
            x_expectation_val = result.values["cen"]
            plt.axvline(x=x_expectation_val, c="grey", linestyle="dotted")
            # energies.append(x_expectation_val)

        # print(f"{energies=}")

    plt.show()


# get a list of available calibration isotopes before command is run
calibration_catalog = pd.read_csv("catalogs/common_calibration_sources.csv")
isotopes = list(set(calibration_catalog.iloc[:, 0]))


@cmd_group.command()
@click.argument("path", type=click.Path())
@click.argument("isotope", type=click.Choice(isotopes))
@click.option(
    "-s",
    "--save",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Provide a directory where the calibration data should be saved.",
)
def calibrate(path: click.Path, isotope: str, save: click.Path):
    data = pd.read_csv(path)
    data_process = ProcessData(data=data)

    known_energies = calibration_catalog[calibration_catalog["isotope"] == isotope]
    isotope_energies = [
        float(known_energies.iloc[:, 1].values[0]),
        float(known_energies.iloc[:, 2].values[0]),
    ]

    calibration_params = data_process.calibrate(known_energies=isotope_energies)

    table = Table(title=f"{isotope} Calibration Results")
    table.add_column("Scaling Factor")
    table.add_column("Energy Offset")
    scaling_str = f"{round(calibration_params[0], 4)} keV/mV"
    hoffset_str = f"{round(calibration_params[1], 4)} keV"
    table.add_row(scaling_str, hoffset_str)
    console = Console()
    console.print(table)

    if save:
        calibration_Series = pd.DataFrame(
            {
                "unix timestamp": [datetime.now()],
                "isotope": [isotope],
                "scaling factor": [calibration_params[0]],
                "horizontal offset": [calibration_params[1]],
            }
        )

        save = Path(save)
        path = save / f"{isotope}_calibration.csv"
        calibration_Series.to_csv(path, index=False)


if __name__ == "__main__":
    cmd_group()
