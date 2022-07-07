# Dashboard webapp application for GECKO project.
# Author: A.C. van Rijswijk
# Date: 2-3-2020/

"""
This Flask webapp application loads generated cancer gene expression data.
On generated data filter options are available to make multiple visualisations and tables.
"""

# <==================================================================================>
#                                     Start script
# <==================================================================================>

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/charts', methods=['GET', 'POST'])
def handle_charts():
    return render_template('charts.html')

@app.route('/tables', methods=['GET', 'POST'])
def hanlde_tables():
    return render_template('tables.html')





# Static returns
@app.route('/introduction', methods=['GET', 'POST'])
def handle_introduction():
    return render_template('about_templates/introduction.html')

@app.route('/people', methods=['GET', 'POST'])
def handle_people():
    return render_template('about_templates/people.html')

@app.route('/admin_settings', methods=['GET', 'POST'])
def handle_admin_settins():
    """
    admin_settings checks if current user is admin.
    If admin return settings page, else return 401 error unauthorized.
    :return: Error_401.html or settings page.
    """
    # Check if admin is logged in
    # else
    user = 'Elco'
    error = '<p> User {} is not authorized to acces settings</p>'.format(user)
    return render_template('error_templates/error_401.html', error_message=error)


@app.errorhandler(404)
def handle_404_error(error):
    """
    error_handler catches an unexpexted 404 url not found error.
    :param error: Error message that gets displayed on error_404.html.
    :return: The 404.html template containing the error message.
    """
    return render_template('error_templates/error_404.html', error_message=error)



@app.errorhandler(Exception)
def handle_error(error):
    """
    handle_error cathes any error and returnes a static HTML page with corresponding error message.
    :param error: Error message that gets displayed on error.html.
    :return: The error.html template containing the error message.
    """
    return render_template('error_templates/error.html', error_message=error)


if __name__ == '__main__':
    app.run()
