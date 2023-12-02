# Run Application

python version: `3.11`

1. Create a virtual environment

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

2. Run the application

    ```bash
    pip install -r ./requirements.txt
    $env:FLASK_APP = "flaskapp.py"
    flask run --debug
    ```

3. Database

    ```bash
    flask shell
    from flaskapp import db
    db.create_all()
    ```

### Appendix

1. [flask shell script](./flaskapp/flask_db.md)

2. Freeze requirements
   ```bash
   pip freeze
   pip freeze > requirements.txt
   ```"# flaskProject" 
