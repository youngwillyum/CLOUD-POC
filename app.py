import pandas as pd
from database import SessionLocal
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends, status
from starlette.responses import RedirectResponse
from sqlalchemy import text
import io

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def return_csv(sql, db):
    try:
        df = pd.read_sql(sql, db.connection())
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        csv_records = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        return csv_records
    except Exception as exception:
        raise Exception("Issue converting (sql) into csv")

app = FastAPI()

@app.get("/get/emailids")
def get_emailids(db=Depends(get_db)):
    """
    Retrieves email IDs from the database and returns them as a CSV file.
    """
    sql = text(f"SELECT * FROM testtable")
    try:
        csv_data = return_csv(sql, db)
        db.close()  # Close the session after reading the SQL data
        return csv_data
    except Exception as e:
        db.close()  # Close the session in case of an exception
        raise e

@app.post("/update/emailids/{emplid}/{email_id}", status_code=status.HTTP_201_CREATED)
def update_emailids(emplid: str, email_id: str, db=Depends(get_db)):
    """
    Updates the email ID for a given EMPLID in the database.
    """
    sql = text(f"UPDATE testtable SET EMAILADDRESS = '{email_id}' WHERE EMPLID = '{emplid}'")
    try:
        with db.begin():
            test = db.execute(sql)  # Use db.execute instead of cs.execute
            db.commit()  # Commit the changes made in this transaction
        return {"message": "Email ID updated successfully"}
    except Exception as e:
        return {"message": "Failed to update email ID", "error": str(e)}

@app.post("/add/emailids/{emplid}/{email_id}", status_code=status.HTTP_201_CREATED)
def add_emailids(emplid: str, email_id: str, db=Depends(get_db)):
    """
    Adds a new EMPLID and email ID to the database.
    """
    sql = text(f"INSERT INTO testtable (EMPLID, EMAILADDRESS) VALUES ('{emplid}', '{email_id}')")
    try:
        with db.begin():
            test = db.execute(sql)  # Use db.execute instead of cs.execute
            db.commit()  # Commit the changes made in this transaction
        return {"message": "Employee ID and Email added successfully"}
    except Exception as e:
        return {"message": "Failed to add Employee ID and Email", "error": str(e)}

