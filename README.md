
# Urban Home Finder 
## Team Neighborhood Change  
Georgetown University  
School of Continuing Studies  
Data Science Certificate Capstone Project
## Team Members
Karen Belita - [@kbelita](https://github.com/kbelita)  
Veronica Helms - [@vevahelms](https://github.com/vevahelms)  
Emily Pugliese - [@emilypugliese](https://github.com/emilypugliese)  
Hua Zhong - [@hzhongDC](https://github.com/hzhongdc)  

## Abstract  
>Millennials represent one-quarter (24%) of the United States population but made up almost half (43%) of all movers during 2007-2012.  This unique demographic population resides in urban areas at higher rates than any other generation and surveys suggest that the majority of millennials prefer living in metropolitan areas. Urban Home Finder was developed as an application to provide a platform for users to input preferences associated with metropolitan centers. The application’s purpose is to assist millennials in choosing their next urban home wisely. Using underlying machine learning processes, user inputs are used to predict urban areas aligned with user preferences. Eight data sources at varying levels of geography were ingested and wrangled to extract forty features from structured raw data files. With a dataset containing indicators for over twenty topics, two machine learning processes, unsupervised and supervised, were employed to label, describe, and analyze the data. Clustering was used to assign 300 metropolitan statistical areas, the measure used to define an urban center, into sixteen clusters. Classification techniques were used to describe clusters and select the best predictor model. K Nearest Neighbors using all forty features was ultimately selected as the final predictor model and outputted a F1 score of 0.962. Within Jupyter notebook, slider widgets were employed to allow users a platform for preference input. In the final application, the predictor model uses five inputs determined via domain expertise (while to remaining thirty-five indicators remained constant) to predict and output one to five recommended metropolitan areas. 

## Project Overview
**Project Purpose**: Provide a platform to determine a metropolitan area of interest based on user preferences.  
**Unit of Analysis**: Metropolitan Statistical Areas (MSAs) represent core urban areas consisting of a 50,000 or more population.  As of July 2015, 389 MSAs were delineated, but 300 MSAs were utilized for the purposes of this project.  
**Research Questions**: 
What characteristics do millennials prioritize when considering metropolitan areas for a future move? 
What features predict MSA selection?  
**Hypothesis**: The most predictive features of a MSA will be rent burden, employment, and crime. 
> **Project Architecture**
> ![Neighborhood Change Architecture](https://github.com/kbelita/neighborhood-change-images/raw/master/neighborhood-change-architecture.png)  

## Summary of Methodology
**Ingestion**: Download data from data sources using their API or download directly from their website.  
**Wrangling**: Clean and organize data in preparation for storage and analysis.  
**Normalization**: Store and merge clean data in PostgreSQL.  
**Machine Learning**: Employ unsupervised and supervised machine learning methods to describe data and select predictive model for application.  
**Application**: Create interactive visualizations and an ipywidgets slider that serves as a recommender application.  

> **[Interactive Bubble Chart](https://plot.ly/~karen.belita/2.embed "https://plot.ly/~karen.belita/2.embed")**
 [![Data Visualization](https://raw.githubusercontent.com/kbelita/neighborhood-change-images/master/Indicators_Clusters.png)](https://plot.ly/~karen.belita/2.embed "https://plot.ly/~karen.belita/2.embed")  

## Data Sources  
American Community Survey  
USDA Food Atlas  
Walkability Index  
National Assessment of Educational Progress  
FBI Uniform Crime Reporting  
BLS Unemployment Reporting  
Public Transportation Safety

## File Organization
**ing-wr**: Folder contains ingestion and wrangling python scripts and notebooks.  
**storage**: Folder contains scripts for creating the database in PostgreSQL, loading data into PostgreSQL, and generating a csv file with data ready for analysis and machine learning.  
**ml-application**: Folder contains notebooks for unsupervised and supervised machine learning, application, and visualizations.  


