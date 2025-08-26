from flask import Blueprint, render_template, request, redirect, url_for
from models.db import get_next_event, get_all_events, add_email, email_exists, unsubscribe_email

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    next_event = get_next_event()
    return render_template("home.html", next_event=next_event)

@main_bp.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    if email:
        if email_exists(email):
            # Email already exists, offer to unsubscribe
            return render_template("subscription_check.html", email=email, already_subscribed=True)
        else:
            # Email doesn't exist, show subscription confirmation
            return render_template("subscription_check.html", email=email, already_subscribed=False)
    return redirect(url_for("main.home"))

@main_bp.route("/confirm_subscription", methods=["POST"])
def confirm_subscription():
    email = request.form.get("email")
    if email:
        add_email(email)
        return render_template("subscription_result.html", email=email, action="subscribed")
    return redirect(url_for("main.home"))

@main_bp.route("/confirm_unsubscribe", methods=["POST"])
def confirm_unsubscribe():
    email = request.form.get("email")
    if email:
        if unsubscribe_email(email):
            return render_template("subscription_result.html", email=email, action="unsubscribed")
        else:
            return render_template("subscription_result.html", email=email, action="not_found")
    return redirect(url_for("main.home"))

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/classes")
def classes():
    return render_template("classes.html")

@main_bp.route("/teachers")
def teachers():
    return render_template("teachers.html")

@main_bp.route("/calendar")
def calendar():
    events = get_all_events()
    return render_template("calendar.html", events=events)
