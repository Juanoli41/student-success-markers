
    
    

with all_values as (

    select
        at_risk as value_field,
        count(*) as n_records

    from "UCI_Student_Info"."public"."stg_students"
    group by at_risk

)

select *
from all_values
where value_field not in (
    '0','1'
)


