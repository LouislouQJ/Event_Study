from flask import render_template, Flask, url_for
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from support_functions import initialization

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "temp_passwd"


class NameForm(FlaskForm):
    name = StringField("Which single stock do you want to check?", validators=[DataRequired()])
    submit = SubmitField("Submit")


stock_dict, group_dict = initialization()


@app.route('/', methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        target = form.name.data
        if target in stock_dict:
            temp = stock_dict[target]
            temp.return_plot()
            return render_template('stock.html', title=target, group=temp.stock_class, est_eps=temp.est_EPS,
                                   act_eps=temp.act_EPS, fig="/static/%s.png" % target)
    return render_template("index.html", form=form)


@app.route('/group_miss')
def group_miss():
    return render_template('group.html', title='Miss', stock_list=group_dict["Miss"].get_stocklist(),
                           fig="/static/Miss.png")


@app.route('/group_meet')
def group_meet():
    return render_template('group.html', title='Meet', stock_list=group_dict["Meet"].get_stocklist(),
                           fig="/static/Meet2.png")


@app.route('/group_beat')
def group_beat():
    return render_template('group.html', title='Beat', stock_list=group_dict["Beat"].get_stocklist(),
                           fig="/static/Beat2.png")


@app.route('/detail')
def detail():
    return render_template('detail.html')


if __name__ == "__main__":
    app.run()
