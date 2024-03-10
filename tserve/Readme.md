# Torch Serve  

Torch serve is a model serving library that allows you to deploy machine learning models in a production environment. It is built on top of the PyTorch library and is designed to be easy to use, scalable and high performance.

## Deploying 

### Torch Serve itself

  * use **jetson/deploy.sh** script to deploy the model on jetson orin
    * it will fetch the torch serve repository  
    * build docker image for jetson 
    * and start the container

### Model on Torch Serve
  
  * configure which models to use in **./models/config.sh**
  * build models archive using **./models/build_models.sh**
    * it will generate model archives in **./model_store** folder
  * register models with torch serve using **./models/register_models.sh**

## Adding a new model 

  * make sure the model name is unique 
  * create a folder with the model name in **./models** folder
    * add files 
      * model_da.py
        * this file should contain the model class
      * df_handler.py
        * this file contains serialization and deserialization functions for the https request  
      * any additional files
        * make sure to add these files to extra_files in **./models/config.sh**
  * update the **./models/config.sh** file to include the new model
    * add the model name to the models array
    * add extra files to the extra_files array
  * build the model archive using **./models/build_models.sh** 
  * register the model to running instance of torch serve using **./models/register_models.sh**





