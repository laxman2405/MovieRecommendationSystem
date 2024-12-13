Movie Recommendation System

Steps to run the project in local environment
1. Install python version 3.11.10
2. Install Python Anaconda
3. Clone the repository using the command - git clone
4. Go into the MovieRecommendationSystem folder using the command - cd MovieRecommendationSystem
5. Create a conda virtual environment
   conda create -n <environment_name> python=3.11.10
   
   conda activate <environment_name>
7. conda update conda
8. conda update --all
9. Ideally, now if we run the command 'pip install -r requirements.txt' command, it should download the required dependencies. If it doesn't work, then run the command 'conda install scipy' and 'conda install scikit-learn'.
10. Do 'pip list' now to check the versions of scipy and scikit-learn installed and update the same versions in requirements.txt file.
11. Now, run the command 'pip install -r requirements.txt' to download all the required dependencies.
12. Next, we can follow 2 options to run the code in local.
    The first way is to train the model to generate the training data. For this, run the command 'python recommendation_system/training.py' command. This command generates two pkl files: sim_final.pkl and movies.pkl.
    
    The second way is, If we don't want to traing the model and run the application in local, then run the command 'pip install gdown' in terminal.
14. Then, go to recommendation_model.py file and comment out lines 13-29, 7 and uncomment lines 32-53 and 6. Then run the command 'python manage.py runserver' on the terminal.
15. This will start the application in localhost.
16. Go to the browser and run with the IP address: 127.0.0.1:8000
17. The Movie Recommendation System application should start working now!
