from flask import Flask, request, render_template, redirect, url_for
from flask import jsonify, abort, make_response
from forms import ItemForm
from models import items
from app import app

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

    form = ItemForm(data=item_dict)

    if request.method == "POST":
        if form.validate_on_submit():
            items.update(item, tuple(form.data.values())[:4])
        return redirect(url_for("items_list"))
    return render_template("item.html", form=form, item_id=item_id)


@app.route("/items/<int:item_id>", methods=['DELETE'])
def delete_item(conn, item_id):
    if request.form.get('delete_checkbox') == '1':
        if request.get('submit'):
            print("TEST")
    #         with conn:
    #             result = items.delete(conn, item_id)
    #             if not result:
    #                 abort(404)
    # return jsonify({'result': result})


if __name__ == "__main__":

    app.run(debug=True)

