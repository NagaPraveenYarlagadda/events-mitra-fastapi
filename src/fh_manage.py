import psycopg2
from fastapi import APIRouter, HTTPException, status
from typing import List

from src import schemas
from src.database import get_db_connection

router = APIRouter(
    prefix="/api/function_halls",
    tags=['Function Halls']
)

@router.post("", response_model=schemas.FunctionHall)
async def add_function_hall(function_hall: schemas.FunctionHallCreate):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO function_halls (name, capacity, location, contact_person, contact_number) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        values = (
            function_hall.name,
            function_hall.capacity,
            function_hall.location,
            function_hall.contact_person,
            function_hall.contact_number
        )
        cursor.execute(insert_query, values)

        new_function_hall_id = cursor.fetchone()[0]
        connection.commit()
        function_hall_response = schemas.FunctionHall(
            id = new_function_hall_id,
            name = function_hall.name,
            capacity = function_hall.capacity,
            location = function_hall.location,
            contact_person = function_hall.contact_person,
            contact_number = function_hall.contact_number
        )

        return function_hall_response
    except Exception as e:
        print(e)
        connection.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.get("", response_model=List[schemas.FunctionHall])
async def get_function_halls():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        select_query = "SELECT * FROM function_halls"
        cursor.execute(select_query)

        function_halls = []
        for row in cursor.fetchall():
            function_hall = schemas.FunctionHall(
                id=row[0],
                name=row[1],
                capacity=row[2],
                location=row[3],
                contact_person=row[4],
                contact_number=row[5]
            )
            function_halls.append(function_hall)

        if not function_halls:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No function halls found')

        return function_halls
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.get("/{hall_id}", response_model=schemas.FunctionHall)
async def get_function_hall_by_id(hall_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        select_query = "SELECT * FROM function_halls WHERE id = %s"
        cursor.execute(select_query, (hall_id,))

        function_hall_data = cursor.fetchone()
        if not function_hall_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Function hall not found')

        function_hall = schemas.FunctionHall(
            id=function_hall_data[0],
            name=function_hall_data[1],
            capacity=function_hall_data[2],
            location=function_hall_data[3],
            contact_person=function_hall_data[4],
            contact_number=function_hall_data[5]
        )

        return function_hall
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        connection.close()
