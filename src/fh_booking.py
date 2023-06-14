import psycopg2
from fastapi import APIRouter, HTTPException, status
from typing import List

from src import schemas
from src.database import get_db_connection

router = APIRouter(
    prefix="/api/bookings",
    tags=['Bookings']
)

@router.post("", response_model=schemas.Booking)
async def add_booking(booking: schemas.BookingCreate):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO bookings (hall_name, date, start_time, end_time, customer_name, booking_status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING booking_id"
        values = (
            booking.hall_name,
            booking.date,
            booking.start_time,
            booking.end_time,
            booking.customer_name,
            'Pending'
        )
        cursor.execute(insert_query, values)

        new_booking_id = cursor.fetchone()[0]
        connection.commit()
        booking_response = schemas.Booking(
            booking_id=new_booking_id,
            hall_name=booking.hall_name,
            date=booking.date,
            start_time=booking.start_time,
            end_time=booking.end_time,
            customer_name=booking.customer_name,
            booking_status='Pending'
        )

        return booking_response
    except Exception as e:
        print(e)
        connection.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.get("", response_model=List[schemas.Booking])
async def get_bookings():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        select_query = "SELECT * FROM bookings"
        cursor.execute(select_query)

        bookings = []
        for row in cursor.fetchall():
            booking = schemas.Booking(
                booking_id=row[0],
                hall_name=row[1],
                date=row[2],
                start_time=row[3],
                end_time=row[4],
                customer_name=row[5],
                booking_status=row[6]
            )
            bookings.append(booking)

        if not bookings:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No bookings found')

        return bookings
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.get("/{booking_id}", response_model=schemas.Booking)
async def get_booking_by_id(booking_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        select_query = "SELECT * FROM bookings WHERE booking_id = %s"
        cursor.execute(select_query, (booking_id,))

        booking_data = cursor.fetchone()
        if not booking_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')

        booking = schemas.Booking(
            booking_id=booking_data[0],
            hall_name=booking_data[1],
            date=booking_data[2],
            start_time=booking_data[3],
            end_time=booking_data[4],
            customer_name=booking_data[5],
            booking_status=booking_data[6]
        )

        return booking
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        connection.close()