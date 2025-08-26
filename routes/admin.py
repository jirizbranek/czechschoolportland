from flask import Blueprint, render_template, request, redirect, url_for
from models.db import get_all_events, get_mailing_list, add_event, delete_event, delete_email, get_event_by_id, update_event

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def admin_home():
    return render_template("admin_dashboard.html")

@admin_bp.route("/events", methods=["GET", "POST"])
def manage_events():
    events = get_all_events()
    return render_template("admin_events.html", events=events)

@admin_bp.route("/events/add", methods=["GET", "POST"])
def add_event_form():
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        description = request.form["description"]
        location = request.form.get("location")
        time = request.form.get("time")
        invitation_link = request.form.get("invitation_link")
        add_event(title, date, description, location, time, invitation_link)
        return redirect(url_for('admin.manage_events'))
    
    return render_template("admin_event_form.html")

@admin_bp.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event_form(event_id):
    if request.method == "POST":
        if "delete_event" in request.form:
            delete_event(event_id)
            return redirect(url_for('admin.manage_events'))
        elif "update_event" in request.form:
            title = request.form["title"]
            date = request.form["date"]
            description = request.form["description"]
            location = request.form.get("location")
            time = request.form.get("time")
            invitation_link = request.form.get("invitation_link")
            update_event(event_id, title, date, description, location, time, invitation_link)
            return redirect(url_for('admin.manage_events'))
    
    event = get_event_by_id(event_id)
    if not event:
        return redirect(url_for('admin.manage_events'))
    
    return render_template("admin_event_form.html", event=event)

@admin_bp.route("/mailing", methods=["GET", "POST"])
def manage_mailing():
    if request.method == "POST":
        if "delete_email" in request.form:
            email_id = request.form["delete_email"]
            delete_email(email_id)
        return redirect(url_for('admin.manage_mailing'))
    
    mailing_list = get_mailing_list()
    return render_template("admin_mailing.html", mailing_list=mailing_list)
