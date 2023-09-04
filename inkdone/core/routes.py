from flask import render_template, request, Blueprint
from inkdone import db
from inkdone.users.models import User


core = Blueprint('core', __name__)


@core.route('/')
@core.route('/home')
def home():
    return render_template('home.html')


@core.route('/about')
def about():
    return render_template('about.html')


@core.route('/search')
def search():
    query = request.args.get('query', '')
    results = ''
    page = request.args.get('page', 1)
    per_page = 1
    if query != '':
        results = User.query.filter(
            db.or_(
                User.username.icontains(query), 
                User.bio.icontains(query), 
                User.academics.icontains(query))).paginate(
                    page=int(page), 
                    per_page=per_page
                    )
    return render_template(
        'search.html', 
        results=results, 
        query=query
        )