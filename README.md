# Convoy Shipping Company

This is designed to streamline the process of converting a spreadsheet (.xlsx) file into different formats (.csv, .s3db, .json, and .xml) through a series of steps that also include data correction and evaluation. It is perfect for automated processing of vehicle data with scoring based on fuel efficiency and load capacity.

## Features

- **Excel to CSV Conversion**: Converts `.xlsx` files to `.csv`, specifically targeting a sheet named `Vehicles`.
- **CSV Correction**: Evaluates and corrects `.csv` files to ensure that all data is numeric, appending `[CHECKED]` to the filename.
- **CSV S3DB Conversion**: Converts corrected `.csv` files into SQLite3 database files (`.s3db`) and assigns scores to each vehicle based on fuel efficiency and load capacity.
- **Database to JSON/XML**: Exports vehicles scoring above or equal to 4 to a `.json` file and those below 4 to an `.xml` file.

## Requirements

- [Python 3](https://www.python.org/downloads/)

## Installation

This application is written in Python, so you'll need Python installed on your computer to run it. If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

To install this project, follow these steps:

1. Clone the repository to your local machine:

```
git clone https://github.com/SonikSeven/convoy-shipping-company.git
```

2. Navigate to the cloned repository:

```
cd convoy-shipping-company
```

3. Create and activate a virtual environment:

```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies using pip and the requirements.txt file:

```
pip install -r requirements.txt
```

## How to Run

To run the program, follow these steps:

1. Open a terminal and navigate to the directory where the script is located.
2. Run the script using Python:

```
python main.py
```

## Usage

Follow the onscreen instructions to input your file name.

Ensure that your initial `.xlsx` file is correctly formatted and that the `Vehicles` sheet is present.

### Step-by-Step Guide

1. **Prepare Your `.xlsx` File**: The file should contain vehicle data in the `Vehicles` sheet.
2. **Run the Script**: Execute the script in your terminal or command prompt.
3. **Input File Name**: When prompted, input the name of your `.xlsx` file.
4. **Follow the Conversion Process**: The script will guide you through the conversion steps automatically.
5. **Access Converted Files**: Find the converted `.csv`, `[CHECKED].csv`, `.s3db`, `.json`, and `.xml` files in the same directory as your original file.

## License

This project is licensed under the [MIT License](LICENSE.txt).
