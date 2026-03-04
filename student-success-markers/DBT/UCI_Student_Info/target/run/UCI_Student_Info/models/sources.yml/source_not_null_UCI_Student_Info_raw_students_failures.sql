
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select failures
from "UCI_Student_Info"."public"."raw_students"
where failures is null



  
  
      
    ) dbt_internal_test