from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import TextField
from logic import pull_results
from .models import Profiles
from . import db, page_not_found
import os
import json

main = Blueprint("main", __name__)

head = [
    "Skill / Job Role",
    "Current Rank",
    "Rank Change Year-on-Year",
    "Median Salary",
    "Median Salary % Change",
    "Historical Ads",
    "Live Vacancies",
]

file = pull_results()
table = [[value for value in row.values()] for row in file]

jobs = [
    {
        "id": i,
        "skill_job_role": table[i][0],
        "current_rank": table[i][1],
        "rank_change": table[i][2],
        "median_salary": table[i][3],
        "median_salary_change": table[i][4],
        "historical_ads": table[i][5],
        "live_vacancies": table[i][6],
    }
    for i in range(len(table))
]


def update_table():
    global file
    global table
    global jobs

    file = pull_results()
    table = [[value for value in row.values()] for row in file]

    jobs = [
        {
            "id": i,
            "skill_job_role": table[i][0],
            "current_rank": table[i][1],
            "rank_change": table[i][2],
            "median_salary": table[i][3],
            "median_salary_change": table[i][4],
            "historical_ads": table[i][5],
            "live_vacancies": table[i][6],
        }
        for i in range(len(table))
    ]


@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "pull" in request.form:
            update_table()

            return render_template(
                "index.html", page_name="Home Page", page=table, heading=head
            )

    elif request.method == "GET":
        return render_template("index.html", page_name="Home Page")


@main.route("/team/")
def team():
    return render_template("team.html", page_name="Meet the Team")


@main.route("/profile/<fname>_<lname>", methods=["GET"])
def profile(fname="index", lname="index"):
    data = Profiles.query.all()

    profile_data = None
    for person in data:
        if (
            person.fname.upper() == fname.upper()
            and person.lname.upper() == lname.upper()
        ):
            profile_data = person
            break

    if profile_data != None:
        service_json = json.loads(profile_data.services)
        service_temp = service_json.keys()
        service_keys = [x for x in service_temp]

        education_json = json.loads(profile_data.education)
        education_temp = education_json.keys()
        education_keys = [x for x in education_temp]

        experience_json = json.loads(profile_data.experience)
        experience_temp = experience_json.keys()
        experience_keys = [x for x in experience_temp]

        return render_template(
            "profile.html",
            page_name=f"{fname.upper()}",
            description=profile_data.description,
            name=f"{profile_data.fname} {profile_data.lname}",
            age=profile_data.age,
            year_exp=profile_data.year_exp,
            country=profile_data.country,
            location=profile_data.location,
            email=profile_data.email,
            service_keys=service_keys,
            service_data=service_json,
            education_keys=education_keys,
            education_data=education_json,
            experience_keys=experience_keys,
            experience_data=experience_json,
            image=f"{fname.lower()}_{lname.lower()}",
        )
    else:
        return render_template("404.html", page_name="ERROR 404")


# The only OOP Class To exist in my code :(
class DBForm(FlaskForm):
    first_name = TextField("First Name")
    last_name = TextField("Last Name")
    age = TextField("Age")
    description = TextField("Profile Description")
    year_exp = TextField("Year's of experience")
    country = TextField("Country (code)")
    location = TextField("Location (city)")
    email = TextField("Email Address")
    services_one = TextField("Services Box Title 1")
    services_one_desc = TextField("Services Box Description 1")
    services_two = TextField("Services Box Title 2")
    services_two_desc = TextField("Services Box Description 2")
    services_three = TextField("Services Box Title 3")
    services_three_desc = TextField("Services Box Description 3")
    services_four = TextField("Services Box Title 4")
    services_four_desc = TextField("Services Box Description 4")
    education = TextField("Education (Specific JSON Format!!!)")
    experience = TextField("Experience (Specific JSON Format!!!)")


@main.route("/db_form", methods=["GET", "POST"])
def db_form():
    error = ""
    form = DBForm(request.form)

    if request.method == "POST":
        fname = form.first_name.data
        lname = form.last_name.data
        age = form.age.data
        description = form.description.data
        year_exp = form.year_exp.data
        country = form.country.data
        location = form.location.data
        email = form.email.data
        services_one = form.services_one.data
        services_one_desc = form.services_one_desc.data
        services_two = form.services_two.data
        services_two_desc = form.services_two_desc.data
        services_three = form.services_three.data
        services_three_desc = form.services_three_desc.data
        services_four = form.services_four.data
        services_four_desc = form.services_four_desc.data
        education = form.education.data
        experience = form.experience.data

        if (
            fname
            and lname
            and age
            and description
            and year_exp
            and country
            and location
            and email
            and services_one
            and services_two
            and services_three
            and services_four
            and education
            and experience
        ):
            db_check = Profiles.query.all()

            exists = False
            for user in db_check:
                if user.fname == fname and user.lname == lname:
                    exists = True

            if not exists:
                services = json.dumps(
                    {
                        services_one: services_one_desc,
                        services_two: services_two_desc,
                        services_three: services_three_desc,
                        services_four: services_four_desc,
                    }
                )

                data = Profiles(
                    fname=fname,
                    lname=lname,
                    age=age,
                    description=description,
                    year_exp=year_exp,
                    country=country,
                    location=location,
                    email=email,
                    services=services,
                    education=education,
                    experience=experience,
                )
                db.session.add(data)
                db.session.commit()

            else:
                print("Already Exists")
        else:
            error = "Please fill in all the details!!"

    return render_template(
        "form.html",
        page_name="Profile Builder",
        msg=error,
        form=form,
        announce="Please use 'http://www.objgen.com/json' to generate JSON format.",
    )


