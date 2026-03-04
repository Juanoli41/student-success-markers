
  create view "UCI_Student_Info"."public"."stg_students__dbt_tmp"
    
    
  as (
    with source as (
    select * from "UCI_Student_Info"."public"."raw_students"
),

staged as (
    select
        -- identifiers
        row_number() over () as student_id,

        -- demographics
        school,
        sex,
        age,
        address,
        famsize,
        pstatus,

        -- parent background
        medu as mother_education,
        fedu as father_education,
        mjob as mother_job,
        fjob as father_job,
        guardian,

        -- academic
        traveltime as travel_time,
        studytime as study_time,
        failures as past_failures,
        absences,
        g1 as grade_period_1,
        g2 as grade_period_2,
        g3 as final_grade,

        -- support
        schoolsup as school_support,
        famsup as family_support,
        paid as paid_classes,
        higher as wants_higher_ed,
        internet as has_internet,

        -- lifestyle
        famrel as family_relationship,
        freetime,
        goout,
        dalc as weekday_alcohol,
        walc as weekend_alcohol,
        health,
        romantic,

        -- target variable
        case when g3 < 10 then 1 else 0 end as at_risk

    from source
)

select * from staged
  );