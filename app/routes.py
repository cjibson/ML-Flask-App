#This file defines the routes for the application
from flask import Blueprint, render_template, url_for, app

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/lung_cancer_analysis')
def lung_cancer_analysis():
    # Render the HTML template for your analysis
    return render_template('lung_cancer_analysis.html')