import json

from flask import render_template, request, redirect, url_for

from datetime import datetime
from uuid import uuid4

from app import app, db, Employment, NursingCourse, Person, Education
from map import prepare_regions, prepare_powiats_data
from courses import education_levels
from places import wojewodztwa_dict


@app.route('/')
def index():
    wojewodztwa = prepare_regions("static/maps/wojewodztwa-min.geojson")
    powiaty = prepare_regions("static/maps/powiaty-min.geojson")

    poland_west_most = 999
    poland_east_most = -999
    poland_north_most = -999
    poland_south_most = 999

    for wojewodztwo in wojewodztwa:
        poland_west_most = min(wojewodztwo["west_border"], poland_west_most)
        poland_east_most = max(wojewodztwo["east_border"], poland_east_most)
        poland_north_most = max(wojewodztwo["north_border"], poland_north_most)
        poland_south_most = min(wojewodztwo["south_border"], poland_south_most)

    poland_width = poland_east_most - poland_west_most
    poland_height = poland_north_most - poland_south_most

    powiats_data = json.dumps(prepare_powiats_data("static/maps/powiats.csv"))

    all_employment_data = Employment.query.all()
    #print(all_employment_data)
    employment_info = [
        {
            'wojewodztwo': employment_data.place,
            'wage': employment_data.wage
        }
        for employment_data in all_employment_data
    ]
    print(employment_info)

    return render_template(
        "index.html",
        wojewodztwa=wojewodztwa,
        powiaty=powiaty,
        poland_west_most=poland_west_most,
        poland_north_most=poland_north_most,
        poland_width=poland_width,
        poland_height=poland_height,
        powiats_data=powiats_data
    )


@app.route('/form', methods=['GET', 'POST'])
def form():
    all_courses = {
        level: [
            {
                'id': level.replace(' ', '_') + '_' + str(i),
                'label': course + ' (' + level + ')',
                'name': course,
                'level': level
            }
            for i, course in enumerate(courses_list)
        ]
        for level, courses_list in education_levels.items()
    }

    course_id_to_name = {
        course_data['id']: {'name': course_data['name'], 'level': course_data['level']}
        for courses_on_given_level in all_courses.values()
        for course_data in courses_on_given_level
    }

    if request.method == "POST":
        print(request.form)

        # get answers from the form
        sex = request.form.get('sex')
        year_of_birth = request.form.get('year_of_birth')
        #years_of_experience = request.form.get('years_of_experience')
        user_courses = request.form.getlist('course[]')
        course_years = request.form.getlist('course_year[]')
        finished_courses = [
            {'id': course_id, 'year': course_year, 'name': course_id_to_name[course_id]['name'], 'level': course_id_to_name[course_id]['level']}
            for course_id, course_year in zip(user_courses, course_years)
        ]
        print(sex, year_of_birth, finished_courses)
        now = datetime.utcnow()
        print(now)
        print(datetime.strptime(request.form.get('date_from'), "%Y-%m"))
        employment = Employment(
            date_from=datetime.strptime(request.form.get('date_from'), "%Y-%m"),
            date_to=datetime.strptime(request.form.get('date_to'), "%Y-%m"),
            #person_id=,
            date_entered=now,
            date_modified=now,
            **{
                key: request.form.get(key)
                for key in ['place', 'position', 'type_of_contract', 'wage', 'wage_per_x']
            }
        )

        #NursingCourse, Education

        person = Person(
            username=str(uuid4()),
            hashed_password=str(uuid4()),
            date_added=now,
            date_modified=now,
            **{
                key: request.form.get(key)
                for key in ['year_of_birth', 'sex', 'years_of_experience']
            }
        )

        db.session.add_all([employment, person])
        db.session.commit()

        return redirect(url_for('index'))

    return render_template(
        "form.html",
        courses=all_courses,
        wojewodztwa_dict=wojewodztwa_dict
    )