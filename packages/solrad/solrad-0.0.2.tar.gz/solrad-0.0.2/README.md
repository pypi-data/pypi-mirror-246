<h1 align="center">
<img src="solrad_logo_ai_rescaled_2.png" width="400">
</h1><br>

Solrad is a modular set of tools, entirely written in Python 3, designed for modeling and estimating the spatial and spectral distributions of radiation coming from the sky. The package enables the computation of relevant radiometric quantities such as (spectral or regular) radiance, (spectral or regular) radiant exposure vectors, and total absorbed energy. For this, solrad employs a simplified All-Sky radiation model that incorporates geographic and meteorological data of a site in its calculations.

Solrad is a project that aims to provide an easy-to-use, *plug and play*, solution for the problem of sky radiation modeling; from the acquisition and processing of site-relevant variables to the implementation and computation of spectral and spatial radiation models.


# Installation 
You can install Solrad directly from PyPI using the following command:

```bash
pip install solrad
```

# Getting started
To get started with Solrad, we recommend downloading the 'examples' folder and following the step-by-step tutorial presented there in the intended order. This tutorial will guide you through downloading all required third-party satellite data, processing it, setting up a simulation instance, acquiring the necessary site-relevant variables, and performing the computation of relevant radiometric quantities.

Solrad currently lacks official documentation (work in progress), but all classes, functions, and modules are thoroughly documented using docstrings. We encourage you to read these docstrings whenever you feel lost.