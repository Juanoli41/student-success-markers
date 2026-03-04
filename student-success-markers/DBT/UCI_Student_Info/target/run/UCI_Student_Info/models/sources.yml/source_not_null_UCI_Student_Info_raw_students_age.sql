
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select age
from "UCI_Student_Info"."public"."raw_students"
where age is null



  
  
      
    ) dbt_internal_test