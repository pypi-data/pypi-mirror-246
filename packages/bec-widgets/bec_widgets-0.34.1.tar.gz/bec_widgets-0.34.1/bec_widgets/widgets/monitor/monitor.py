# pylint: disable = no-name-in-module,
import time

import pyqtgraph as pg
from bec_lib import MessageEndpoints
from pydantic import ValidationError
from pyqtgraph import mkBrush, mkPen
from qtpy import QtCore
from qtpy.QtCore import Signal as pyqtSignal
from qtpy.QtCore import Slot as pyqtSlot
from qtpy.QtWidgets import QApplication, QMessageBox

from bec_widgets.utils import Colors, Crosshair
from bec_widgets.utils.yaml_dialog import load_yaml
from bec_widgets.validation import MonitorConfigValidator
from bec_widgets.utils.bec_dispatcher import bec_dispatcher

# just for demonstration purposes if script run directly
CONFIG_SCAN_MODE = {
    "plot_settings": {
        "background_color": "white",
        "num_columns": 3,
        "colormap": "plasma",
        "scan_types": True,
    },
    "plot_data": {
        "grid_scan": [
            {
                "plot_name": "Grid plot 1",
                "x": {"label": "Motor X", "signals": [{"name": "samx", "entry": "samx"}]},
                "y": {
                    "label": "BPM",
                    "signals": [
                        {"name": "gauss_bpm", "entry": "gauss_bpm"},
                        {"name": "gauss_adc1", "entry": "gauss_adc1"},
                    ],
                },
            },
            {
                "plot_name": "Grid plot 2",
                "x": {"label": "Motor X", "signals": [{"name": "samx", "entry": "samx"}]},
                "y": {
                    "label": "BPM",
                    "signals": [
                        {"name": "gauss_bpm", "entry": "gauss_bpm"},
                        {"name": "gauss_adc1", "entry": "gauss_adc1"},
                    ],
                },
            },
            {
                "plot_name": "Grid plot 3",
                "x": {"label": "Motor Y", "signals": [{"name": "samx", "entry": "samx"}]},
                "y": {"label": "BPM", "signals": [{"name": "gauss_bpm", "entry": "gauss_bpm"}]},
            },
            {
                "plot_name": "Grid plot 4",
                "x": {"label": "Motor Y", "signals": [{"name": "samx", "entry": "samx"}]},
                "y": {"label": "BPM", "signals": [{"name": "gauss_adc3", "entry": "gauss_adc3"}]},
            },
        ],
        "line_scan": [
            {
                "plot_name": "BPM plot",
                "x": {"label": "Motor X", "signals": [{"name": "samx", "entry": "samx"}]},
                "y": {
                    "label": "BPM",
                    "signals": [
                        {"name": "gauss_bpm", "entry": "gauss_bpm"},
                        {"name": "gauss_adc1"},
                        {"name": "gauss_adc2", "entry": "gauss_adc2"},
                    ],
                },
            },
            {
                "plot_name": "Multi",
                "x": {"label": "Motor X", "signals": [{"name": "samx", "entry": "samx"}]},
                "y": {
                    "label": "Multi",
                    "signals": [
                        {"name": "gauss_bpm", "entry": "gauss_bpm"},
                        {"name": "samx", "entry": "samx"},
                    ],
                },
            },
        ],
    },
}

CONFIG_SIMPLE = {
    "plot_settings": {
        "background_color": "black",
        "num_columns": 2,
        "colormap": "plasma",
        "scan_types": False,
    },
    "plot_data": [
        {
            "plot_name": "BPM4i plots vs samx",
            "x": {
                "label": "Motor Y",
                # "signals": [{"name": "samx", "entry": "samx"}],
                "signals": [{"name": "samy"}],
            },
            "y": {"label": "bpm4i", "signals": [{"name": "bpm4i", "entry": "bpm4i"}]},
        },
        {
            "plot_name": "Gauss plots vs samx",
            "x": {"label": "Motor X", "signals": [{"name": "samx", "entry": "samx"}]},
            "y": {
                "label": "Gauss",
                # "signals": [{"name": "gauss_bpm", "entry": "gauss_bpm"}],
                "signals": [{"name": "gauss_bpm"}, {"name": "samy", "entry": "samy"}],
            },
        },
    ],
}

