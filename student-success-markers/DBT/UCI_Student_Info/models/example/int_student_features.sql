with staged as (
    select * from {{ ref('stg_students') }}
),

features as (
    select
        -- carry over all staged columns
        *,

        -- grade trend: is the student improving or declining?
        (grade_period_2 - grade_period_1) as grade_trend_p1_p2,
        (final_grade - grade_period_2) as grade_trend_p2_final,

        -- overall grade trajectory: positive = improving, negative = declining
        case
            when (grade_period_2 - grade_period_1) > 0 and (final_grade - grade_period_2) > 0 then 'improving'
            when (grade_period_2 - grade_period_1) < 0 and (final_grade - grade_period_2) < 0 then 'declining'
            else 'mixed'
        end as grade_trajectory,

        -- average grade across all periods
        round((grade_period_1 + grade_period_2 + final_grade) / 3.0, 2) as avg_grade,

        -- alcohol risk: combined weekday and weekend drinking
        (weekday_alcohol + weekend_alcohol) as total_alcohol_score,

        -- social risk score: higher means more at-risk lifestyle
        (goout + weekday_alcohol + weekend_alcohol) as social_risk_score,

        -- academic support score: higher means more support available
        -- academic support score: higher means more support available
    (
        case when school_support = 'yes' then 1 else 0 end +
        case when family_support = 'yes' then 1 else 0 end +
    case when paid_classes = 'yes' then 1 else 0 end
    ) as support_score,

        -- absence risk: flag students with high absences
        case when absences > 10 then 1 else 0 end as high_absences,

        -- failure flag
        case when past_failures > 0 then 1 else 0 end as has_prior_failures

    from staged
)

select * from features