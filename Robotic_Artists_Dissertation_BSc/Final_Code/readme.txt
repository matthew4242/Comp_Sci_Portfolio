This document talks about how to get the project 'Robotic Artist' running:
    Required devices:
        Roland DXY-990 Pen Plotter
        Monitor
        Raspberry Pi
        Mouse
        KeyBoard
    The python libraries that need to be installed are:
        PYQT4
        pySerial
        OpenCV
        Threading
        Unittest
    The method to run the Robot can be done in two ways,
    with or without the Roland DXY-990 Pen Plotter. However, if without the Roland DXY-990
    Pen Plotter at the plotting stage of the graphical user interface an error will occur
    saying that the serial cannot be found.

    To run:
        Make sure that the Plotters serial is connected to port 0. If the plotter is being used.

        Enter the source_code file in the terminal and run python 2.7 application.py.
            An example of this on the Raspberry Pi being used for tests is
                'python application.py'
    To Run Unit Tests:
        Run python 2.7 run_tests.py
            If using plotter remove skip in test_serial_controller.py
