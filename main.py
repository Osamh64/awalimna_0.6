from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, UserMixin
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import jwt_required
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from awallimna.model.user import Reader, Writer, Reader_Admin, Reader_SuperAdmin, Writer_Admin, Writer_SuperAdmin, Center, Teacher, Student, Owner

Awallimna = Flask(__name__, template_folder="templates", static_folder="static", methods=["GET", "POST"])
Awallimna.secret_key = 'your_secret_key'  # يجب تغييره في الإنتاج
db = SQLAlchemy(Awallimna)
migrate = Migrate(Awallimna, db)
bcrypt = Bcrypt(Awallimna)
mail = Mail(Awallimna)
csrf = CSRFProtect(Awallimna)
cache = Cache(Awallimna)
jwt = JWTManager(Awallimna)
Awallimna.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/awallimna'


# إعداد Swagger ليكون على /apidocs/
swagger = Swagger(Awallimna, template={
    "swagger": "2.0",
    "info": {
        "title": "Awallimna API Documentation",
        "description": "توثيق API الخاصة بمنصة أوالمنا باستخدام Swagger UI. فقط المسارات التي تبدأ بـ /api/ تظهر هنا.",
        "version": "0.0.5"
    },
    "basePath": "/"
}, config={
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: rule.rule.startswith('/api/'),  # فقط API تبدأ بـ /api/
            'model_filter': lambda tag: True,
        }
    ],
    'specs_route': '/apidocs/',
    'headers': []
})

login_manager = LoginManager()
login_manager.init_app(Awallimna)
login_manager.login_view = 'login'

# تصميم login_manager.user_loader للقارئ والكاتب و مشرف لقارئ ومشرف للكاتب و مشرف عالي للقاري و مشرف عالي للقاري و مركز تعليمي و معلم مركز تعليمي و طالب مركز تعليمي و مالك
@login_manager.user_loader
def load_user(user_id):
    user = Reader.query.get(user_id) # قارئ
    if user:
        return user
    user = Writer.query.get(user_id) # كاتب
    if user:
        return user
    user = Reader_Admin.query.get(user_id) # مشرف لقارئ
    if user:
        return user
    user = Reader_SuperAdmin.query.get(user_id) # مشرف للكاتب
    if user:
        return user
    user = Writer_Admin.query.get(user_id) # مشرف عالي للكاتب
    if user:
        return user
    user = Writer_SuperAdmin.query.get(user_id) # مشرف عالي للكاتب
    if user:
        return user
    user = Center.query.get(user_id) # مركز تعليمي
    if user:
        return user
    user = Teacher.query.get(user_id) # معلم مركز تعليمي
    if user:
        return user
    user = Student.query.get(user_id) # طالب مركز تعليمي
    if user:
        return user
    user = Owner.query.get(user_id) # مالك
    return None

# إضافة context processor لتمرير user=None لجميع القوالب
@Awallimna.context_processor
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

# كل صفحات المزقع و رابط لهن
@Awallimna.get("/", methods=["GET", "POST"])
def paths():
    # توليد قائمة بالروابط لكل صفحة
    links = []
    for page in pages:
        # إزالة .html للحصول على اسم المسار
        route = page.replace('.html', '')
        # بعض الصفحات مثل index قد تكون مختلفة، هنا نفترض أن اسم المسار هو اسم الملف بدون .html
        links.append(f'<li><a href="/{route}">{page}</a></li>')
    # بناء HTML بسيط
    html = f"""
    <html>
    <head><title>جميع صفحات الموقع</title></head>
    <body>
        <h1>جميع صفحات الموقع وروابطها</h1>
        <ul>
            {''.join(links)}
        </ul>
    </body>
    </html>
    """
    return html

@Awallimna.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", methods=["GET", "POST"])
        password = request.form.get("password", methods=["GET", "POST"])
        # تحقق من صحة البيانات
        user = Reader.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('reader_profile'))
        else:
            flash("البريد الإلكتروني أو كلمة المرور غير صحيحة", "danger", methods=["GET", "POST"])
    return render_template("login.html")

@Awallimna.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@Awallimna.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# حماية صفحة الملف الشخصي
@Awallimna.route("/reader_profile", methods=["GET", "POST"])
def reader_profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("reader_profile.html", user=session['user'])

# إنشاء route ودالة منفصلة لكل صفحة HTML فقط بدون توثيق Swagger
@Awallimna.route("/accept_educational_center", methods=["GET", "POST"])
def accept_educational_center():
    return render_template("accept_educational_center.html")

