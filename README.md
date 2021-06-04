# EnR4D
Project realized at ENSEIRB-MATMECA in collaboration with Orange. This repository gathers the documentation realized throughout the project, a bibliography gathering important sources and the Github Project facilitating the distribution of the tasks.


## Project management tool

The Github Project is accessible via the Project tab on this page. It gathers all the User Stories : to do, in progress and done.

Link to the weekly tracking table : https://docs.google.com/presentation/d/1LTmyKdJtUMtE4mM98s6AkLWbQGiaFR6oFwXyF4fA1xQ/edit?usp=sharing

## Add an User Story (issue) on Github Project

"Issues" tab
On the main part:

   --> "New issue"
 
   --> Add a explicit/detailed title
 
On the right (parameters) :
 
   --> Assignees : No one
 
   --> Labels : enhancement
 
   --> Projects : Projet EnR4D
 
Finally, "Submit new issue"
 
The User Story will be automatically added on the rubrik "To Do" of the Github Project.

## How to launch the algorithm
The final algorithm we had implemented is "main_merged.py" located in "Code" folder.
When launched, the algorithm creates a desired number of workloads. At each new loop, the algorithm redistributes the workloads according to a ratio. 
This ratio is calculated using weather data (production) and the number of workloads running on a datacenter (consumption).

### Prerequisites
The algorithm uses wiremock which must be installed and three yaml configuration files.

#### Wiremock
Go to this page http://wiremock.org/docs/download-and-installation/ and download the link at the bottom of the page.
Once wiremock is installed, you have to move it in the "simulate_meteo.jar" folder. To launch wiremock, just type the following command in a terminal:
``
java -jar blabla
``

#### Yaml configuration files
At each run, the algorithm creates a specified number of workloads. 
The creation of these workloads is based on three yaml files "worker1.yaml", "worker2.yaml" and "worker3.yaml" located in the "Code" folder.
It is necessary to place in the same folder these three configuration files and the file "main_merged.py"

## Run the algorithm
First you have to launch wiremock with the command : 
``
java -jar blabla
``
Then, you just have to type the following command :
``
python3 main_merged.py
``

To restart the algorithm, you will have to delete the pods and files that were created during the execution of the algorithm.
Use the following commands:

``
rm worker*_*
``
``
 kubectl delete pod pod1 pod2 pod3 pod4 pod5 pod6 pod7 pod8 pod9 pod10
``
The second command depends on the number of pods created, you will have to adjust according to what you choose.
