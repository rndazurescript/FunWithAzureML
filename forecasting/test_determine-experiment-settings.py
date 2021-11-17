import sys

from checknotebookoutput import checkNotebookOutput


# Check the output cells of the notebook.
checkNotebookOutput("auto-ml-forecasting-bike-share.nbconvert.ipynb" if len(sys.argv) < 2 else sys.argv[1],
                    "warning[except]retrying[except]UserWarning: Matplotlib is building the font cache"
                    "[except]warning: a newer version of conda exists"
                    "[except]UserWarning: Starting from version 2.2.1, "
                    "the library file in distribution wheels for macOS is built by the Apple Clang"
                    "[except]The following algorithms are not compatibile with lags and rolling windows"
                    "[except]brew install libomp"
                    "[except]If 'script' has been provided here"
                    "[except]If 'arguments' has been provided here")