@Awallimna.route("/adventure", methods=["GET", "POST"])
def adventure():
    return render_template("adventure.html")

@Awallimna.route("/center_profile", methods=["GET", "POST"])
def center_profile():
    return render_template("center_profile.html")

@Awallimna.route("/children", methods=["GET", "POST"])
def children():
    return render_template("children.html")

@Awallimna.route("/comedy", methods=["GET", "POST"])
def comedy():
    return render_template("comedy.html")

@Awallimna.route("/confirmation_sent_email", methods=["GET", "POST"])
def confirmation_sent_email():
    return render_template("confirmation_sent_email.html")

@Awallimna.route("/create_center_account", methods=["GET", "POST"])
def create_center_account():
    return render_template("create_center_account.html")

@Awallimna.route("/crime_investigation", methods=["GET", "POST"])
def crime_investigation():
    return render_template("crime_investigation.html")

@Awallimna.route("/deleted_confirmation", methods=["GET", "POST"])
def deleted_confirmation():
    return render_template("deleted_confirmation.html")

@Awallimna.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    return render_template("delete_account.html")

@Awallimna.route("/drama", methods=["GET", "POST"])
def drama():
    return render_template("drama.html")

@Awallimna.route("/fantasy", methods=["GET", "POST"])
def fantasy():
    return render_template("fantasy.html")

@Awallimna.route("/fiction", methods=["GET", "POST"])
def fiction():
    return render_template("fiction.html")

@Awallimna.route("/historic", methods=["GET", "POST"])
def historic():
    return render_template("historic.html")

@Awallimna.route("/historical", methods=["GET", "POST"])
def historical():
    return render_template("historical.html")

@Awallimna.route("/horror", methods=["GET", "POST"])
def horror():
    return render_template("horror.html")

@Awallimna.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    return render_template("reset_password.html")

@Awallimna.route("/romance", methods=["GET", "POST"])
def romance():
    return render_template("romance.html")

@Awallimna.route("/science_fiction", methods=["GET", "POST"])
def science_fiction():
    return render_template("science_fiction.html")

@Awallimna.route("/statistics", methods=["GET", "POST"])
def statistics():
    return render_template("statistics.html")

@Awallimna.route("/subscriptions", methods=["GET", "POST"])
def subscriptions():
    return render_template("subscriptions.html")

@Awallimna.route("/terms_conditions", methods=["GET", "POST"])
def terms_conditions():
    return render_template("terms_conditions.html")

@Awallimna.route("/theft", methods=["GET", "POST"])
def theft():
    return render_template("theft.html")

@Awallimna.route("/war", methods=["GET", "POST"])
def war():
    return render_template("war.html")

@Awallimna.route("/writer_profile", methods=["GET", "POST"])
def writer_profile():
    return render_template("writer_profile.html")

@Awallimna.route("/write_story", methods=["GET", "POST"])
def write_story():
    return render_template("write_story.html")

@Awallimna.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    return render_template("forgot_password.html")

@Awallimna.route("/review_story", methods=["GET", "POST"])
def review_story():
    return render_template("review_story.html")

@Awallimna.route("/admin_page", methods=["GET", "POST"])
def admin_page():
    return render_template("admin_page.html")

@Awallimna.route("/story_functions", methods=["GET", "POST"])
def story_functions():
    return render_template("story_functions.html")

@Awallimna.route("/website", methods=["GET", "POST"])
def website():
    return render_template("website.html")

@Awallimna.route("/header", methods=["GET", "POST"])
def header():
    return render_template("header.html")

@Awallimna.route("/footer", methods=["GET", "POST"])
def footer():
    return render_template("footer.html")

@Awallimna.route("/patha", methods=["GET", "POST"])
def patha():
    return render_template("patha.html")

@Awallimna.route("/read_story", methods=["GET", "POST"])
def read_story():
    return render_template("read_story.html")

@Awallimna.route("/teacher_accounts", methods=["GET", "POST"])
def teacher_accounts():
    return render_template("teacher_accounts.html")

@Awallimna.route("/sent_educational_center", methods=["GET", "POST"])
def sent_educational_center():
    return render_template("sent_educational_center.html")

@Awallimna.route("/update_story_status", methods=["GET", "POST"])
def update_story_status():
    return render_template("update_story_status.html")

@Awallimna.route("/register_center", methods=["GET", "POST"])
def register_center():
    return render_template("register_center.html")

@Awallimna.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html", methods=["GET", "POST"])

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    Awallimna.run(
        host=host,
        port=port,
        debug=True,
        use_debugger=True,
        threaded=True,
        ssl_context=('cert.pem', 'key.pem')
    )