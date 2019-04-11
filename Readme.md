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