@main.route("/test_db/")
def test_database():
    fname = "Hubert"
    lname = "Swic"
    age = 23
    description = "I am a Business Management Graduate. Currently working as a Python DevOps Trainee. Aspiring Programmer with 6 years of non-professional experience in multiple languages, such as Python, Lua, C++, JSON, and JavaScript to name a few. Working on open-source projects to further my understanding and learning to apply it in the workplace."
    year_exp = 5
    country = "UK"
    location = "London"
    email = "hswic@spartaglobal.com"
    services = json.dumps(
        {
            "Python": "An interpreted, high-level and general-purpose programming language.",
            "Flask": "A micro web framework written in Python. Used for back-end web applications.",
            "HashiCorp": "Knowledge of tools such as Terraform, Packer, Vagrant.",
            "Docker": "A set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.",
        }
    )
    education = json.dumps(
        {
            "University of Kent": [
                "2016 - 2020",
                "Studied Business Management with a year placement. Main modules consisted of Leadership, Management and Operations. Completed a CMI Level 5 Certification.",
            ],
            "St John Bosco College": [
                "2013 - 2016",
                "Sixth Form. Studied ICT, Busines, Media, achieved A*-B. Achieved many rewards in all the subjects studied.",
            ],
        }
    )
    experience = json.dumps(
        {
            "Python DevOps Trainee - Sparta Global": [
                "Oct 2020 - Present",
                "Currently training towards the consultant role. Studied core Business, Python, Linux, SQL, and Automated Deployment subjects.",
            ],
            "Sales Representative - House of Vapes": [
                "Sep 2018 - Aug 2019",
                "Helped customers through product choice process. Responsible for restocking the store. Worked in a small team. Provided technical knowledge about products and devices.",
            ],
            "Data Administrator - Computappoint": [
                "Aug 2017 - Sep 2017",
                "Dealt with customers over the phone, as well as email and updated the database with current and updated CV. Improved my communication skills and market knowledge, as well as team working skills as I worked as part of the recruitment team.",
            ],
        }
    )

    db_check = Profiles.query.all()

    exists = False
    for user in db_check:
        if user.fname == fname and user.lname == lname:
            exists = True

    if not exists:
        data = Profiles(
            fname=fname,
            lname=lname,
            age=age,
            description=description,
            year_exp=year_exp,
            country=country,
            location=location,
            email=email,
            services=services,
            education=education,
            experience=experience,
        )
        db.session.add(data)
        db.session.commit()

    else:
        print("Already Exists")


@main.route("/panel/", methods=["GET", "POST"])
@login_required
def panel():
    if request.method == "POST":
        if "submit" in request.form:
            params = request.form

            id_num = params.get("id_number")
            job = params.get("job_role")
            rank = params.get("rank")

            query_builder = []

            if id_num:
                query_builder.append(f"id={id_num}")

            if job:
                query_builder.append(f"skill_job_role={job}")

            if rank:
                query_builder.append(f"current_rank={rank}")

            if not (id_num or job or rank):
                return page_not_found(404)

            query = "?" + "&".join(query_builder)

            return redirect("/api/v1/resources/jobs" + query)

    elif request.method == "GET":
        return render_template(
            "panel.html", page_name="User Panel", name=current_user.username
        )


@main.route("/api/v1/resources/jobs/all", methods=["GET"])
def api_all():
    return jsonify(jobs)


@main.route("/api/v1/resources/jobs", methods=["GET"])
def api_id():
    params = request.args

    id_num = None
    job_name = None
    rank = None

    if "id" in params:
        id_num = int(params["id"])

    if "skill_job_role" in params:
        job_name = str(params["skill_job_role"])

    if "current_rank" in params:
        rank = str(params["current_rank"])

    results = []
    for job in jobs:
        if job["id"] == id_num:
            results.append(job)

        if job["skill_job_role"] == job_name:
            results.append(job)

        if job["current_rank"] == rank:
            results.append(job)

    if len(results) == 0:
        return page_not_found(404)

    return jsonify(results)


@main.errorhandler(500)
def template_not_found(e):
    return render_template("404.html", page_name="ERROR 500")
