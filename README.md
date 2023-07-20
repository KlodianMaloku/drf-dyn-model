# drf-dyn-model
A django rest framework app creating dynamic models using schema editor


## Initial configurations
    1. docker-compose up -d --build
    2. docker-compose exec web python manage.py migrate --noinput
    3. docker-compose exec web python manage.py createsuperuser

## Usage

    1. To see the api urls use http://localhost:8000/swagger-docs

    2. To add a new model make a post call to : 
        http://localhost:8000/api/table
        with the following body
        ```json
        {
            "name": "model24",
            "db_name": "default",
            "managed": true,
            "db_table_name": "table24",
            "fields": [
            {
                "name5555": "Field1",
                "class_name": "django.db.models.TextField",
                "kwargs": {}
            },
            {
                "name": "Field2",
                "class_name": "django.db.models.IntegerField",
                "kwargs": {"default": 0}
            },
            {
                "name": "Field3",
                "class_name": "django.db.models.TextField",
                "kwargs": {"null": true}
            }
            ]
        }

    4. To modify the model of the dynamic table created above make a put call to: 
        http://localhost:8000/api/table/{table_id} where
        {table_id} is the id of the row in modelschema table for the create dynamic table. The body of the post call
            
            ```json
            {
                "name": "model24",
                "db_name": "default",
                "managed": true,
                "db_table_name": "table24",
                "fields": [
                {
                    "name": "Field1",
                    "class_name": "django.db.models.TextField",
                    "kwargs": {}
                },
                {
                    "name": "Field2",
                    "class_name": "django.db.models.IntegerField",
                    "kwargs": {"default": 0}
                },
                {
                    "name": "Field3",
                    "class_name": "django.db.models.TextField",
                    "kwargs": {"null": true}
                },
                {
                    "name": "Field4",
                    "class_name": "django.db.models.TextField",
                    "kwargs": {"null": true}
                }
                ]
            }

    3. To add rows to a dynamic table make a post call to: 
        http://localhost:8000/api/table/{table_id}/row where
       {table_id} is the id of the row in modelschema table for the create dynamic table. The body of the post call
        
        ```json
        {
            "Field1": "value1",
            "Field2": 2,
            "Field3": "value3"
        }

    4. To get all the rows of a dynamic table make a get call to
        http://localhost:8000/api/table/{table_id}/rows where
         {table_id} is the id of the row in modelschema table for the create dynamic table.
    
```bash