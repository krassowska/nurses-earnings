import json

from flask import render_template, request, redirect, url_for

from datetime import datetime
from uuid import uuid4
from unidecode import unidecode

from app import app, db, Employment, NursingCourse, Person, Education
from map import prepare_regions, prepare_powiats_data
from courses import education_levels
from places import wojewodztwa_list, wojewodztwa_dict


def calculate_mean(regions_list, employment_info):
    regions_wage = {}

    for region in regions_list:
        regions_wage[unidecode(region)] = [0, 0]

    for info in employment_info:
        regions_wage[info['wojewodztwo']][0] += info['wage']
        regions_wage[info['wojewodztwo']][1] += 1

    regions_wage_mean = {
        region: (wage / count)
        for region, (wage, count) in regions_wage.items() if count
    }
    
    return regions_wage_mean


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

    ''''id': person_data.id,
            'year_of_birth': person_data.year_of_birth,
            'sex': person_data.sex,
            'years_of_experience': person_data.years_of_experience'''

    all_person_data = Person.query.all()
    person_info = {
        person_data.id: person_data
        for person_data in all_person_data
    }
    
    all_employment_data = Employment.query.all()
    all_employment_info = [
        {
            'wojewodztwo': employment_data.place,
            'wage': employment_data.wage,
            'sex': person_info[employment_data.person_id].sex
        }
        for employment_data in all_employment_data
    ]
        
    wojewodztwa_wage_mean = calculate_mean(wojewodztwa_list, all_employment_info)
    
    # find wage for males anf females
    wojewodztwa_female_wage_mean = calculate_mean(
        wojewodztwa_list,
        [
            info
            for info in all_employment_info if info['sex'] == 'Female'
        ]
    )
    wojewodztwa_male_wage_mean = calculate_mean(
        wojewodztwa_list,
        [
            info
            for info in all_employment_info if info['sex'] == 'Male'
        ]
    )

    return render_template(
        "index.html",
        wojewodztwa=wojewodztwa,
        powiaty=powiaty,
        poland_west_most=poland_west_most,
        poland_north_most=poland_north_most,
        poland_width=poland_width,
        poland_height=poland_height,
        powiats_data=powiats_data,
        wojewodztwa_wage_mean=wojewodztwa_wage_mean,
        wojewodztwa_female_wage_mean=wojewodztwa_female_wage_mean,
        wojewodztwa_male_wage_mean=wojewodztwa_male_wage_mean
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
        #print(request.form)

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
        #print(sex, year_of_birth, finished_courses)
        now = datetime.utcnow()
        #print(datetime.strptime(request.form.get('date_from'), "%Y-%m"))

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

        employment = Employment(
            date_from=datetime.strptime(request.form.get('date_from'), "%Y-%m"),
            date_to=datetime.strptime(request.form.get('date_to'), "%Y-%m"),
            person=person,
            date_entered=now,
            date_modified=now,
            **{
                key: request.form.get(key)
                for key in ['place', 'position', 'type_of_contract', 'wage', 'wage_per_x']
            }
        )

        db.session.add_all([person, employment])
        db.session.commit()

        return redirect(url_for('index'))

    return render_template(
        "form.html",
        courses=all_courses,
        wojewodztwa_dict=wojewodztwa_dict
    )