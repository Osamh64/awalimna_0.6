from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="templates")

# إضافة context processor لتمرير user=None لجميع القوالب
@app.context_processor
def inject_user():
    return dict(user=None)

# صفحات HTML في مجلد templates
# تم تجاهل ملفات .py وأخذ فقط ملفات .html
pages = [
    "accept_educational_center.html",
    "adventure.html",
    "center_profile.html",
    "children.html",
    "comedy.html",
    "confirmation_sent_email.html",
    "create_center_account.html",
    "crime_investigation.html",
    "deleted_confirmation.html",
    "delete_account.html",
    "drama.html",
    "fantasy.html",
    "fiction.html",
    "historic.html",
    "historical.html",
    "horror.html",
    "reader_profile.html",
    "reset_password.html",
    "romance.html",
    "science_fiction.html",
    "statistics.html",
    "subscriptions.html",
    "terms_conditions.html",
    "theft.html",
    "war.html",
    "writer_profile.html",
    "write_story.html",
    "forgot_password.html",
    "review_story.html",
    "admin_page.html",
    "login.html",
    "story_functions.html",
    "website.html",
    "header.html",
    "footer.html",
    "patha.html",
    "read_story.html",
    "teacher_accounts.html",
    "sent_educational_center.html",
    "update_story_status.html",
    "register_center.html",
    "register.html"
]

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("website.html")

# إنشاء route ودالة منفصلة لكل صفحة
@app.route("/accept_educational_center")
def accept_educational_center():
    return render_template("accept_educational_center.html")

@app.route("/adventure")
def adventure():
    return render_template("adventure.html")

@app.route("/center_profile")
def center_profile():
    return render_template("center_profile.html")

@app.route("/children")
def children():
    return render_template("children.html")

@app.route("/comedy")
def comedy():
    return render_template("comedy.html")

@app.route("/confirmation_sent_email")
def confirmation_sent_email():
    return render_template("confirmation_sent_email.html")

@app.route("/create_center_account")
def create_center_account():
    return render_template("create_center_account.html")

@app.route("/crime_investigation")
def crime_investigation():
    return render_template("crime_investigation.html")

@app.route("/deleted_confirmation")
def deleted_confirmation():
    return render_template("deleted_confirmation.html")

@app.route("/delete_account")
def delete_account():
    return render_template("delete_account.html")

@app.route("/drama")
def drama():
    return render_template("drama.html")

@app.route("/fantasy")
def fantasy():
    return render_template("fantasy.html")

@app.route("/fiction")
def fiction():
    return render_template("fiction.html")

@app.route("/historic")
def historic():
    return render_template("historic.html")

@app.route("/historical")
def historical():
    return render_template("historical.html")

@app.route("/horror")
def horror():
    return render_template("horror.html")

@app.route("/reader_profile")
def reader_profile():
    return render_template("reader_profile.html")

@app.route("/reset_password")
def reset_password():
    return render_template("reset_password.html")

@app.route("/romance")
def romance():
    return render_template("romance.html")

@app.route("/science_fiction")
def science_fiction():
    return render_template("science_fiction.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/subscriptions")
def subscriptions():
    return render_template("subscriptions.html")

@app.route("/terms_conditions")
def terms_conditions():
    return render_template("terms_conditions.html")

@app.route("/theft")
def theft():
    return render_template("theft.html")

@app.route("/war")
def war():
    return render_template("war.html")

@app.route("/writer_profile")
def writer_profile():
    return render_template("writer_profile.html")

@app.route("/write_story")
def write_story():
    return render_template("write_story.html")

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/review_story")
def review_story():
    return render_template("review_story.html")

@app.route("/admin_page")
def admin_page():
    return render_template("admin_page.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/story_functions")
def story_functions():
    return render_template("story_functions.html")

@app.route("/website")
def website():
    return render_template("website.html")

@app.route("/header")
def header():
    return render_template("header.html")

@app.route("/footer")
def footer():
    return render_template("footer.html")

@app.route("/patha")
def patha():
    return render_template("patha.html")

@app.route("/read_story")
def read_story():
    return render_template("read_story.html")

@app.route("/teacher_accounts")
def teacher_accounts():
    return render_template("teacher_accounts.html")

@app.route("/sent_educational_center")
def sent_educational_center():
    return render_template("sent_educational_center.html")

@app.route("/update_story_status")
def update_story_status():
    return render_template("update_story_status.html")

@app.route("/register_center")
def register_center():
    return render_template("register_center.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
