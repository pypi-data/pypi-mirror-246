# NiCo

Developed by Ankit Agrawal (c) Grün lab 2023

Find covariation patterns between interacting cell types from image-based single cell resolution spatial transcriptomics data.


A package that performs cell type annotations on spatial transcriptomics data, finds the niche interactions and covariation patterns between interacting cell types.

Ready for use! Tutorials and Documentation are available!


## Install the NiCo package using the conda environment.  

```shell
conda create -n nicoUser python=3.11
conda activate nicoUser
pip install nico-sc-sp
pip install jupyterlab
```

# Required packages built upon
By default, these packages should install automatically.
But if any version conflict exists, the user can install the specific version independently using pip command.
```shell
scanpy==1.9.6
seaborn==0.12.2
scipy==1.11.3
matplotlib==3.7.3
numpy==1.26.1
gseapy==1.0.6
xlsxwriter==3.1.9
numba==0.58.1
pydot==1.4.2
KDEpy==1.1.8
pygraphviz==1.11
networkx==3.2.1
sklearn==1.3.2
pandas==2.1.1
leidenalg
```

# Import the functions from the Python prompt in the following way.  

```python
from nico import Annotations as sann
from nico import Interactions as sint
from nico import Covariations as scov
```

# Documentations

Please follow the NiCo documentation here.

https://nico-sc-sp.readthedocs.io/en/latest/

# Tutorials
Please follow the NiCo tutorial here.

https://github.com/ankitbioinfo/nico_tutorial


# Check out more:
Thanks to the following two utils packages used to develop NiCo.

SCTransformPy

https://github.com/atarashansky/SCTransformPy

pyliger

https://github.com/welch-lab/pyliger
