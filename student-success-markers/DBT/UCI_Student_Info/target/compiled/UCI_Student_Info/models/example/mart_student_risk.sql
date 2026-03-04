with features as (
    select * from "UCI_Student_Info"."public"."int_student_features"
),

mart as (
    select
        -- identifier
        student_id,

        -- demographics
        school,
        sex,
        age,
        address,
        famsize,

        -- academic performance
        grade_period_1,
        grade_period_2,
        final_grade,
        avg_grade,
        grade_trend_p1_p2,
        grade_trend_p2_final,
        grade_trajectory,

        -- risk indicators
        past_failures,
        has_prior_failures,
        absences,
        high_absences,
        social_risk_score,
        total_alcohol_score,

        -- support
        support_score,
        wants_higher_ed,
        has_internet,
        study_time,
        travel_time,

        -- target variable
        at_risk

    from features
)

select * from mart