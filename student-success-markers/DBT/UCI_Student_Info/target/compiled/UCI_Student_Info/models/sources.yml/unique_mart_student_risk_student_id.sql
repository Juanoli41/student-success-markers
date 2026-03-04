
    
    

select
    student_id as unique_field,
    count(*) as n_records

from "UCI_Student_Info"."public"."mart_student_risk"
where student_id is not null
group by student_id
having count(*) > 1


