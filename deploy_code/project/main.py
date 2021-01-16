from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from flask_login import login_required, current_user
from logic import pull_results
from . import db, page_not_found
import os

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


@main.route("/profile/<name>/", methods=["GET"])
def profile(name="index"):
    return render_template(f"{name}.html", page_name=f"{name.upper()}")


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
