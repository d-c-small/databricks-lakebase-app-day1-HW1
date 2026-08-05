import os
from datetime import datetime
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from crud import (
    add_message_to_ticket,
    create_ticket,
    delete_ticket,
    get_all_tickets,
    get_messages_for_ticket,
    get_ticket_by_id,
    get_ticket_stats,
    update_ticket_status,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)

VALID_STATUSES = ("open", "in_progress", "resolved")


@app.template_filter("datetimeformat")
def datetimeformat(value, fmt="%b %d, %Y %I:%M %p"):
    return value.strftime(fmt) if isinstance(value, datetime) else value


@app.route("/")
def index():
    status_filter = request.args.get("status")
    if status_filter not in VALID_STATUSES:
        status_filter = None
    tickets = get_all_tickets(status_filter=status_filter)
    stats = get_ticket_stats()
    return render_template(
        "index.html",
        tickets=tickets,
        stats=stats,
        status_filter=status_filter,
        valid_statuses=VALID_STATUSES,
    )


@app.route("/ticket/<int:ticket_id>")
def view_ticket(ticket_id):
    ticket = get_ticket_by_id(ticket_id)
    if ticket is None:
        abort(404)
    messages = get_messages_for_ticket(ticket_id)
    return render_template(
        "ticket.html",
        ticket=ticket,
        messages=messages,
        valid_statuses=VALID_STATUSES,
    )


@app.route("/new-ticket", methods=["GET", "POST"])
def new_ticket():
    form_data = {"title": "", "created_by": ""}
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        created_by = request.form.get("created_by", "").strip()
        form_data = {"title": title, "created_by": created_by}
        if not title:
            flash("Title is required.", "danger")
        elif not created_by:
            flash("Your name is required.", "danger")
        elif len(title) > 200:
            flash("Title must be 200 characters or fewer.", "danger")
        else:
            new_id = create_ticket(title, created_by)
            flash(f"Ticket #{new_id} created successfully.", "success")
            return redirect(url_for("view_ticket", ticket_id=new_id))
    return render_template("new_ticket.html", form_data=form_data)


@app.route("/ticket/<int:ticket_id>/add-message", methods=["POST"])
def add_message(ticket_id):
    if get_ticket_by_id(ticket_id) is None:
        abort(404)
    message_text = request.form.get("message_text", "").strip()
    author = request.form.get("author", "").strip()
    if not message_text:
        flash("Message text is required.", "danger")
    elif not author:
        flash("Your name is required.", "danger")
    elif len(message_text) > 2000:
        flash("Message must be 2,000 characters or fewer.", "danger")
    else:
        add_message_to_ticket(ticket_id, message_text, author)
        flash("Message added successfully.", "success")
    return redirect(url_for("view_ticket", ticket_id=ticket_id))


@app.route("/ticket/<int:ticket_id>/update-status", methods=["POST"])
def update_status(ticket_id):
    if get_ticket_by_id(ticket_id) is None:
        abort(404)
    new_status = request.form.get("status", "").strip()
    if new_status not in VALID_STATUSES:
        flash("Invalid status value.", "danger")
    else:
        update_ticket_status(ticket_id, new_status)
        flash("Status updated successfully.", "success")
    return redirect(url_for("view_ticket", ticket_id=ticket_id))


@app.route("/ticket/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket_route(ticket_id):
    ticket = get_ticket_by_id(ticket_id)
    if ticket is None:
        abort(404)
    delete_ticket(ticket_id)
    flash(f"Ticket \"{ticket['title']}\" has been deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False,
    )
