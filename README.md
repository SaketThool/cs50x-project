# CS50x-project: Cricket Worldcup Winners(Men's/Women's)
My final project for the CS50x course.

### Video Demo: https://youtu.be/pwE1-y-O5Xc


# How to run program
* Run program: `$ flask run`

# What My Program Does
* My project is a web applicationthat displays information about Cricket World Cup winners for both Men's and Women's tournaments. It allows users to:

  * View a list of winners, runner-ups, hosts, and other details for each year of the Cricket World Cup.

  * Navigate to detailed pages for specific years to see additional information such as the final score, top scorer, and most wickets.

  * Switch between the Men's and Women's World Cup data using a navigation menu.

* The application is built using Flask, and it dynamically loads data from CSV files (worldcups.csv for Men's and womens_worldcups.csv for Women's). It uses templates to render the data in a user-friendly format.

# How Does It Work
* My project works as following things:

  * Data Loading: The application reads data from two CSV files: worldcups.csv for Men's World Cup data and womens_worldcups.csv for Women's World Cup data.

  * Flask Framework: The application is built using Flask, a lightweight Python web framework.

  * Routes: The application defines routes for the home page (/), the Women's World Cup page (/women), and detailed pages for specific years (/year/<int:year> for Men's and /women/year/<int:year> for Women's).

  * Templates: The application uses Jinja2 templates to render HTML pages dynamically.

  * Dynamic Pages: Users can view a list of World Cup winners on the main pages for Men's and Women's tournaments.

  * Web Server: The application runs a local web server using Flask.

* This combination of Flask, dynamic routing, and templates makes the application interactive and easy to use.

## File Descriptions
* `README.md`: In this I Write about my project what my program does and how does it work.

* `data` : This directory contains the CSV files used by the application to store information about Cricket World Cup winners.

  * `worldcups.csv`: Contains data for the Men's Cricket World Cup, including year, winner, runner-up, host, final score, top scorer, and most wickets.

  * `womens_worldcups.csv`: Contains similar data for the Women's Cricket World Cup.

* `templates` : This directory contains the HTML templates used to render the web pages dynamically.
  * `layout.html`: The base template that provides a consistent structure for all pages, including the navigation menu.

  * `index.html`: Displays the list of Men's Cricket World Cup winners.

  * `women_index.html`: Displays the list of Women's Cricket World Cup winners. 

  * `details.html`: Displays detailed information about a specific year's World Cup for both Men's and Women's tournaments.

* `app.py` : The main Python file that runs the Flask application.