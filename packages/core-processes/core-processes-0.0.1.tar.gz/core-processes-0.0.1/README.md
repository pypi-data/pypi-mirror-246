# core-processes 


Core implementations of `process-bigraph.composite.Process()` aligning with BioSimulators simulator
tools.


## Getting Started (PyPI)

The simulation tools that live at the heart of the Core Processes are individually installed and imported as 
optional requirements. To interact with this repository and the related simulation tools therein, the syntax for 
installing from the Python Package Index (PyPI) is as follows:

    pip install core-processes[<SIMULATOR>]

where `<SIMULATOR>` can be one of the following simulator options:

    cobra 
    copasi 
    tellurium
    smoldyn


For example, if you wish to create an instance of `TelluriumProcess`, 
the install-command would be:

    pip install core-processes[tellurium]

We recommend using an environment/package manager [like Conda](https://conda.io/projects/conda/en/latest/index.html) to 
install the dependencies required for your use.


### PLEASE NOTE:

The `SmoldynProcess` process dependency installation requires the installation of Smoldyn.
To install Smoldyn, please adhere to the following procedure according to your platform:

#### Linux:
    
1. Create a virtual environment (`conda create -n smoldyn-process python=3.10 && conda activate smoldyn-process`)
2. `pip install smoldyn`

#### Mac:

1. [Download the Mac distribution on the Smoldyn website](https://www.smoldyn.org/download.html)
2. Navigate to the root of the distribution folder
3. `sudo -H ./install.sh`

#### Windows:
1. Follow the same steps for Mac, but for Windows.


## TODO: Add DatabaseEmitter to this README


