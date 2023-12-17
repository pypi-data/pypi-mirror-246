[![PyPI Version](https://img.shields.io/pypi/v/ML-medic-kit.svg)](https://pypi.org/project/ML-medic-kit/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marthadinsdale/hds_ca2/HEAD)

# Machine Learning Medic Kit

## Introduction
Welcome to the Machine Learning Medic Kit, a Python package designed to enhance the capabilities of health data scientists tackling binary classification problems.

This toolkit simplifies and enhances your workflow, providing a comprehensive set of tools for model selection, data preprocessing, evaluation, and visualization, tailored toward health datasets.  By utilizing the toolkit, data scientists can shift their focus to the analyses of results and predictions, reducing the time and effort spent on manual model fitting and comparison. 



## Purpose
Binary classification tasks are fundamental in health data science, essential for critical analyses such as disease identification and predicting treatment outcomes. The accuracy of binary classification therfore has a profound impact on clinical decisions and patient care. Recognizing the crucial nature of choosing and training the most appropriate model for binary classification, we developed the Machine Learning Medic Kit.



## Features 
This toolkit offers:

- Data preprocessing tailored for health datasets.
- Train and test multiple classifiers with a single command.
- Tools to fine tune models for peak performance
- Tools for effective model comparison and evaluation.
- Visualization utilities for side-by-side model analysis.



## Usage     
Follow the included user guide notebooks for step-by-step instructions on utilizing the Machine Learning Medic Kit, complete with practical examples on two different health datasets.



## Getting Started

### Installation
The Machine Learning Medic Kit is available on PyPI and can be easily installed using standard Python package management tools. To install, run:
```
pip install ML-medic-kit
```

### Dependencies
Before you can use the Machine Learning Medic Kit, you'll need to ensure that your system has the following dependencies installed:
* jupyterlab==1.2.6
* matplotlib==3.1.3
* numpy==1.18.1
* pandas==1.0.1
* pytest==5.3.5
* scipy==1.4.1
* seaborn==0.10.0
* scikit-learn==0.24.1
* pytest-cov==2.10.0
* setuptools>=51.1.2
* twine>=3.3.0
* wheel>0.36.2
* shap==0.40.0

To install these dependencies, the authors recommend the following:
```
conda create -n new_env python=3.8
```

```
conda activate new_env
```
```
pip install -r /path/requirements.txt
```

```
pip install ML-medic-kit
```

```
import ML_medic_kit
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## Contact
For any queries, please reach out to:
* md661@exeter.ac.uk
* hm761@exeter.ac.uk

