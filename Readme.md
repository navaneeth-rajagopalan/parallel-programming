COMP90024_2019_SM1 Assignment 1

Navaneeth Rajagopalan
Avinash Rao

Instructions:
1. In case not in master branch - checkout to the master branch using "git checkout master"
2. cd to "TwitterFiles"
3. run "ln –s /data/projects/COMP90024/bigTwitter.json" to link the bigTwitter.json (tinyTwitter.json and smallTwitter.json are already part of the repository)
4. go back the parent directory where the "TwitterAnalysis_Parallel.py", "TwitterAnalysis_1Node_1Core.sh", "TwitterAnalysis_1Node_8Core.sh" and "TwitterAnalysis_2Node_8Core.sh" are located
5. The "TwitterAnalysis_Parallel.py" is the main file. It will be executed when either of the 3 shell script files are exectuted
6. To run the job in 1 Node with 1 Core run the command (from the parent directory)
    sbatch TwitterAnalysis_1Node_1Core.sh
7. To run the job in 1 Node with 8 Core run the command (from the parent directory)
    sbatch TwitterAnalysis_1Node_8Core.sh
8. To run the job in 2 Node with 8 Core i.e. 4 cores in each node run the command (from the parent directory)
    sbatch TwitterAnalysis_2Node_8Core.sh


Folder Structure:
1. Parent level:
    The parent level contains the following files:
        i. TwitterAnalysis_1Node_1Core.sh
        ii. TwitterAnalysis_1Node_8Core.sh
        iii. TwitterAnalysis_2Node_8Core.sh
        iv. TwitterAnalysis_Parallel.py
        v. TwitterAnalysis_Serial.py
        vi. Readme
2. Config directory:
    This folder is located at the parent level and contains the following:
        i. MelbGrid.json
3. Model directory:
    The directory contains the model class files that store and process the tweet information. This folder is located at the parent level and contains the following:
        i. Grid.py - stores individual grid information (grid id and coordinates, tweet count and hashtags)
        ii. MelbGrid.py - processes the MelbGrid data and builds 16 grid objects and 1 grid object to store the tweets that originated outside any of the 16 given grids (for a sanity check)
        iii. Summary.py - stores the MelbGrid object and the additional information from each core that the application runs on - total tweets processed, execution time, rank.
4. TwitterFiles directory:
    The input file for the application is to be placed here. Run the following command at this directory to make a symbolic link to the Twitter file:
        i. bigTwitter.json
            ln –s /data/projects/COMP90024/bigTwitter.json
5. OutputFiles directory:
    This folder contains the output files resulted from the execution of the job on Spartan. (The files are manually placed here)
        i. Slurm-8081549.out - 1 Node 1 Core
        ii. Slurm-8081550.out - 1 Node 8 Core
        iii. Slurm-8081551.out - 2 Nodes 8 Core