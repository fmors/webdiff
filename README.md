# webdiff


A small challenge implemented by Fernando M. S.


## Installation:


#### Without using included virtualenv


Within a python3 enabled environment:

    # pip install -r requirements.txt
    # python app.py
    
Open your web browser and point it to:

    localhost:5000

    
#### Using included virtualenv


Within a python3 enabled environment:

    # . venv/bin/activate
    # pip install -r requirements.txt
    # python app.py
    
Open your web browser and point it to:

    localhost:5000


## Usage:


This web application will show the difference between 2 data fields through the usage of the following endpoints:


#### Left side data:

    
Post a JSON data:
    
    {
        "data": "<base64 encoded data>"
    }
    
To this endpoint:
    
    localhost:5000/v1/diff/<session_id>/left
    

#### Right side data:


Post another JSON data:

    {
        "data": "<base64 encoded data>"
    }

To this endpoint:
    
    localhost:5000/v1/diff/<session_id>/left


#### Show the diff:


Get the diff from the endpoint below:

    localhost:5000/v1/diff/<session_id>
    

## Design choices:


1. Due to its simplicity, I've chosen Flask web framework. It is not the champion of performance or scalability, but its
easy to deploy makes it a good choice for this exercise.
2. I've focused more in unit testing than automating end-to-end tests.
3. I've used ddt to make it easier to implement the unit tests.
4. To keep memory footprint low, I've limited the number of diff sessions to 16, which are kept during the lifetime of
the web application process. To use a 17th session, one of the other 16 must be used instead.
5. All data must be entered in a JSON structure like this:


    {
        "data": "<your data goes here"
    }