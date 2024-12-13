**Movie Recommendation System**

Steps to run the project in local environment
1. Install python version 3.11.10
2. Install Python Anaconda
3. Clone the repository using the command - git clone https://github.com/laxman2405/MovieRecommendationSystem.git
4. Go into the MovieRecommendationSystem folder using the command - cd MovieRecommendationSystem
5. Create a conda virtual environment
   
   conda create -n <environment_name> python=3.11.10
   
   conda activate <environment_name>
6. conda update conda
7. conda update --all
8. Ideally, now if we run the command 'pip install -r requirements.txt' command, it should download the required dependencies. If it doesn't work, then run the command 'conda install scipy' and 'conda install scikit-learn'.
9. Do 'pip list' now to check the versions of scipy and scikit-learn installed and update the same versions in requirements.txt file.
10. Now, run the command 'pip install -r requirements.txt' to download all the required dependencies.
11. Next, we can follow 2 options to run the code in local.
    
    The first way is to train the model to generate the training data. For this, run the command 'python recommendation_system/training.py' command. This command generates two pkl files: sim_final.pkl and movies.pkl. If this step provides any issue while feature extraction, then please follow second way mentioned below.
    
    The second way is, If we don't want to traing the model and run the application in local, then run the command 'pip install gdown' in terminal. Here, it will try to download the training pkl files from shared google drive after the 12th step.
12. Then, go to recommendation_model.py file and comment out lines 13-29, 7 and uncomment lines 32-53 and 6. Then run the command 'python manage.py runserver' on the terminal.
13. This will start the application in localhost.
14. Go to the browser and run with the IP address: 127.0.0.1:8000
15. The Movie Recommendation System application should start working now!
