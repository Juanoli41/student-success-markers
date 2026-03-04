
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select student_id
from "UCI_Student_Info"."public"."stg_students"
where student_id is null



  
  
      
    ) dbt_internal_test