# Project Management Tool

### User
    id                  big-int
    first_name          str
    last_name           str
    role (FK)           big-int
    date_joined         date-time
    last_login          date-time
    no_of_logins        big-int

### Role 
    id                  big-int
    role                str
    description         text
    permissions         <yet to decide>

### StatusCodes
    id                  big-int
    name                str | unique

### Project
    id                  big-int
    name                str (100)
    description         text
    created_by          FK (User)
    created_date_time   date-time (auto_now)
    last_modified       date-time
    start_date          date-time
    end_date            date-time
    status              FK ( Status )
    is_deleted          BooleanField ( False )

### Team
    
    name                str (50)
    users               ManyToMany (user)
    project             FK (Project)

### Tasks
    task_id             big-int
    project_id          FK ( Project )
    created_by          FK ( User )
    assigned_to         FK ( User )
    create_date         date-time
    due-date            date-time
    task_name           str
    task_description    text
    status              FK ( Status )
    priority            str (choice  - high, medium, low)







