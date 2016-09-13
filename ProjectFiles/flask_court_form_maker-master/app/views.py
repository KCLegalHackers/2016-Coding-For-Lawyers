from flask import render_template, flash, redirect, url_for, session, Markup, request, g
from app import app

from .forms import InputForm




print "Top of Views"
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  print "Top of index"
  form = InputForm()
  if form.validate_on_submit():
      session['respondent'] = form.respondent._value()
      session['petitioner'] = form.petitioner._value()
      

      return redirect(url_for('results'))

  return render_template('index.html',
                           title='Court Form Sample',
                           form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
  
  respondent = session['respondent']
  print "Petitioner = %s" % session['petitioner']
  petitioner = session['petitioner']
  
  

  return render_template('results.html',
                          title='Court Form Sample', 
                          petitioner=petitioner, 
                          respondent=respondent
                          )


    
#Error Handling:
    
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500
    