CONFIG_NO_ENTRY = {
    "plot_settings": {
        "background_color": "white",
        "num_columns": 5,
        "colormap": "plasma",
        "scan_types": False,
    },
    "plot_data": [
        {
            "plot_name": "BPM4i plots vs samx",
            "x": {"label": "Motor Y", "signals": [{"name": "samx"}]},
            "y": {"label": "bpm4i", "signals": [{"name": "bpm4i"}]},
        },
        {
            "plot_name": "Gauss plots vs samx",
            "x": {"label": "Motor X", "signals": [{"name": "samx"}]},
            "y": {"label": "Gauss", "signals": [{"name": "gauss_bpm"}, {"name": "gauss_adc1"}]},
        },
    ],
}

CONFIG_WRONG = {
    "plot_settings": {
        "background_color": "white",
        "num_columns": 5,
        "colormap": "plasma",
        "scan_types": False,
    },
    "plot_data": [
        {
            "plot_name": "BPM4i plots vs samx",
            "x": {"label": "Motor Y", "signals": [{"name": "samx"}]},
            "y": {"label": "bpm4i", "signals": [{"name": "bpm4i"}]},
        },
        {
            "plot_name": "Gauss plots vs samx",
            "x": {"label": "Motor X", "signals": [{"name": "samx"}]},
            "y": {
                "label": "Gauss",
                "signals": [
                    {"name": "gauss_bpm"},
                    {"name": "non_exist1"},
                    {"name": "non_exist2"},
                    {"name": "gauss_bpm", "entry": "samx"},
                ],
            },
        },
    ],
}

test_config = {
    "plot_settings": {
        "background_color": "white",
        "axis_width": 2,
        "num_columns": 5,
        "colormap": "plasma",
        "scan_types": False,
    },
    "plot_data": [
        {
            "plot_name": "BPM4i plots vs samx",
            "x": {"label": "Motor Y", "signals": [{"name": "samx"}]},
            "y": {"label": "bpm4i", "signals": [{"name": "bpm4i"}]},
        }
    ],
}


