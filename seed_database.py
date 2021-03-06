"""Automatically drop, recreate, and populate database"""

import os
from random import randint, choice
from faker import Faker
import crud
import model
import server

os.system('dropdb irr')
os.system('createdb irr')

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()

#make specific investigator for development - me!
investigator = crud.create_investigator(fname="Dr. Lisa", lname="Murray", email="lisamichellemurray@gmail.com", phone="123 456 7589")
investigator.password = "test"

#make specific participant for development - me!
participant = crud.create_participant(email="lisamichellemurray@gmail.com", fname="Lisa", lname="Murray", dob="01/02/1923", phone="123 456-7890")
participant.password = "test"

#make fake investigators for db, no pws:
for i in range(10):
    i_fname = fake.first_name()
    i_lname = fake.last_name()
    i_phone = fake.phone_number()
    # i_domain = fake.free_email_domain()
    i_email = f'{i_lname}.{i_fname}@test.com'

    investigator = crud.create_investigator(fname=i_fname, lname=i_lname, email=i_email, phone=i_phone)

study_names = [ 
    'Covid-19 Vaccine Study - Adults',
    'Covid-19 Vaccine Study - Children',
    'Alzheimers Medication Trial',
    'Impact of Vitamin D on Depression',
    'Genetic Screening for Non-Treatable Diseases',
    'Effectiveness of Chemotherapy vs. Placebo',
    'Comparison of Vitamin D Supplements vs. Vacation on Depression',
    'Comparison of Covid-19 Vaccine to Placebo',
    'Accuracy of Colon Cancer Screening',
    'Accuracy of At-Home Covid-19 Tests']

for j in range(10):
    #create study details and study object
    investigator_id = randint(1,10)
    study_name = study_names[j]
    investigational_product = fake.unique.license_plate()
    status = choice(["Planning", "Active"])
    
    study = crud.create_study(investigator_id=investigator_id, study_name=study_name, investigational_product=investigational_product, status=status)

    #create three results to return per study:
    for visit in ['recruitment', 'consent', 'study-visit-1']:
        result_category = choice(['actionable','unknown','personally valuable'])
        urgency_potential = choice([True, False])
        return_plan = choice([True, False])
        if return_plan is True:
            return_timing = choice(['during', 'after'])
        else:
            return_timing = None
        result_plan = crud.create_result_plan(
            study_id=study.study_id,
            result_category=result_category,
            visit=visit,
            urgency_potential=urgency_potential,
            return_plan=return_plan,
            test_name=f"{visit} test",
            return_timing=return_timing)

# create 10 participants per study
for k in range(100):

    # participant details
    p_fname = fake.first_name()
    p_lname = fake.last_name()
    p_phone = fake.phone_number()
    p_domain = fake.free_email_domain()
    p_dob = fake.date_of_birth(minimum_age=0, maximum_age=60)
    p_email = f'{p_lname.lower()}.{p_fname.lower()}@test.com'
    # p_email = f'{p_lname.lower()}.{p_fname.lower()}@{p_domain}'
    # p_email = 'return.of.results.dev@gmail.com'

    crud.create_participant(email=p_email, fname=p_fname, lname=p_lname, dob=p_dob, phone=p_phone)

# enroll each participant in a random study
participants = crud.return_all_participants()

for participant in participants:
    crud.create_participantsstudies_link(
        participant_id=participant.participant_id,
        study_id=randint(1,10))
    crud.create_participantsstudies_link(
        participant_id=participant.participant_id,
        study_id=randint(1,10))

# choose to receive all results available in each study enrolled in:

for participant in participants:
    for study in participant.studies:
        for result in study.result_plans:
            if result.return_plan == True:
                crud.create_result(participant_id=participant.participant_id, result_plan_id=result.result_plan_id, receive_decision=True)
            else:
                crud.create_result(participant_id=participant.participant_id, result_plan_id=result.result_plan_id, receive_decision=None)
