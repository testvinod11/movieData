# MovieData

### Prerequisite:

    * Python 3.5.2+
    

### System Setup:

1. Environment setup:

    * Install pip and virtualenv:
        - sudo apt-get install python3-pip
        - pip install --upgrade pip
        - sudo pip3 install virtualenv or sudo pip install virtualenv

    * Create virtual environment:
        - virtualenv movies-env

        OPTIONAL:- In case finding difficulty in creating virtual environment by
                  above command , you can use the following commands too.

            *   Create virtualenv using Python3:-
                    - virtualenv -p python3.5 venv
            *   Instead of using virtualenv you can use this command in Python3 for creating virtual environment:-
                    - python3.5 -m venv venv

    * Activate environment:
        - source venv/bin/activate

    * Checkout to branch
        - git checkout "branch_name"

    * Install the requirements by using command:
        - cd movieData/
        * for local system follow below command
        ```
          pip3 install -r requirements.txt
        ```

2. Database Setup

     * DB migrations:
        ```
        $ python manage.py migrate
        ```

3. Run servers:
    ```
     $ python manage.py runserver
    ```