class BECMonitor(pg.GraphicsLayoutWidget):
    update_signal = pyqtSignal()

    def __init__(
        self,
        parent=None,
        client=None,
        config: dict = None,
        enable_crosshair: bool = True,
        gui_id=None,
    ):
        super(BECMonitor, self).__init__(parent=parent)

        # Client and device manager from BEC
        self.plot_data = None
        self.client = bec_dispatcher.client if client is None else client
        self.dev = self.client.device_manager.devices
        self.queue = self.client.queue

        self.validator = MonitorConfigValidator(self.dev)
        self.gui_id = gui_id

        if self.gui_id is None:
            self.gui_id = self.__class__.__name__ + str(time.time())  # TODO still in discussion

        # Connect slots dispatcher
        bec_dispatcher.connect_slot(self.on_scan_segment, MessageEndpoints.scan_segment())
        bec_dispatcher.connect_slot(self.on_config_update, MessageEndpoints.gui_config(self.gui_id))
        bec_dispatcher.connect_slot(
            self.on_instruction, MessageEndpoints.gui_instructions(self.gui_id)
        )

        # Current configuration
        self.config = config

        # Enable crosshair
        self.enable_crosshair = enable_crosshair

        # Displayed Data
        self.data = {}

        self.crosshairs = None
        self.plots = None
        self.curves_data = None
        self.grid_coordinates = None
        self.scanID = None

        # TODO make colors accessible to users
        self.user_colors = {}  # key: (plot_name, y_name, y_entry), value: color

        # Connect the update signal to the update plot method #TODO enable when update is fixed
        self.proxy_update_plot = pg.SignalProxy(
            self.update_signal, rateLimit=25, slot=self.update_plot
        )

        # Init UI
        if self.config is None:
            print("No initial config found for BECDeviceMonitor")
        else:
            self.on_config_update(self.config)

    def _init_config(self):
        """
        Initializes or update the configuration settings for the PlotApp.
        """

        # Separate configs
        self.plot_settings = self.config.get("plot_settings", {})
        self.plot_data_config = self.config.get("plot_data", {})
        self.scan_types = self.plot_settings.get("scan_types", False)

        if self.scan_types is False:  # Device tracking mode
            self.plot_data = self.plot_data_config  # TODO logic has to be improved
        else:  # without incoming data setup the first configuration to the first scan type sorted alphabetically by name
            self.plot_data = self.plot_data_config[min(list(self.plot_data_config.keys()))]

        # Initialize the UI
        self._init_ui(self.plot_settings["num_columns"])

    def _init_ui(self, num_columns: int = 3) -> None:
        """
        Initialize the UI components, create plots and store their grid positions.

        Args:
            num_columns (int): Number of columns to wrap the layout.

        This method initializes a dictionary `self.plots` to store the plot objects
        along with their corresponding x and y signal names. It dynamically arranges
        the plots in a grid layout based on the given number of columns and dynamically
        stretches the last plots to fit the remaining space.
        """
        self.clear()
        self.plots = {}
        self.grid_coordinates = []

        num_plots = len(self.plot_data)

        # Check if num_columns exceeds the number of plots
        if num_columns >= num_plots:
            num_columns = num_plots
            self.plot_settings["num_columns"] = num_columns  # Update the settings
            print(
                "Warning: num_columns in the YAML file was greater than the number of plots."
                f" Resetting num_columns to number of plots:{num_columns}."
            )
        else:
            self.plot_settings["num_columns"] = num_columns  # Update the settings

        num_rows = num_plots // num_columns
        last_row_cols = num_plots % num_columns
        remaining_space = num_columns - last_row_cols

        for i, plot_config in enumerate(self.plot_data):
            row, col = i // num_columns, i % num_columns
            colspan = 1

            if row == num_rows and remaining_space > 0:
                if last_row_cols == 1:
                    colspan = num_columns
                else:
                    colspan = remaining_space // last_row_cols + 1
                    remaining_space -= colspan - 1
                    last_row_cols -= 1

            plot_name = plot_config.get("plot_name", "")
            x_label = plot_config["x"].get("label", "")
            y_label = plot_config["y"].get("label", "")

            plot = self.addPlot(row=row, col=col, colspan=colspan, title=plot_name)
            plot.setLabel("bottom", x_label)
            plot.setLabel("left", y_label)
            plot.addLegend()
            self._set_plot_colors(plot, self.plot_settings)

            self.plots[plot_name] = plot
            self.grid_coordinates.append((row, col))

        self.init_curves()

    def _set_plot_colors(self, plot: pg.PlotItem, plot_settings: dict) -> None:
        """
        Set the plot colors based on the plot config.

        Args:
            plot (pg.PlotItem): Plot object to set the colors.
            plot_settings (dict): Plot settings dictionary.
        """
        if plot_settings.get("show_grid", False):
            plot.showGrid(x=True, y=True, alpha=0.5)
        pen_width = plot_settings.get("axis_width")
        color = plot_settings.get("axis_color")
        if color is None:
            if plot_settings["background_color"].lower() == "black":
                color = "w"
                self.setBackground("k")
            elif plot_settings["background_color"].lower() == "white":
                color = "k"
                self.setBackground("w")
            else:
                raise ValueError(
                    f"Invalid background color {plot_settings['background_color']}. Allowed values"
                    " are 'white' or 'black'."
                )
        print(plot_settings)
        pen = pg.mkPen(color=color, width=pen_width)
        x_axis = plot.getAxis("bottom")  # 'bottom' corresponds to the x-axis
        x_axis.setPen(pen)
        x_axis.setTextPen(pen)
        x_axis.setTickPen(pen)

        y_axis = plot.getAxis("left")  # 'left' corresponds to the y-axis
        y_axis.setPen(pen)
        y_axis.setTextPen(pen)
        y_axis.setTickPen(pen)

    def init_curves(self) -> None:
        """
        Initialize curve data and properties, and update table row labels.

        This method initializes a nested dictionary `self.curves_data` to store
        the curve objects for each x and y signal pair. It also updates the row labels
        in `self.tableWidget_crosshair` to include the grid position for each y-value.
        """
        self.curves_data = {}
        row_labels = []

        for idx, plot_config in enumerate(self.plot_data):
            plot_name = plot_config.get("plot_name", "")
            plot = self.plots[plot_name]
            plot.clear()

            y_configs = plot_config["y"]["signals"]
            colors_ys = Colors.golden_angle_color(
                colormap=self.plot_settings["colormap"], num=len(y_configs)
            )

            curve_list = []
            for i, (y_config, color) in enumerate(zip(y_configs, colors_ys)):
                y_name = y_config["name"]
                y_entry = y_config["entry"]

                user_color = self.user_colors.get((plot_name, y_name, y_entry), None)
                color_to_use = user_color if user_color else color

                pen_curve = mkPen(color=color_to_use, width=2, style=QtCore.Qt.DashLine)
                brush_curve = mkBrush(color=color_to_use)

                curve_data = pg.PlotDataItem(
                    symbolSize=5,
                    symbolBrush=brush_curve,
                    pen=pen_curve,
                    skipFiniteCheck=True,
                    name=f"{y_name} ({y_entry})",
                )

                curve_list.append((y_name, y_entry, curve_data))
                plot.addItem(curve_data)
                row_labels.append(f"{y_name} ({y_entry}) - {plot_name}")

            self.curves_data[plot_name] = curve_list

        # Hook Crosshair
        if self.enable_crosshair == True:
            self.hook_crosshair()

    def hook_crosshair(self) -> None:
        """Hook the crosshair to all plots."""
        # TODO can be extended to hook crosshair signal for mouse move/clicked
        self.crosshairs = {}
        for plot_name, plot in self.plots.items():
            crosshair = Crosshair(plot, precision=3)
            self.crosshairs[plot_name] = crosshair

    def update_plot(self) -> None:
        """Update the plot data based on the stored data dictionary."""
        for plot_name, curve_list in self.curves_data.items():
            for y_name, y_entry, curve in curve_list:
                x_config = next(
                    (pc["x"] for pc in self.plot_data if pc.get("plot_name") == plot_name), {}
                )
                x_signal_config = x_config["signals"][0]
                x_name = x_signal_config.get("name", "")
                x_entry = x_signal_config.get("entry", x_name)

                key = (x_name, x_entry, y_name, y_entry)
                data_x = self.data.get(key, {}).get("x", [])
                data_y = self.data.get(key, {}).get("y", [])

                curve.setData(data_x, data_y)

    def get_config(self):
        """Return the current configuration settings."""
        return self.config

    def show_config_dialog(self):
        """Show the configuration dialog."""
        from .config_dialog import ConfigDialog

        dialog = ConfigDialog(default_config=self.config)
        dialog.config_updated.connect(self.on_config_update)
        dialog.show()

    def update_client(self, client) -> None:
        """Update the client and device manager from BEC.
        Args:
            client: BEC client
        """
        self.client = client
        self.dev = self.client.device_manager.devices

    @pyqtSlot(dict)
    def on_instruction(self, msg_content: dict) -> None:
        """
        Handle instructions sent to the GUI.
        Possible actions are:
            - clear: Clear the plots
            - close: Close the GUI

        Args:
            msg_content (dict): Message content with the instruction and parameters.
        """
        action = msg_content.get("action", None)
        parameters = msg_content.get("parameters", None)

        if action == "clear":
            self.flush()
        elif action == "close":
            self.close()
        else:
            print(f"Unknown instruction received: {msg_content}")

    @pyqtSlot(dict)
    def on_config_update(self, config: dict) -> None:
        """
        Validate and update the configuration settings for the PlotApp.
        Args:
            config(dict): Configuration settings
        """

        try:
            validated_config = self.validator.validate_monitor_config(config)
            self.config = validated_config.model_dump()
            self._init_config()
        except ValidationError as e:
            error_str = str(e)
            formatted_error_message = BECMonitor.format_validation_error(error_str)

            # Display the formatted error message in a popup
            QMessageBox.critical(self, "Configuration Error", formatted_error_message)

    @staticmethod
    def format_validation_error(error_str: str) -> str:
        """
        Format the validation error string to be displayed in a popup.
        Args:
            error_str(str): Error string from the validation error.
        """
        error_lines = error_str.split("\n")
        # The first line contains the number of errors.
        error_header = f"<p><b>{error_lines[0]}</b></p><hr>"

        formatted_error_message = error_header
        # Skip the first line as it's the header.
        error_details = error_lines[1:]

        # Iterate through pairs of lines (each error's two lines).
        for i in range(0, len(error_details), 2):
            location = error_details[i]
            message = error_details[i + 1] if i + 1 < len(error_details) else ""

            formatted_error_message += f"<p><b>{location}</b><br>{message}</p><hr>"

        return formatted_error_message

    def flush(self) -> None:
        """Flush the data dictionary."""
        self.data = {}
        self.init_curves()

    @pyqtSlot(dict, dict)
    def on_scan_segment(self, msg, metadata):
        """
        Handle new scan segments and saves data to a dictionary. Linked through bec_dispatcher.

        Args:
            msg (dict): Message received with scan data.
            metadata (dict): Metadata of the scan.
        """
        # TODO for scan mode, if there are same names for different plots, the data are assigned multiple times
        current_scanID = msg.get("scanID", None)
        if current_scanID is None:
            return

        if current_scanID != self.scanID:
            if self.scan_types is False:
                self.plot_data = self.plot_data_config
            elif self.scan_types is True:
                current_name = metadata.get("scan_name")
                if current_name is None:
                    raise ValueError(
                        f"Scan name not found in metadata. Please check the scan_name in the YAML"
                        f" config or in bec configuration."
                    )
                self.plot_data = self.plot_data_config.get(current_name, [])
                if self.plot_data == []:
                    raise ValueError(
                        f"Scan name {current_name} not found in the YAML config. Please check the scan_name in the "
                        f"YAML config or in bec configuration."
                    )

                # Init UI
                self._init_ui(self.plot_settings["num_columns"])

            self.scanID = current_scanID
            self.flush()

        for plot_config in self.plot_data:
            x_config = plot_config["x"]
            x_signal_config = x_config["signals"][0]  # There is exactly 1 config for x signals

            x_name = x_signal_config.get("name", "")
            x_entry = x_signal_config.get("entry", [])

            y_configs = plot_config["y"]["signals"]
            for y_config in y_configs:
                y_name = y_config.get("name", "")
                y_entry = y_config.get("entry", [])

                key = (x_name, x_entry, y_name, y_entry)

                data_x = msg["data"].get(x_name, {}).get(x_entry, {}).get("value", None)
                data_y = msg["data"].get(y_name, {}).get(y_entry, {}).get("value", None)

                if data_x is not None:
                    self.data.setdefault(key, {}).setdefault("x", []).append(data_x)

                if data_y is not None:
                    self.data.setdefault(key, {}).setdefault("y", []).append(data_y)

        self.update_signal.emit()


if __name__ == "__main__":  # pragma: no cover
    import argparse
    import json
    import sys

    from bec_widgets.utils.bec_dispatcher import bec_dispatcher

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", help="Path to the config file.")
    parser.add_argument("--config", help="Path to the config file.")
    parser.add_argument("--id", help="GUI ID.")
    args = parser.parse_args()

    if args.config is not None:
        # Load config from file
        config = json.loads(args.config)
    elif args.config_file is not None:
        # Load config from file
        config = load_yaml(args.config_file)
    else:
        config = test_config

    client = bec_dispatcher.client
    client.start()
    app = QApplication(sys.argv)
    monitor = BECMonitor(config=config, gui_id=args.id)
    monitor.show()
    sys.exit(app.exec())
