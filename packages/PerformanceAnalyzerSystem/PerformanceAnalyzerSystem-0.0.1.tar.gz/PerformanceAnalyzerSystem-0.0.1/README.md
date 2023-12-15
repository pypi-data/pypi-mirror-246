
![Main badge](https://github.com/Naye013/Data533-Step3-ContinuousIntergration/actions/workflows/main.yml/badge.svg)

# Python Package Performance Analysis System

This is a customization analysis system that supports multiple data formats (JSON, XML, CSV) and has the capability to be configured and used across multiple domains.

### Description

The Performance Analysis System is a versatile project developed by students in the Master of Data Science Program at UBC-O. It extract data from various sources including CSV, JSON, and XML files, to generate meaningful statistical metrics and plots. This system aims to assist customers from different fields in visualize performance.   

The configuration in the system allows user to input their needs. The system fetches the data from the configured data source and process it accordingly to visualize and extract information if required. The visualization part include a table with basic statiscical metrics (mean, median, mode, count, min and max), bar plot, line chart, scatter plot, and box plot. Users can choose to display the results either on the terminal or export the analysis.   

### Package structure

* **main/**
  * **data_processor/**
    * `configuration.py`
    * `entity.py`
    * `performanceanalyzer.py`
  * **data_transformer/**
    * `data_manager_factory.py`
    * `abstract_parser.py`
    * `transformer-csv_parser.py`
    * `xml_parser.py`
    * `json_parser.py`
    * `custom_exception.py`

- **`package-main`:** The main package facilitates the entire setup process, such as retrieving the configuration and prompting the user to choose the information to compute and/or visualize.
- **`subpackage1-\main\data_processor`:** The main package facilitates the entire setup process, such as retrieving the configuration and prompting the user to choose the information to compute and/or visualize.
- **`subpackage1-module1 \main\data_processor\configuration.py`:** This module provides a structured and modular approach to handling data. It ensures that the necessary configuration is in place before performing data operations.
- **`subpackage1-module2 \main\data_processor\entity.py`:** This module processes entities and collections (e.g. student-students, employee-employees, etc.).
- **`subpackage1-module3 \main\data_processor\performanceanalyzer.py`:** This module generates a summary of basic statistical metrics for the data from the entity collection. It also facilitates the creation of appropriate plots.
- **`subpackage2-\main\data_trasformer`:** This main function of this sub-package is to co-ordinate and control data parsing and data transformation from user data type to Entity Collection type.  
- **`subpackage2-module1 \main\data_trasformer\data_manager_factory.py`:** It helps to invoke the respective parser depending on the data type of the input configuration.
- **`subpackage2-module2 \main\data_trasformer\abstract_parser.py`:** This class serves as a parent class which is inherited by all the other parsers classes. It helps to parse and evaluate expression in configuraion.
- **`subpackage2-module3 \main\data_trasformer\csv_parser.py`:** This class is responsible for parsing  CSV data into Entity Collection.
- **`subpackage2-module4 \main\data_trasformer\xml_parser.py`:** This class is responsible for parsing  XML data into Entity Collection.
- **`subpackage2-module4 \main\data_trasformer\json_parser.py`:** This class is responsible for parsing  JSON data into Entity Collection.

### How to use the package

1. Download the package and store in your working repository.

https://pypi.org/project/PerformanceAnalyzerSystem/

3. If you want to create a configuration file you can follow step 3. If not the system creates a configuration file on behalf of you. So you can directly go to step 4.

4. In your current working directory create a JSON file with name `config.json`.

   Sample Config data:

```
 {

    "data_type": "JSON",
    
    "entity_collection": "students",
    
    "base_field": "name",
    
    "computable_fields": ["science", "english", "science+english As total"],
    
    "path": "C://Users//yourData.json"
    
  }
```
Description from the fields within the config.json:

- **data_type:** This property denotes what type of data source file you have.
    
- **entity_collection:** This property denotes the sample data collection name that is present in data file (e.g. Students, Employees, Players, etc.).
    
- **base_field:** This is the field that can be considered the X-axis for creating the plots in the visualization (e.g. ID, name, key, etc.).
    
- **computable_fields:** These are the operational fields on which caulations can be computed. As of now, we support only +, -, /, * with 2 variables.
    
- **path:** The data source path.

    
4. Once the package is installed, import the package in your code to run the PerformanceAnalyzer. The main package name is "main" and initial process starts. So you can use below code to run the package.
  
   import main    

6. If you have not filled the configuration file, then system will prompt you to enter the configuration data.


7. After processing the data, you can choose to display the analysis of your data or export it.

8. Sample Data (in case you want for testing):
   
```
{"students": [
       {
         "name": "John Doe",
         "english": 90,
         "science": 85
       },
       {
         "name": "Jane Smith",
         "english": 95,
         "science": 92
       },
       {
         "name": "Bob Johnson",
         "english": 88,
         "science": 78
       },
       {
         "name": "Karl",
         "english": 92,
         "science": 94
       }
     ]
   }
```
### Authors

- Karthiga Sethu Sethuramalingam
- Nayeli Montiel Rodríguez


