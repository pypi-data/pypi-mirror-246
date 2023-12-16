from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QToolBar,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QStackedLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6 import QtWebEngineWidgets

from synapse_selector.gui.settingswindow import SettingsWindow
from synapse_selector.utils.trace_data import SynapseResponseData
from synapse_selector.utils.threshold import compute_threshold
from synapse_selector.utils.plot import trace_plot
from synapse_selector.detection.model_wraper import torch_model
from synapse_selector.detection.peak_detection import peak_detection_scipy

import os

file_path = os.path.dirname(__file__)
asset_path = '/'.join(file_path.split('/')[0:-1]) + '/assets'


class MainWindow(QMainWindow):
    def __init__(self, settings):
        super(MainWindow, self).__init__()
        # --- settings ---
        self.settings = settings

        # --- variables ---
        self.directory = None
        self.synapse_response = None

        self.model = torch_model()
        # load weights for CNN
        if self.settings.config["peak_detection_type"] == "ML-based":
            self.model.load_weights(self.settings.config["model_path"])

        stim_frames = self.settings.config['stim_frames']
        self.stim_frames = sorted([int(frame) for frame in stim_frames.split(",")]) if len(stim_frames) > 0 else []

        # --- function calls ---
        self.setup_gui()

    # --- helper functions ---

    def setup_gui(self):
        self.setWindowTitle("Synapse Selector")

        # toolbar
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        # status bar
        self.setStatusBar(QStatusBar(self))

        # main 'tab'
        main_wrapper_widget = QWidget()
        self.main_layout = QVBoxLayout()
        main_wrapper_widget.setLayout(self.main_layout)

        # settings 'tab'
        settings_wrapper_widget = QWidget()
        settings_layout = QVBoxLayout()
        settings_wrapper_widget.setLayout(settings_layout)

        settings_layout.addWidget(SettingsWindow(self.settings, self, lambda: stack_layout.setCurrentIndex(0)))

        # stack layout
        stack_wrapper_widget = QWidget()
        stack_layout = QStackedLayout()
        stack_layout.addWidget(main_wrapper_widget)
        stack_layout.addWidget(settings_wrapper_widget)
        stack_wrapper_widget.setLayout(stack_layout)

        # set stack layout as central widget
        self.setCentralWidget(stack_wrapper_widget)

        # toolbar buttons

        # home
        button_home = QAction(QIcon(os.path.join(asset_path, 'home.svg')), 'Home (H)', self)
        button_home.setStatusTip('Go back to the main menu (H)')
        button_home.triggered.connect(lambda: stack_layout.setCurrentIndex(0))
        button_home.setShortcut(QKeySequence("h"))
        toolbar.addAction(button_home)

        # spacing between main options and home button
        toolbar.addSeparator()

        # open
        button_open = QAction(QIcon(os.path.join(asset_path, 'open.svg')), 'Open file (CTRL + O)', self)
        button_open.setStatusTip('Open a file containing traces using your file system (CTRL + O)')
        button_open.triggered.connect(self.get_filepath)
        button_open.setShortcut(QKeySequence("Ctrl+o"))
        toolbar.addAction(button_open)

        # save
        button_save = QAction(QIcon(os.path.join(asset_path, 'save.svg')), 'Save your work', self)
        button_save.setStatusTip('Saves all traces up to this point and skips the rest')
        button_save.triggered.connect(self.skip_rest)
        toolbar.addAction(button_save)

        # settings
        button_settings = QAction(QIcon(os.path.join(asset_path, 'settings.svg')), 'Open Settings', self)
        button_settings.setStatusTip('Make the Synapse Selector Experience your own')
        button_settings.triggered.connect(lambda: stack_layout.setCurrentIndex(1))
        toolbar.addAction(button_settings)

        # spacer between settings and navigation
        toolbar.addSeparator()

        # back
        button_back = QAction(QIcon(os.path.join(asset_path, 'back.svg')), 'Go back to previous Sample', self)
        button_back.setStatusTip('Go back to the previous trace')
        button_back.triggered.connect(self.back)
        toolbar.addAction(button_back)

        # trash
        button_trash = QAction(QIcon(os.path.join(asset_path, 'trash.svg')), 'Trash Sample', self)
        button_trash.setStatusTip('Trash the current trace')
        button_trash.triggered.connect(self.trash_trace)
        toolbar.addAction(button_trash)

        # keep
        button_keep = QAction(QIcon(os.path.join(asset_path, 'keep.svg')), 'Keep Sample', self)
        button_keep.setStatusTip('Keep the current trace')
        button_keep.triggered.connect(self.keep_trace)
        toolbar.addAction(button_keep)

        # add
        self.button_add = QAction(QIcon(os.path.join(asset_path, 'add.svg')), 'Add Response', self)
        self.button_add.setStatusTip('Add another peak')
        self.button_add.setEnabled(self.settings.config['select_responses'])
        # button_add.triggered.connect()
        toolbar.addAction(self.button_add)

        # add separator between file path and rest
        toolbar.addSeparator()

        # file path
        self.file_path_label = QLabel('Current open file: ')
        toolbar.addWidget(self.file_path_label)

        # plot
        self.trace_plot = QtWebEngineWidgets.QWebEngineView(self)
        self.trace_plot.hide()

        # startup label
        self.startup_label = QLabel('Welcome to Synapse Selector! As a first step open up a file with traces using the toolbar.')
        self.startup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.startup_label)

        if (self.synapse_response):
            self.plot()

    def update_file_path_label(self, filepath: str):
        self.file_path_label.setText('Current open file: ' + filepath.split('/')[-1])

    def reset(self):
        self.main_layout.removeWidget(self.trace_plot)
        self.trace_plot.hide()
        self.main_layout.addWidget(self.startup_label)
        self.synapse_response = None
        self.update_file_path_label('')

    # --- slot functions ---
    def get_filepath(self):
        # no directory has been saved
        if self.directory is not None:
            self.filepath = QFileDialog.getOpenFileName(
                caption="Select Input File",
                directory=self.directory,
                filter="Table(*.txt *.csv *.xlsx *.xls)",
            )[0]
        else:
            self.filepath = QFileDialog.getOpenFileName(
                caption="Select Input File",
                filter="Table(*.txt *.csv *.xlsx *.xls)",
            )[0]

        if self.filepath == '':
            warning = QMessageBox(self)
            warning.setWindowTitle('Warning')
            warning.setText('No file has been selected')
            warning.exec()
            return

        self.filename = os.path.basename(self.filepath)
        self.directory = os.path.dirname(self.filepath)
        self.update_file_path_label(self.filepath)
        self.open_file()

    def open_file(self):
        """
        Opens a new file holding the synaptic responses.
        This file should have meta columns (that will be ignored) and appended to the
        resulting output dataframes and response columns.
        All responses columns will be plotted.
        """
        self.synapse_response = SynapseResponseData(
            self.filepath, self.filename, self.settings.config["meta_columns"]
        )
        self.peak_selection_buttons = []
        self.labels = []
        # remove startup label and add plot
        self.main_layout.removeWidget(self.startup_label)
        self.trace_plot.show()
        self.main_layout.addWidget(self.trace_plot)
        self.plot()

    def plot(self):
        """
        Plots a trace of the response that a specific Synapse gave.
        This is done by creating a instance of trace_plot (plot.py),
        that handels all operations of the figure.
        """
        # check to load normalized or unnormalized trace
        if self.settings.config['normalized_trace']:
            trace = self.synapse_response.norm_intensity
        else:
            trace = self.synapse_response.intensity

        if self.settings.config["select_responses"]:
            self.peak_selection()

        self.threshold = compute_threshold(
            self.settings.config["stim_used"],
            trace,
            self.settings.config["threshold_mult"],
            self.settings.config["threshold_start"],
            self.settings.config["threshold_stop"],
        )

        self.peak_detection()

        # create plot depending on mode
        if self.settings.config["peak_detection_type"] == "Thresholding":
            self.tr_plot = trace_plot(
                self.synapse_response.time,
                trace,
                self.threshold,
            )
        else:
            self.tr_plot = trace_plot(
                self.synapse_response.time,
                trace,
                self.threshold,
                self.model.preds,
            )
        self.tr_plot.create_plot()

        # add responses
        if self.settings.config["select_responses"]:
            if self.settings.config["stim_used"]:
                self.tr_plot.add_stimulation_window(
                    self.stim_frames, self.settings.config["stim_frames_patience"]
                )
            selection = [btn.isChecked() for btn in self.peak_selection_buttons]
            if self.settings.config["peak_detection_type"] == "Thresholding":
                self.labels = self.tr_plot.add_peaks(
                    self.synapse_response.peaks, self.settings_.config["nms"], selection
                )
            else:
                self.labels = self.tr_plot.add_peaks(
                    self.synapse_response.peaks,
                    self.settings.config["nms"],
                    selection,
                    self.model.preds,
                )

        # set plot
        self.trace_plot.setHtml(self.tr_plot.fig.to_html(include_plotlyjs="cdn"))

    def next(self):
        """
        Opens next trace and if this is the last trace, it opens a new file.
        """
        # reinitalize labels
        self.labels = []
        # check if end of file
        if self.synapse_response.end_of_file():
            # if the output paths are not set, the user needs to set them now
            if self.settings.config['output_filepath'] == '':
                warning = QMessageBox(self)
                warning.setWindowTitle('Warning')
                warning.setText('No output path has been set. Please select it before your files can be saved.')
                warning.exec()
                self.settings.get_output_folder(self)
                # abort next() if output paths have not been set
                if self.settings.config['output_filepath'] == '':
                    warning = QMessageBox(self)
                    warning.setWindowTitle('Warning')
                    warning.setText('No output path has been set. Your data has not been lost. Make sure to select an output path.')
                    warning.exec()
                    return

            # tell the user that the file was done and it has been saved
            msg = QMessageBox(self)
            msg.setWindowTitle('Info')
            msg.setText('You reached the end of the file. Your data will be saved at the set output path')
            msg.exec()
            self.synapse_response.save(
                self.settings.config["export_xlsx"],
                os.path.join(self.settings.config['output_filepath'], 'keep_folder'),
                os.path.join(self.settings.config['output_filepath'], 'trash_folder'),
                self.settings.config["compute_ppr"],
                self.stim_frames,
                self.settings.config["stim_frames_patience"],
            )
            # self.clear_selection_buttons()
            self.reset()
            return

        # advance to next trace if file isn't at eof
        self.synapse_response.next()
        self.peak_selection_buttons = []
        self.plot()
        # self.clear_selection_buttons()

    def back(self):
        """
        Go one trace plot back
        """
        success = self.synapse_response.back()
        if success:
            self.next()

    def keep_trace(self):
        """
        Select trace as a trace that is kept.
        """
        if self.settings.config["select_responses"]:
            selection = [int(btn.text().split(" ")[1]) for btn in self.peak_selection_buttons if btn.isChecked()]
        else:
            selection = []

        self.synapse_response.keep(
            self.settings.config["select_responses"],
            self.settings.config["frames_for_decay"],
            selection,
            self.stim_frames,
            self.settings.config["stim_frames_patience"],
        )
        self.next()

    def trash_trace(self):
        """
        Put trace to the unselected traces
        """
        self.synapse_response.trash()
        self.next()

    def skip_rest(self):
        """
        Method to skip all remaining traces (these will be appended to trash) and
        open next file.
        """
        response = QMessageBox.question(
            self, "Skip Rest", "Do you wish skip the remaining traces and save your current results?"
        )
        if response == QMessageBox.StandardButton.No:
            return
        self.synapse_response.trash_rest()
        self.next()

    def peak_detection(self):
        """
        Runs peak detection and hands peaks to synapse_response data class.
        """
        if self.settings.config["peak_detection_type"] == "Thresholding":
            automatic_peaks = peak_detection_scipy(
                self.synapse_response.norm_intensity,
                self.threshold,
                self.settings.config["stim_used"],
                self.stimframes,
                self.settings.config["stim_frames_patience"],
            )
        else:
            if not self.model.weights_loaded:
                self.model.load_weights(self.settings.config["model_path"])
            automatic_peaks = self.model.predict(self.synapse_response.norm_intensity, self.settings.config['threshold_slider_ml'] / 100,)
        self.synapse_response.add_automatic_peaks(automatic_peaks)

    def update_probability_label(self) -> None:
        # self.current_threshold.setText(f"{self.threshold_slider.value()}%")
        automatic_peaks = self.model.update_predictions(self.settings.config['threshold_slider_ml'] / 100)
        self.synapse_response.automatic_peaks = []
        self.synapse_response.add_automatic_peaks(automatic_peaks)
        self.plot()
