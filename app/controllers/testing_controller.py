# Do not modify this used only for testing purposes to render templates
from flask import Blueprint, render_template


# Do not modify this used only for testing purposes to render templates
testing_blueprint = Blueprint('testing_blueprint', __name__)


# Do not modify this used only for testing purposes to render templates
@testing_blueprint.route('/testing/template')
def testingTemplate():

    # Enter your file path in render_template
    return render_template('path/to/your/file')