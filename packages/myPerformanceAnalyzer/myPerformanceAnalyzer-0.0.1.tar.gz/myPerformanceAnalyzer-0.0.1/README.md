# Python Package Performance Analysis System

This is a customization analysis system that supports multiple data (JSON, XML, CSV) that has capability to configure and used among multiple domain.

### Description

The Performance Analysis System is a flexible project developed by students in Master of Data Science Program at UBC-O, to extract data from various sources such as CSV, JSON, and XML files to provide meaningful statistical metrics and plots to help customers from different fields tom visualize performance.
The configuration in the system helps user to input their needs. The system fetches the data from configured data source and does data processing accordingly to visualize it and extract the information if required. The visualization part include table (mean, median, mode, count, min and max), bar plot, line chart, scatter plot and box plot. The user can either choose to see it or export it.

### Package structure

* |main/
* |   |  data_processor
* |   |   | configuration.py
* |   |   | entity.py
* |   |   | performanceanalyzer.py
* |   |  data_transformer
* |   |   | data_manager_factory.py
* |   |   | abstract_parser.py 
* |   |   | transformer-csv_parser.py
* |   |   | xml_parser.py
* |   |   | json_parser.py
* |   |   | custom_exception.py


- `package-main` The main package facilitates the entire setup process, such as retrieving the configuration and prompting the user to choose the information to compute and/or visualize.
- `subpackage1-\main\data_processor` The main sub-package provides a structured and modular approach to handling data. It ensures that the necessary configuration is in place before performing data operations.
- `subpackage1-module1 \main\data_processor\configuration.py` This module provides a structured and modular approach to handling data. It ensures that the necessary configuration is in place before performing data operations.
- `subpackage1-module2 \main\data_processor\entity.py` This module processes entities and collections (e.g. student-students, employee-employees, etc.).
- `subpackage1-module3 \main\data_processor\performanceanalyzer.py` This module generates a summary of basic statistical metrics for the data from the entity collection. It also facilitates the creation of appropriate plots.
- `subpackage2-\main\data_trasformer` This main function of this sub-package is to co-ordinate and control data parsing and data transformation from user data type to Entity Collection type.  
- `subpackage2-module1 \main\data_trasformer\data_manager_factory.py` It helps to invoke the respective parser depending on the data type of the input configuration.
- `subpackage2-module2 \main\data_trasformer\abstract_parser.py` This class serves as a parent class which is inherited by all the other parsers classes. It helps to parse and evaluate expression in configuraion.
- `subpackage2-module3 \main\data_trasformer\csv_parser.py` This class is responsible for parsing  CSV data into Entity Collection.
- `subpackage2-module4 \main\data_trasformer\xml_parser.py` This class is responsible for parsing  XML data into Entity Collection.
- `subpackage2-module4 \main\data_trasformer\json_parser.py` This class is responsible for parsing  JSON data into Entity Collection.

### How to use the package

1. Download the package and store in your working repository.

2. If you want to create config you can follow step 3. If not the system creates a config on behalf of you. So you can directly go to step 4.

3. In your current working directory create a json file with name `config.json`.

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

3.0.  data_type: this property denotes what type of data source file you have.
    
3.1.  entity_collection: this denotes the sample data collection name present in data file.
    
3.2. base_field: the field which can be considered X axis field for visualization.
    
3.3. computable_fields: the operational fields on which caulations can be computed. As of now, we support only +, -, /, * with 2 variables.
    
3.4. path: the data source path.

    
4. Import the package in your code and call run method. The main package name is "main" and initial process starts with method run(). So you can use below code to run the package.

   `from main import run` 

    `run()`
  

5. If you haven't filled config, then system prompts to enter the config data.


6. After processing the data, you can choose to see the data or export it.

7. Sample Data(incase you want for testing):
   
```    {
      "students": [
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


