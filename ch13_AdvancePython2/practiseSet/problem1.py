# Create a Virtual Environment, install few pakages in the first one. How do you create a similar environment in the second one?
"""
======================   Docstring for practiseSet.problem1 ==============


PREREQUISIT : "pip install virtualenv"

Step 1 ---> Create virtual env1 and virtual env2 
        By Using command "virtualenv env1"

Step 2 ----> Activate any one of environment  by using the command:
                ".\env1\Scripts\activate.ps1" ---> This will activate env1 virtual environment

Step 3 ----> Now Install Pacakges like : "pandas", "pyjokes", 

Step 4 ----> Create a requirement.txt file by running the command 
            "pip freeze > requirements.txt"

Step 5 -----> Now deactivate this env1 
        command: "deactivate"

Step 6 ----> Now activate env 2 enviroment  (Read step 2)

Step 7 ----> Now in this new env2 install old pakages using requirement.txt file
            Using command "pip install -r .\requirements.txt"


"Conclusion: After Step 7 you are able to install the pakages from env1 emviroment to env2 environment"
"""