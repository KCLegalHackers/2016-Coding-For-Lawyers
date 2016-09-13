from flask import flash, Markup
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired

class InputForm(Form):
  respondent = StringField('respondent', validators=[DataRequired()])
  petitioner = StringField('petitioner', validators=[DataRequired()])
  

  

  def validate(self):
    if not Form.validate(self):
      #print "not form validate"
      if "<" in self.respondent.data or \
        "<" in self.petitioner.data:
        info = Markup("<img src='/static/hackers.jpg'>")
        flash(info)
        return False
      elif self.respondent or \
        self.petitioner.data or \
        self.respondent.data:
                
        return True
            #print "Should return False"
      info = Markup('<h2 style="color:red"> Must complete all fields </h2>')
      flash(info)
      return False
    return True
        
