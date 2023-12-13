# MLFoMpy
MLFoMpy is a post-processing tool for semiconductor TCAD data. The center object of this tool is the fds (FoMpy Dataset),
in which through the parsers, all the necessary information is stored. There are also defined different utilities to
process the data stored in the fds object, as to extract figures of merit, to plot or to save results in files.

The figure shows basic workflow behind the MLFoMpy library:

![Scheme of the MLFoMpy post-processing tool](./doc/img/MLFOMPY_diagram.png)

## MLFoMpy documentation

* The project documentation is available in https://mlfompy.readthedocs.io/

In the project folder *examples* there are several scripts and [Jupyter Notebooks](https://jupyter.org/) that show the library functionality:

* Basic usage of the software functionalities in [basic_usage.py](examples/basic_usage.py)

* Figure of merit extraction for drift-diffusion, Monte Carlo, or combined simlations in [extract_dd_mc.py](examples/extract_dd_mc.py)

* Machine learning models and utilities to predict figures of merit and I-V characteristic in [train_mlp_ler.ipynb](examples/train_mlp_ler.ipynb), [train_mlp_mgg_fom.ipynb](examples/train_mlp_mgg_fom.ipynb) and [train_mlp_mgg_iv.ipynb](examples/train_mlp_mgg_iv.ipynb)

## Installation
First you need to have installed **pip3** on your system. For Ubuntu, open up a terminal and type:

    sudo apt update
    sudo apt install python3-pip

**Instalation of MLFoMpy via pip3**

For basic usage of the tool (figure of merit extraction), install the tool using pip3:

    pip3 install mlfompy

To add the machine learning functionality for figure of merit and I-V characteristic
predictions, install the library using the command:

    pip3 install mlfompy[ML]

and check the library is installed by importing it from a **python3 terminal**:

    import mlfompy

Unless an error comes up, MLFoMpy is now installed on your environment.

For more detailed explanation about instalation, please, check
the [documentation](https://mlfompy.readthedocs.io/#getting-started).

**Documentation generation**

Documentation of the project should be available at https://mlfompy.readthedocs.io/.
To generate a local copy of the documentation, first it is necesary to install the
tool [Sphinx](//sphinx-doc.org) with the following command:

    pip3 install sphinx

Then, to generate the documentation, run the following command in the project directory:

    sphinx-build -a doc DOC_DESTINATION_DIR

DOC_DESTINATION_DIR is the directory where the documentation will be generated.
Normally you should choose a directory outside of the project directory.

Once generated, the documentation, in HTML format, can be opened using a web browser,
using the following destination:

    file://DOC_DESTINATION_DIR/index.html
