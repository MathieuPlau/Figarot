from flask import Blueprint, render_template, request
from app.fichiers import parse_directory

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/sounds')
def sounds():
    directory_path = request.args.get('dir', '.')  # default to current directory
    directory_contents = parse_directory(directory_path)
    return render_template('sounds.html', directory_contents=directory_contents, directory_path=directory_path)