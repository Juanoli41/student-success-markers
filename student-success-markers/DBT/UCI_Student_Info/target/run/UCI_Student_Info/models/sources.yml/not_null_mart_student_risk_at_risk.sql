
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select at_risk
from "UCI_Student_Info"."public"."mart_student_risk"
where at_risk is null



  
  
      
    ) dbt_internal_test