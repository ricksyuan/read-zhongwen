Read Zhongwen
-------------

[Live Site](https://www.readzhongwen.com)


Read Zhongwen allows the user to improve their Mandarin reading skills by copying and pasting text into the service, which then automatically provides dictionary looks for all phrases. Works for either simplified or traditional Mandarin.

Technologies
------------

Read Zhongwen uses a simple Flask web service deployed using AWS Elastic Beanstalk.

Files
-----

* requirements.txt - this file is used to install Python dependencies needed by
  the Flask application
* application.py - this file contains the Flask application
* flaskrun.py - this file contains a CLI wrapper that passes
  options to the Flask application
* .ebextensions/ - this directory contains the configuration files that allow
  AWS Elastic Beanstalk to deploy the application

Steps to Run the Project Locally
--------------------------------

1. Create a Python virtual environment for the Flask project. At the terminal, type the following command:

        $ virtualenv .venv

2. Activate the virtual environment:

        $ source ./.venv/bin/activate

3. Install Python dependencies for this project:

        $ pip3 install -r requirements.txt

4. Create searches database:

        $ python3 createdb_searches.py

5. Start the Flask development server:

        $ python3 application.py --port 8000

6. Open http://127.0.0.1:8000/ in a web browser to view the output of your
   service.

Deploying to Elastic Beanstalk
----------------------------------
Install the Elastic Beanstalk CLI using Homebrew and configure with proper credentials. Create Elastic Beanstalk files for the repository using the following terminal command:

        $ eb init

Finally, automatically package the repo and upload:

        $ eb deploy

The changes should be immediately live!