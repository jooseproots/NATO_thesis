# NATO Thesis Project

This repository contains the data analysis and research code for my thesis project focused on analysing how economic variables influence recruitment and retention in NATO countries. The project involves data cleaning, exploration, correlation analysis, multicollinearity checks, and regression analysis using multiple years of military data.

## Project Structure

- **analysis/**: Contains Python scripts for data cleaning, exploration, and statistical analysis.
  - `correlation_analysis.py`: Analyses bivariate correlations between variables.
  - `dataset_exploration.py`: Explores and summarizes the datasets.
  - `multicollinearity.py`: Checks for multicollinearity among features.
  - `regression_analysis.py`: Performs regression analysis.
  - `data_cleaning/`: Scripts for cleaning and preprocessing raw data.
- **clean_data/**: Cleaned CSV files ready for analysis.
- **raw_data/**: Original, unprocessed data files.

## Getting Started

### Prerequisites

- Python 3.8+
- See [requirements.txt](requirements.txt) for required Python packages.

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/jooseproots/NATO_thesis.git
    cd NATO_thesis
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. Place raw data files in the `raw_data/` directory.
2. Run data cleaning scripts in `analysis/data_cleaning/` to generate cleaned datasets in `clean_data/`.
3. Use the analysis scripts in `analysis/` to perform exploratory data analysis, correlation, multicollinearity checks, and regression.

# Additional documentation

Because this code was used to write a thesis, additional explanation of what each script was used for can be found in the thesis, which is available in a pdf file [here](https://github.com/jooseproots/thesis_paper).

# Licence

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# Contact

For questions or collaboration, please contact me at [joosep.roots@gmail.com](mailto:joosep.roots@gmail.com).