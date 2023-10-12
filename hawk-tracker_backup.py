import os

# import time
import datetime
from datetime import datetime

from enum import Enum

import secrets
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Column, Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Sequence
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    render_template,
    request,
    session,
    jsonify,
    redirect,
    url_for,
    send_file,
)
from werkzeug.utils import secure_filename

# from sqlalchemy.exc import SQLAlchemyError
# from json import JSONDecodeError
import pytz
from config import (
    ADMIN_PASSWORD,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
    # DEV_DB_NAME,
    # DEV_DB_USER,
    # FLASK_ENV,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
# if FLASK_ENV == "development":
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"
#     ] = f"postgresql://{DEV_DB_USER}:{DB_PASSWORD}@localhost:5432/{DEV_DB_NAME}"
# else:
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"
#     ] = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"


# Initialize SQLAlchemy
db = SQLAlchemy(app)

app.config["TIMEZONE"] = pytz.timezone("Asia/Kuala_Lumpur")

app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
# app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")



class PriorityLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


Base = declarative_base()


class Status(Enum):
    OPEN = "OPEN"
    DEVELOPING = "DEVELOPING"
    CLOSED = "CLOSED"


#############################################################
# attempt to declare int Status
# class Status:
#     OPEN = 1
#     DEVELOPING = 2
#     CLOSED = 3

#     @classmethod
#     def choices(cls):
#         return [
#             (cls.OPEN, "Open"),
#             (cls.DEVELOPING, "Developing"),
#             (cls.CLOSED, "Closed"),
#         ]
###############################################################


class Request(db.Model):
    __tablename__ = "issue"
    __table_args__ = {"schema": "hawktracker"}

    # Define the primary key as an auto-incrementing column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # urgency = db.Column(db.Enum(PriorityLevel), nullable=False)
    urgency = Column(SQLAEnum(PriorityLevel, name="priority_lvl"), nullable=False)
    tags = db.Column(db.ARRAY(db.Text))
    date_posted = db.Column(db.Date, default=lambda: datetime.now().date())
    issue = db.Column(db.Text)
    email = db.Column(db.Text)
    remarks = db.Column(db.Text)
    date_updated = db.Column(db.Date)
    status = db.Column(SQLAEnum(Status), default=Status.OPEN)
    # status = db.Column(db.Integer, nullable=False, default=Status.OPEN)
    expected_completion = db.Column(db.Date)
    comments = db.relationship(
        "Comment", backref="request"
    )  # "Comment" entity will have a reference attribute named "request" that points back to the parent "request" entity.

    def __repr__(self):
        return f"<Request(id={self.id}, issue='{self.issue}')>"


class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {"schema": "hawktracker"}

    id_comment = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(
        db.Integer, db.ForeignKey("hawktracker.issue.id"), nullable=False
    )
    date_posted = db.Column(db.Date, nullable=False)
    email = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    remarks = db.Column(db.Text)
    image_paths = db.Column(db.ARRAY(db.Text))

    def __repr__(self):
        return f"<Comment(id={self.id_comment}, issue='{self.issue}')>"


# Function to disable caching for all responses
def disable_caching(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# Route to handle the admin login
@app.route("/admin_login", methods=["POST"])
def admin_login():
    # Get the password from the request
    password = request.form.get("password")

    # Verify the password (you can use any method for password verification)
    if password == ADMIN_PASSWORD:
        # Set the 'admin_logged_in' session variable to True
        session["admin_logged_in"] = True
        return jsonify(success=True)
        # return jsonify(success=True)
    else:
        return jsonify(success=False, message="Incorrect password"), 500

    # Route to handle updating the issue data (protected with admin password)


# @app.route("/update_issue", methods=["POST"])
# def update_issue():
#     # Check if the admin is logged in
#     if session.get("admin_logged_in"):
#         try:
#             data = request.get_json()

#             for item in data:
#                 request_id = item["id"]
#                 remarks_new = item["remarks"]
#                 status_new = Status[item["status"]]  # Convert string to Status enum
#                 urgency_new = PriorityLevel[
#                     item["urgency"]
#                 ]  # Convert string to Status enum
#                 date_updated_str = item[
#                     "date_updated"
#                 ]  # ISO 8601 formatted date string
#                 date_updated = datetime.fromisoformat(
#                     date_updated_str
#                 )  # Convert to datetime object
#                 expected_completion_str = item["expected_completion"]
#                 expected_completion = datetime.fromisoformat(expected_completion_str)

#                 # Update column in the database based on the id
#                 request_row = Request.query.get(request_id)
#                 request_row.remarks = remarks_new
#                 request_row.status = status_new.value
#                 request_row.urgency = urgency_new.value
#                 request_row.date_updated = date_updated  # Assign the datetime object
#                 request_row.expected_completion = expected_completion

#                 for comment_data in item["comments"]:
#                     comment_id = comment_data["id"]
#                     comment_issue = comment_data["issue"]
#                     comment_remarks = comment_data["remarks"]

#                     if comment_id:  # If comment ID exists, update or delete
#                         comment = Comment.query.get(comment_id)
#                         if comment:
#                             if comment_issue:
#                                 comment.issue = comment_issue
#                             if comment_remarks:
#                                 comment.remarks = comment_remarks
#                         else:
#                             # Delete the comment if it's not found
#                             db.session.query(Comment).filter_by(
#                                 id_comment=comment_id
#                             ).delete()
#                     else:  # If comment ID doesn't exist, create a new comment
#                         new_comment = Comment(issue_id=request_id,issue=comment_issue,remarks=comment_remarks,)
#                         db.session.add(new_comment)

#                 db.session.commit()

#             return jsonify(success=True)
#         # except SQLAlchemyError as e:  # Catch specific AQLAlchemy errors
#         #     db.session.rollback()  # Rollback changes in case of an error
#         #     return jsonify(success=False, message="commit changes error")
#         # except JSONDecodeError:  # Catch specific JSON decode errors
#         #     return jsonify(success=False, message="Invalid JSON data format")
#         except Exception as e:
#             return jsonify(success=False, message="Error in commit"), 500
#     else:
#         return jsonify(success=False, message="Unauthorized"), 500


@app.route("/update_issue_only", methods=["POST"])
def update_issue_only():
    # Check if the admin is logged in
    if session.get("admin_logged_in"):
        try:
            data = request.get_json()

            for item in data:
                request_id = item["id"]
                remarks_new = item["remarks"]
                status_new = Status[item["status"]]  # Convert string to Status enum
                urgency_new = PriorityLevel[
                    item["urgency"]
                ]  # Convert string to Status enum
                date_updated_str = item[
                    "date_updated"
                ]  # ISO 8601 formatted date string
                date_updated = datetime.fromisoformat(
                    date_updated_str
                )  # Convert to datetime object
                expected_completion_str = item["expected_completion"]
                expected_completion = datetime.fromisoformat(expected_completion_str)

                tags_new = item.get("tag", [])

                # Update column in the database based on the id
                request_row = Request.query.get(request_id)
                request_row.remarks = remarks_new
                request_row.status = status_new.value
                request_row.urgency = urgency_new.value
                request_row.date_updated = date_updated  # Assign the datetime object
                request_row.expected_completion = expected_completion
                # Update the "tags" column
                request_row.tags = tags_new

                db.session.commit()

            return jsonify(success=True)
        # except SQLAlchemyError as e:  # Catch specific AQLAlchemy errors
        #     db.session.rollback()  # Rollback changes in case of an error
        #     return jsonify(success=False, message="commit changes error")
        # except JSONDecodeError:  # Catch specific JSON decode errors
        #     return jsonify(success=False, message="Invalid JSON data format")
        except Exception as e:
            return jsonify(success=False, message="Error in commit"), 500
    else:
        return jsonify(success=False, message="Unauthorized"), 500


@app.route("/admin_logout", methods=["POST"])
def admin_logout():
    session.pop("admin_logged_in", None)
    return jsonify(success=True)


# Apply the caching headers to all responses
@app.after_request
def apply_caching(response):
    return disable_caching(response)


@app.route("/submit", methods=["GET", "POST"])
def submit_request():
    if request.method == "POST":
        issue = request.form.get("issue", "")
        email = request.form.get(
            "email", ""
        )  # Use default value '' if 'remarks' is missing
        urgency = request.form.get("urgency", "")

        # Create a new Request object and insert it into the database
        try:
            new_request = Request(issue=issue, email=email, urgency=urgency)
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for("table"))  # Redirect to the 'success' endpoint
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {str(e)}"}), 500
    else:
        return render_template("submit.html")

    # #############################################################
    # commit the comment addition


@app.route("/submitComment", methods=["GET", "POST"])
def submit_comment():
    if request.method == "POST":
        # data = request.get_json()  # Get the JSON data from the request
        # issue_id = data.get["issue_id", ""]
        # issue_id = request.args.get('issue_id')

        issue_id = request.form.get("issue_id", "")
        comment = request.form.get("comment", "")
        email = request.form.get("email", "")
        date_posted = datetime.now()
        session.pop("received issue id", issue_id)

        # Initialize a list to store the paths of uploaded images
        image_paths = []

        if "image" in request.files:
            uploaded_files = request.files.getlist("image")
            for uploaded_file in uploaded_files:
                if uploaded_file.filename != "":
                    filename = secure_filename(uploaded_file.filename)
                    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    uploaded_file.save(image_path)
                    image_paths.append(image_path)

        # Create a new Request object and insert it into the database
        try:
            # Convert row_id to integer (if applicable)
            # issue_id = int(issue_id) if issue_id else None
            new_comment = Comment(
                issue_id=issue_id,
                date_posted=date_posted,
                comment=comment,
                email=email,
                image_paths=image_paths,
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(
                f"/commentpop?issue_id={issue_id}"
            )  # Redirect to the 'success' endpoint
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {str(e)}"}), 500
    else:
        issue_id = request.args.get("issue_id")
        return redirect(f"/commentpop?issue_id={issue_id}")


# ###################################################################
#  copy of basetable for testing
@app.route("/test")
def test():
    return render_template("nesttable.html")

    #  Testing the nested tables


@app.route("/commentpop")
def commentpop():
    issue_id = request.args.get("issue_id")
    return render_template("commentpop.html", issue_id=issue_id)


@app.route("/table")
def table():
    return render_template("basetable.html")


@app.route("/")
def home():
    return render_template("basetable.html")


# /////////////////////////////////////////////
# Remove the nested table
# OLD GET DATA
@app.route("/get_data")
def get_data():
    requests = Request.query.all()
    data = [
        {
            "id": request.id,
            "urgency": request.urgency.value,
            "tag": request.tags,
            "date_posted": request.date_posted,
            "issue": request.issue,
            "email": request.email,
            "remarks": request.remarks,
            "date_updated": request.date_updated,
            "status": request.status.value if request.status else None,
            "expected_completion": request.expected_completion,
        }
        for request in requests
    ]
    return jsonify(data)


# /////////////////////////////////////////////

# @app.route("/get_comment")
# def get_comment():
#     comments = Comment.query.all()
#     commentdata = [
#         {
#             "id": comment.id_comment,
#             "issue_id": comment.issue_id,
#             "date_posted": comment.date_posted,
#             "email": comment.email,
#             "comment": comment.issue,
#             "remarks": comment.remarks,

#         }
#         for comment in comments
#     ]
#     return jsonify(commentdata)


@app.route("/get_issue_for_comment")
def get_issue_for_comment():
    issue_ID = int(request.args.get("issue_id"))
    requests = Request.query.filter_by(id=issue_ID).all()
    data = [
        {
            "id": request.id,
            "urgency": request.urgency.value,
            "tag": request.tags,
            "date_posted": request.date_posted,
            "issue": request.issue,
            "email": request.email,
            "remarks": request.remarks,
            "date_updated": request.date_updated,
            "status": request.status.value if request.status else None,
            "expected_completion": request.expected_completion,
        }
        for request in requests
    ]
    return jsonify(data)



@app.route("/get_comment", methods=["GET"])
def get_comment():
    commentdata = []
    try:
        # Get the 'issue_id' query parameter from the request
        issue_ID = int(request.args.get("issue_id"))

        # Debugging: Print the received 'issue_id' to the console
        session.pop("received issue id", issue_ID)
        print(" print Received issue_id:", issue_ID)

        # Query the comments based on 'issue_id'
        comments = Comment.query.filter_by(issue_id=issue_ID).all()

        # Convert comments to a list of dictionaries
        
        commentdata = [
            {
                "id": comment.id_comment,
                "issue_id": comment.issue_id,
                "date_posted": comment.date_posted,
                "email": comment.email,
                "comment": comment.comment,
                "remarks": comment.remarks,
                "image_paths": comment.image_paths,
            }
            for comment in comments
        ]

        return jsonify(commentdata)

    except ValueError:
        return jsonify({"error": "Invalid issue_id"}), 400

    # @app.route("/get_data2")
    # def get_data2():
    requests = Request.query.all()

    tree_data = []
    for request_obj in requests:
        request_data = {
            "id": request_obj.id,
            "urgency": request_obj.urgency.value,
            "tag": request.tags,
            "date_posted": request_obj.date_posted,
            "issue": request_obj.issue,
            "email": request_obj.email,
            "remarks": request_obj.remarks,
            "date_updated": request_obj.date_updated,
            "status": request_obj.status.value,
            # "status": request_obj.status,
            "expected_completion": request_obj.expected_completion,
            "comments": [],  # Initialize an empty list for comments
        }

        for comment in request_obj.comments:
            comment_data = {
                "id": comment.issue_id,
                # "id": comment.comment_id,
                "date_posted": comment.date_posted,
                "issue": comment.issue,
                "email": comment.email,
                "remarks": comment.remarks,
                # "remarks": comment.remarks
            }
            request_data["comments"].append(comment_data)

        tree_data.append(request_data)

    return jsonify(tree_data)


# @app.route("/get_data_comment")
# def get_data_comment():
#     comments = Comment.query.all()
#     data = [
#         {
#             "id": comment.id,
#             "date_posted": comment.DATE_POSTED,
#             "email": comment.EMAIL,
#             "comment": comment.COMMENT,
#         }
#         for comment in comments
#     ]
#     return jsonify(data)


@app.route("/update_comments", methods=["POST"])
def update_comments():
    data = request.get_json()

    for item in data:
        comment_id = item["id"]
        remarks = item["remarks"]

        # Update the "comments" column in the database
        comment_row = Comment.query.get(comment_id)
        comment_row.remarks = remarks

    # Commit the changes to the database
    db.session.commit()
    return jsonify(success=True)


@app.route("/update_comments_only", methods=["POST"])
def update_comments_only():
    if session.get("admin_logged_in"):
        try:
            data = request.get_json()

            for item in data:
                comment_id = item["id"]
                # issue_id = item["issue_id"]
                # comment_new = item["issue"]
                remarks_new = item["remarks"]

                comment_row = Comment.query.get(comment_id)
                comment_row.remarks = remarks_new
                # comment_row.date_updated = date_updated  # Assign the datetime object
                # comment_row.expected_completion = expected_completion

                db.session.commit()

            return jsonify(success=True)
        # except SQLAlchemyError as e:  # Catch specific AQLAlchemy errors
        #     db.session.rollback()  # Rollback changes in case of an error
        #     return jsonify(success=False, message="commit changes error")
        # except JSONDecodeError:  # Catch specific JSON decode errors
        #     return jsonify(success=False, message="Invalid JSON data format")
        except Exception as e:
            return jsonify(success=False, message="Error in commit"), 500
    else:
        return jsonify(success=False, message="Unauthorized"), 500


# Run the application on localhost, port 5000
if __name__ == "__main__":
    app.run(debug=True)
    print(os.getenv("FLASK_ENV"))
