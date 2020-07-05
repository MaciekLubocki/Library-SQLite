from flask import request, render_template, redirect, url_for
from forms import ItemForm
from models import items
from app import app
import sqlite3

app.config["SECRET_KEY"] = "nasturcja"


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("items_list"))


@app.route("/items/", methods=["GET", "POST"])
def items_list():
    form = ItemForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            items.create((tuple(form.data.values())[:4]))
    return render_template("items.html", form=form, items=items.all(), error=error)  # noqa


@app.route("/item/<int:item_id>/", methods=["GET", "POST"])
def item_details(item_id):
    item = items.get(item_id)

    item_dict = {
        'media': item[1],
        'title': item[2],
        'author': item[3],
        'year': item[4]
    }

    conn = sqlite3.connect('multimedia.db')
    form = ItemForm(data=item_dict)
    checked = request.form.get("delete_checkbox")
    if request.method == "POST":
        if form.validate_on_submit():
            if checked is None:
                items.update(item, tuple(form.data.values())[:4])
                print('status UPDATE: ', checked, item_id, conn)
            elif checked == '1':
                items.delete(conn, item_id)
                print('status: ', checked, item_id, conn)
        return redirect(url_for("items_list"))
    return render_template("item.html", form=form, item_id=item_id)


if __name__ == "__main__":

    app.run(debug=True)
