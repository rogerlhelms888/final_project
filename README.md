
# Assignment 04

# Project Proposal

![http://www.pratt.edu/tiny_mce/plugins/imagemanager/files/Light_brown_blue22.jpg](http://www.pratt.edu/tiny_mce/plugins/imagemanager/files/Light_brown_blue22.jpg)

The **purpose of this project** is to have some **well-written** and **well-documented code** in a GitHub repository that illustrates you can write some Python code. This project is for **your** Portfolio, so pick something you are **interested in** or that's **useful** (either in some professional work or automating some task). [Learn how the project is evaluated (rubric)](https://github.com/pratt-savi-810/pratt-savi-810-2020-03-project).


#### Project Routes

There's a couple of routes you can go;

1. **Creating a Tool to Automate a Task** - usually for some task automation, less an analysis, more data engineering. 
2. **Performing Data Analysis to Answer a Research Question** - this type of project requires plots and data insights. 

Since writing the code is the challenging part. Do not think about this in scope of a normal project. **Keep your scope focused!** Keep it limited in functionality and if you finish early, you can add more features. I've seen students go down some pretty deep rabbit holes and emerge with some very disorganized projects. You could have only 30 lines of code or so, and still have a great project so long as the code is well written and the doc's are informative and it has some functionality that's useful in some capacity. Most likely someone such as a hiring manager will only glance at your Repository, so you want it to be organized and clean and very clear as to its purpose. 

## Assignment 04 Submission
You will **Fork** and **Clone this Repo** and **edit this README.md Markdown file**. This is your submission, just the link to your forked Repo and edited README.md file. This project should be the edited version of this README.md (**Markdown**) file. 

#### Learn more about [Markdown](https://www.markdownguide.org/). 

Most code editors allow editing of Markdown files, some recommended editors are;

* [Atom](https://atom.io/)
* [MacDown](https://macdown.uranusjr.com/)
* [Visual Studio Code (VS Code)](https://code.visualstudio.com/)
* [StackEdit (edit in-browser)](https://stackedit.io/)
* [Dillinger (edit in-browser)](https://dillinger.io/)
* You can even edit inside of [GitHub](https://github.com/). 

Your Assignment 04 Deliverables are listed below:

# Deliverables

You should edit the following items in-line and substitute any of the provided text with your response below for your README.md Assignment 04 submission. 


---

## Executive Summary

A _brief description_ of your final project idea. 

- **Why** are you doing this project? 
- **How** do you imagine you'll accomplish this project? 
- Is this a project **Creating a Tool to Automate a Task** or **Performing Data Analysis to Answer a Research Questio**? 

This should be a paragraph or so and provide a _high-level overview_ of your project. Again this is a summary, so think of this as the "Elevator Pitch". 

Start Roger's response:__________________
  
- **Project goals**: 
-- To devolop an interactive web based map and graph that draw on a third party database.  
-- To automate the refresh process from that database.  
-- To arrange a degree of user interactivity in specing out the map and graph.  

End Roger's _____________________________

## Background

A more **detailed background** of your project, please include any information that would be useful for understanding the context of the project. This can be as long or short as you'd like. 

Start Roger's:___________________________

My project would focus on the kind of 'Violent incident' graphing and mapping that I'd showed you earlier.   

An NGO named ACLED (Armed Conflict Location & Event Data Project) has a crew of people who scan news stories for 'violent events', which they enter into a database.  Afghanistan is one of the countries they cover.  They log over 10,000 events a year, and do a respectable job of normalizing them, even to the extent of geocoding them with coordinates and standardized place names.  They refresh their public facing database once a week.  You can feed dates, country names and event types to a 'data tool' of theirs and get back a .CSV of the results.

I want to download their data, process it into a database of my own, and link that database to a graph and a map.  Online users would be able to specify the geography and time period that interested them and get back a graph and map.

End Roger's _____________________________


## Resources
List any possible articles, resources or analysis or anything useful and include links and perhaps annotate a sentence as to the key findings of this resource. Or if you cannot find any resources please mention. 

#### Resources List

**Mapping Software**

Start Roger's:___________________________
I have an ArcGIS Online account and would like to us it to host the map.  I'm comfortable with ArcGIS Online and know what I can get out of it.  I'd rather work on learning connectivity at this point, than trying to master python based map plotting.  

End Roger's _____________________________
 
## Input Data 

#### Data Sources List 

Start Roger's:___________________________

**ACLED**
The ACLED data is stored as an XLSX file which ACLED refreshes every week.  So far, I have successfully downloaded the XLSX to my hard drive and opened it as a dataframe.  I might be able to open it direct from the file's download URL on the ACLED site, but I haven't yet tried. (ACLED also has a "Datatool" that returns an almost identical CSV, but it requires too much manual interaction, so we won't use it.)
Some documentation on the database:
ACLED codebook:  https://acleddata.com/acleddatanew/wp-content/uploads/dlm_uploads/2019/04/ACLED_Codebook_2019FINAL_pbl.pdf
Other ACLED resources:
https://acleddata.com/resources/general-guides/

**Boundary files**:
I'm pretty well set for boundary files.  I will document their provenance in the project.  A key one will be the 421 district / 34 provice version admin boundary set of 2018:
https://mapsynch.maps.arcgis.com/home/item.html?id=50ef8d9c306d43c187b70de0d629c6b5

End Roger's _____________________________

#### Data Wish List
List and describe any type of data you'd like to include but had difficulty tracking down. 

* Data Wish List Item A - description
* Data Wish List Item B - description

## Technical Requirements

#### Python Libraries

Start Roger's _____________________________

Pandas / Geopandas - to manage the ACLED data

Matplotlib - for the graph.  (I had hoped to send the data to be graphed directly to AGOL as a CSV, but don't believe that is possible).  I will instead try to graph the data in Matplotlib and pt the Matplotlib product into an AGOL storymap somehow, either as an embeded Iframe or a PNG image file.

End Roger's _____________________________

#### Library Wish List
[None]

## Measuring Success: 

- How will you measure your project's sucess?

	- Is there some metric you'd hope to generate from your project.  	
    Start Roger's _____________________________
    Hits on the site would be fun to see.  My graphs have already had some impact on how people are seeing the story on levels of violence after the withrawal agreement with the Taliban.  
    END Rogers's ______________________________
	- Is there some plot or visualization that will be generated? 
    Start Roger's _____________________________
    An interactive web map and a static but dynamically updatable bar chart.
    END Rogers's ______________________________

	- Is some manual task now fully automated? 
    Start Roger's _____________________________
    Yes.  I've already reported the data afresh a few times, taking hours each time.
    END Rogers's ______________________________


## Project Execution Plan Outline
Please include a short outline describing the steps you'd imagine going through. 

Could be as simple as;

```
- Background Research 
	- Spend some time researching the topic.
    DONE.

- Data Collection
	- Spend time collecting and looking for additional data
	 DONE.
- Exploratory Data Analysis
 	- Summarize the input data, plot and examine any columns that may be useful. 
DONE
- Data Processing
	- A couple of steps that may be needed to Process your data. 
    PARTIALLY DONE.  I AM DOWNLOADING ACLED DATA INTO A DATAFRAME AND PREPPING IT INTO A .CSV OF DATA TO GRAPH AS A BAR CHART, AND A .CSV FILE OF POINTS TO MAP.  FIGURING OUT HOW TO PLUG THE DATA INTO AGOL DYNAMICALLY WILL BE A CHALLENGE FOR ME.
- Results and Conclusion 
	- Key findings.  THAT THE LEVELS OF VIOLENCE HAVE DECREASED GREATLY SINCE PRIOR TO THE WITHDRAWAL AGREEMENT AND SINCE THIS TIME LAST YEAR.  
	- Was your Project Successful.  [YET TO BE DETERMINED.]
	- Generate Assumptions and Limitations. [?]
```
