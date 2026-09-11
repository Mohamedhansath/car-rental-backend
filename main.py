# """
# DriveEase Car Rental — Complete FastAPI Backend (FIXED)
# ============================================================
# INSTALL:  pip install fastapi uvicorn mysql-connector-python
# RUN:      uvicorn main:app --reload --port 8000
# ============================================================
# """
#
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Optional
# import mysql.connector
# from datetime import date
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # ── DB CONFIG — உங்கள் password & db name இங்கே போடுங்க ──────────
# DB_CONFIG = {
#     "host":     "localhost",
#     "user":     "root",
#     "password": "",           # ← உங்கள் MySQL password
#     "database": "carrental"   # ← schema.sql-ல் உள்ள DB name
# }
#
# def get_db():
#     return mysql.connector.connect(**DB_CONFIG)
#
#
# # ══════════════════════════════════════════════════════════════
# #  PYDANTIC MODELS
# # ══════════════════════════════════════════════════════════════
#
# class RegisterModel(BaseModel):
#     email:    str
#     password: str
#     name:     Optional[str] = ""
#     phone:    Optional[str] = ""
#     city:     Optional[str] = ""
#
# class LoginModel(BaseModel):
#     email:    str
#     password: str
#
# class ForgotPasswordModel(BaseModel):
#     email:        str
#     new_password: str
#
# class ProfileUpdateModel(BaseModel):
#     id:    int
#     name:  Optional[str] = ""
#     phone: Optional[str] = ""
#     city:  Optional[str] = ""
#
# class CarModel(BaseModel):
#     name:         str
#     brand:        Optional[str]   = ""
#     type:         Optional[str]   = "Sedan"
#     fuel:         Optional[str]   = "Petrol"
#     seats:        Optional[int]   = 5
#     transmission: Optional[str]   = "Manual"
#     price:        Optional[int]   = 0
#     status:       Optional[str]   = "Available"
#     plate:        Optional[str]   = ""
#     year:         Optional[int]   = 2022
#     img:          Optional[str]   = "🚗"
#     rating:       Optional[float] = 4.5
#     reviews:      Optional[int]   = 0
#     available:    Optional[bool]  = True
#     features:     Optional[str]   = ""
#     image:        Optional[str]   = ""
#     description:  Optional[str]   = ""
#
# class BookingModel(BaseModel):
#     userId:    int
#     carId:     int
#     days:      Optional[int] = 1
#     pickup:    Optional[str] = "Chennai"
#     drop:      Optional[str] = "Chennai"
#     from_date: Optional[str] = None
#     to_date:   Optional[str] = None
#     status:    Optional[str] = "Booked"
#
# class BookingUpdateModel(BaseModel):
#     customer: Optional[str] = ""
#     phone:    Optional[str] = ""
#     car:      Optional[str] = ""
#     pickup:   Optional[str] = "Chennai"
#     drop:     Optional[str] = "Chennai"
#     from_:    Optional[str] = None
#     to:       Optional[str] = None
#     amount:   Optional[int] = 0
#     status:   Optional[str] = "Pending"
#
# class StatusUpdateModel(BaseModel):
#     status: str
#
# class AdminUserUpdateModel(BaseModel):
#     id:    int
#     name:  Optional[str] = ""
#     email: Optional[str] = ""
#     phone: Optional[str] = ""
#     city:  Optional[str] = ""
#
#
# # ══════════════════════════════════════════════════════════════
# #  USER ROUTES  — TABLE: users
# # ══════════════════════════════════════════════════════════════
#
# @app.post("/users/registration1")
# def register(data: RegisterModel):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))
#         if cursor.fetchone():
#             raise HTTPException(status_code=400, detail="Email already registered")
#
#         cursor.execute(
#             "INSERT INTO users (name, email, password, phone, city) VALUES (%s, %s, %s, %s, %s)",
#             (data.name, data.email, data.password, data.phone, data.city)
#         )
#         db.commit()
#         return {"message": "Registration successful", "user_id": cursor.lastrowid}
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.post("/users/login1")
# def login(data: LoginModel):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute(
#             "SELECT id, name, email, phone, city FROM users WHERE email = %s AND password = %s",
#             (data.email, data.password)
#         )
#         user = cursor.fetchone()
#         if not user:
#             raise HTTPException(status_code=401, detail="Invalid email or password")
#         return {"message": "Login successful", "user": user}
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.put("/users/forgot-password")
# def forgot_password(data: ForgotPasswordModel):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))
#         if not cursor.fetchone():
#             raise HTTPException(status_code=404, detail="Email not found")
#
#         cursor.execute(
#             "UPDATE users SET password = %s WHERE email = %s",
#             (data.new_password, data.email)
#         )
#         db.commit()
#         return {"message": "Password updated successfully"}
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.put("/api/profile")
# def update_profile(data: ProfileUpdateModel):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         cursor.execute(
#             "UPDATE users SET name=%s, phone=%s, city=%s WHERE id=%s",
#             (data.name, data.phone, data.city, data.id)
#         )
#         db.commit()
#         if cursor.rowcount == 0:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {"message": "Profile updated successfully"}
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.get("/api/my-bookings/{user_id}")
# def my_bookings(user_id: int):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute(
#             """SELECT
#                 b.id, b.car_id,
#                 b.car_name, b.car_type, b.car_image, b.car_brand,
#                 b.days, b.price, b.status,
#                 b.pickup, b.drop_loc,
#                 b.from_date, b.to_date, b.created_at,
#                 u.name AS user_name, u.email AS user_email, u.phone AS user_phone
#                FROM bookings b
#                JOIN users u ON b.user_id = u.id
#                WHERE b.user_id = %s
#                ORDER BY b.created_at DESC""",
#             (user_id,)
#         )
#         rows = cursor.fetchall()
#         for r in rows:
#             for k in ("from_date", "to_date", "created_at"):
#                 if r.get(k) and not isinstance(r[k], str):
#                     r[k] = str(r[k])
#             r["id"] = str(r["id"])
#         return rows
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# # ══════════════════════════════════════════════════════════════
# #  CARS ROUTES
# # ══════════════════════════════════════════════════════════════
#
# @app.get("/api/cars")
# def get_cars(available: Optional[bool] = None):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         if available is None:
#             cursor.execute("SELECT * FROM cars ORDER BY id")
#         else:
#             cursor.execute(
#                 "SELECT * FROM cars WHERE available=%s ORDER BY id",
#                 (1 if available else 0,)
#             )
#         cars = cursor.fetchall()
#         for c in cars:
#             if isinstance(c.get("features"), str):
#                 c["features"] = [f.strip() for f in c["features"].split(",") if f.strip()]
#             c["available"] = bool(c.get("available"))
#         return cars
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.get("/api/cars/{car_id}")
# def get_car(car_id: int):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
#         car = cursor.fetchone()
#         if not car:
#             raise HTTPException(status_code=404, detail="Car not found")
#         if isinstance(car.get("features"), str):
#             car["features"] = [f.strip() for f in car["features"].split(",") if f.strip()]
#         car["available"] = bool(car.get("available"))
#         return car
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.post("/api/cars")
# def add_car(data: CarModel):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         features_str = data.features if isinstance(data.features, str) else ",".join(data.features or [])
#         cursor.execute(
#             """INSERT INTO cars
#                (name,brand,type,fuel,seats,transmission,price,status,
#                 plate,year,img,rating,reviews,available,features,image,description)
#                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
#             (data.name, data.brand, data.type, data.fuel, data.seats,
#              data.transmission, data.price, data.status, data.plate,
#              data.year, data.img, data.rating, data.reviews,
#              1 if data.available else 0,
#              features_str, data.image, data.description)
#         )
#         db.commit()
#         return {"message": "Car added", "id": cursor.lastrowid}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.put("/api/cars/{car_id}")
# def update_car(car_id: int, data: CarModel):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         features_str = data.features if isinstance(data.features, str) else ",".join(data.features or [])
#         cursor.execute(
#             """UPDATE cars SET
#                name=%s, brand=%s, type=%s, fuel=%s, seats=%s,
#                transmission=%s, price=%s, status=%s, plate=%s,
#                year=%s, img=%s, rating=%s, reviews=%s,
#                available=%s, features=%s, image=%s, description=%s
#                WHERE id=%s""",
#             (data.name, data.brand, data.type, data.fuel, data.seats,
#              data.transmission, data.price, data.status, data.plate,
#              data.year, data.img, data.rating, data.reviews,
#              1 if data.available else 0,
#              features_str, data.image, data.description, car_id)
#         )
#         db.commit()
#         return {"message": "Car updated"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.delete("/api/cars/{car_id}")
# def delete_car(car_id: int):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
#         db.commit()
#         return {"message": "Car deleted"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# # ══════════════════════════════════════════════════════════════
# #  BOOKINGS ROUTES
# # ══════════════════════════════════════════════════════════════
#
# @app.get("/api/bookings")
# def get_bookings():
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute(
#             """SELECT
#                 b.id,
#                 b.user_id,
#                 b.car_id,
#                 b.user_name  AS customer,
#                 b.user_email,
#                 b.user_phone AS phone,
#                 b.car_name   AS car,
#                 b.car_type,
#                 b.car_image,
#                 b.car_brand,
#                 b.pickup,
#                 b.drop_loc   AS `drop`,
#                 b.from_date  AS `from`,
#                 b.to_date    AS `to`,
#                 b.days,
#                 b.price      AS amount,
#                 b.status,
#                 b.created_at AS createdAt
#                FROM bookings b
#                ORDER BY b.created_at DESC"""
#         )
#         rows = cursor.fetchall()
#         for r in rows:
#             for k in ("from", "to", "createdAt"):
#                 if r.get(k) and not isinstance(r[k], str):
#                     r[k] = str(r[k])
#             r["id"] = str(r["id"])
#         return rows
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.post("/api/bookings")
# def create_booking(data: BookingModel):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         # 1. User fetch — users table
#         cursor.execute(
#             "SELECT id, name, email, phone FROM users WHERE id = %s",
#             (data.userId,)
#         )
#         user = cursor.fetchone()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#
#         # 2. Car fetch
#         cursor.execute(
#             "SELECT id, name, type, image, brand, price, available FROM cars WHERE id = %s",
#             (data.carId,)
#         )
#         car = cursor.fetchone()
#         if not car:
#             raise HTTPException(status_code=404, detail="Car not found")
#
#         if not car["available"]:
#             raise HTTPException(status_code=400, detail="Car is not available")
#
#         # 3. Duplicate booking check
#         cursor.execute(
#             "SELECT id FROM bookings WHERE user_id=%s AND car_id=%s AND status='Booked'",
#             (data.userId, data.carId)
#         )
#         if cursor.fetchone():
#             raise HTTPException(status_code=400, detail="Already booked this car")
#
#         # 4. Price
#         days        = max(1, data.days or 1)
#         total_price = int(car["price"]) * days
#
#         # 5. Insert booking
#         cursor.execute(
#             """INSERT INTO bookings
#                (user_id, car_id,
#                 user_name, user_email, user_phone,
#                 car_name, car_type, car_image, car_brand,
#                 pickup, drop_loc,
#                 from_date, to_date,
#                 days, price, status)
#                VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s, %s,%s, %s,%s, %s,%s,%s)""",
#             (
#                 data.userId, data.carId,
#                 user["name"]  or "", user["email"] or "", user["phone"] or "",
#                 car["name"]   or "", car["type"]   or "", car["image"] or "", car["brand"] or "",
#                 data.pickup   or "Chennai",
#                 data.drop     or "Chennai",
#                 data.from_date or str(date.today()),
#                 data.to_date   or str(date.today()),
#                 days, total_price, "Booked"
#             )
#         )
#         booking_id = cursor.lastrowid
#
#         # 6. Mark car as unavailable
#         cursor.execute(
#             "UPDATE cars SET available=0, status='Rented' WHERE id=%s",
#             (data.carId,)
#         )
#         db.commit()
#
#         return {
#             "message":  "Booking successful",
#             "id":       booking_id,
#             "carId":    data.carId,
#             "carName":  car["name"],
#             "carImage": car["image"] or "",
#             "carType":  car["type"],
#             "price":    total_price,
#             "days":     days,
#             "status":   "Booked",
#             "date":     str(date.today()),
#         }
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.patch("/api/bookings/{booking_id}/cancel")
# def cancel_booking(booking_id: int):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute(
#             "SELECT car_id, status FROM bookings WHERE id = %s",
#             (booking_id,)
#         )
#         booking = cursor.fetchone()
#         if not booking:
#             raise HTTPException(status_code=404, detail="Booking not found")
#         if booking["status"] == "Cancelled":
#             raise HTTPException(status_code=400, detail="Already cancelled")
#
#         cursor.execute(
#             "UPDATE bookings SET status='Cancelled' WHERE id=%s",
#             (booking_id,)
#         )
#         cursor.execute(
#             "UPDATE cars SET available=1, status='Available' WHERE id=%s",
#             (booking["car_id"],)
#         )
#         db.commit()
#         return {"message": "Booking cancelled", "car_id": booking["car_id"]}
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.patch("/api/bookings/{booking_id}")
# def patch_booking_status(booking_id: int, data: StatusUpdateModel):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         cursor.execute(
#             "UPDATE bookings SET status=%s WHERE id=%s",
#             (data.status, booking_id)
#         )
#         db.commit()
#         return {"message": "Status updated"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.put("/api/bookings/{booking_id}")
# def update_booking(booking_id: int, data: BookingUpdateModel):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         cursor.execute(
#             """UPDATE bookings SET
#                user_name=%s, user_phone=%s, car_name=%s,
#                pickup=%s, drop_loc=%s,
#                from_date=%s, to_date=%s,
#                price=%s, status=%s
#                WHERE id=%s""",
#             (
#                 data.customer, data.phone, data.car,
#                 data.pickup,   data.drop,
#                 data.from_,    data.to,
#                 data.amount,   data.status,
#                 booking_id
#             )
#         )
#         db.commit()
#         return {"message": "Booking updated"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.delete("/api/bookings/{booking_id}")
# def delete_booking(booking_id: int):
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT car_id FROM bookings WHERE id=%s", (booking_id,))
#         row = cursor.fetchone()
#         if row:
#             cursor.execute(
#                 "UPDATE cars SET available=1, status='Available' WHERE id=%s",
#                 (row["car_id"],)
#             )
#         cursor.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
#         db.commit()
#         return {"message": "Booking deleted"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# # ══════════════════════════════════════════════════════════════
# #  ADMIN ROUTES — TABLE: users
# # ══════════════════════════════════════════════════════════════
#
# @app.get("/admin/users")
# def get_users():
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     try:
#         cursor.execute(
#             "SELECT id, name, email, phone, city, created_at FROM users ORDER BY id DESC"
#         )
#         users = cursor.fetchall()
#         for u in users:
#             if u.get("created_at") and not isinstance(u["created_at"], str):
#                 u["created_at"] = str(u["created_at"])
#         return users
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.put("/admin/update-user")
# def admin_update_user(data: AdminUserUpdateModel):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         cursor.execute(
#             "UPDATE users SET name=%s, email=%s, phone=%s, city=%s WHERE id=%s",
#             (data.name, data.email, data.phone, data.city, data.id)
#         )
#         db.commit()
#         return {"message": "User updated"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.delete("/admin/delete-user/{user_id}")
# def admin_delete_user(user_id: int):
#     db = get_db()
#     cursor = db.cursor()
#     try:
#         cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
#         db.commit()
#         return {"message": "User deleted"}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close(); db.close()
#
#
# @app.get("/")
# def root():
#     return {"status": "DriveEase Backend Running ✅", "port": 8000}
"""
DriveEase Car Rental — FastAPI Backend (FULLY FIXED)
INSTALL:  pip install fastapi uvicorn mysql-connector-python
RUN:      uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",          # ← உங்கள் MySQL password
    "database": "carrental"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def safe_str(val):
    if val is None:
        return None
    if hasattr(val, 'isoformat'):
        return str(val)
    return val


# ══════════════════════════════════════════════════════════════
#  PYDANTIC MODELS
# ══════════════════════════════════════════════════════════════

class RegisterModel(BaseModel):
    email:    str
    password: str
    name:     Optional[str] = ""
    phone:    Optional[str] = ""
    city:     Optional[str] = ""

class LoginModel(BaseModel):
    email:    str
    password: str

class ForgotPasswordModel(BaseModel):
    email:        str
    new_password: str

class ProfileUpdateModel(BaseModel):
    id:    int
    name:  Optional[str] = ""
    phone: Optional[str] = ""
    city:  Optional[str] = ""

class CarModel(BaseModel):
    name:         str
    brand:        Optional[str]   = ""
    type:         Optional[str]   = "Sedan"
    fuel:         Optional[str]   = "Petrol"
    seats:        Optional[int]   = 5
    transmission: Optional[str]   = "Manual"
    price:        Optional[int]   = 0
    status:       Optional[str]   = "Available"
    plate:        Optional[str]   = ""
    year:         Optional[int]   = 2022
    img:          Optional[str]   = "🚗"
    rating:       Optional[float] = 4.5
    reviews:      Optional[int]   = 0
    available:    Optional[bool]  = True
    features:     Optional[str]   = ""
    image:        Optional[str]   = ""
    description:  Optional[str]   = ""

class BookingModel(BaseModel):
    userId:    int
    carId:     int
    days:      Optional[int] = 1
    pickup:    Optional[str] = "Chennai"
    drop:      Optional[str] = "Chennai"
    from_date: Optional[str] = None
    to_date:   Optional[str] = None
    status:    Optional[str] = "Booked"

class BookingUpdateModel(BaseModel):
    customer: Optional[str] = ""
    phone:    Optional[str] = ""
    car:      Optional[str] = ""
    pickup:   Optional[str] = "Chennai"
    drop:     Optional[str] = "Chennai"
    from_:    Optional[str] = None
    to:       Optional[str] = None
    amount:   Optional[int] = 0
    status:   Optional[str] = "Pending"

class StatusUpdateModel(BaseModel):
    status: str

class AdminUserUpdateModel(BaseModel):
    id:    int
    name:  Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    city:  Optional[str] = ""


# ══════════════════════════════════════════════════════════════
#  USER ROUTES
# ══════════════════════════════════════════════════════════════

@app.post("/users/registration1")
def register(data: RegisterModel):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        cursor.execute(
            "INSERT INTO users (name, email, password, phone, city) VALUES (%s, %s, %s, %s, %s)",
            (data.name, data.email, data.password, data.phone, data.city)
        )
        db.commit()
        return {"message": "Registration successful", "user_id": cursor.lastrowid}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.post("/users/login1")
def login(data: LoginModel):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email, phone, city FROM users WHERE email = %s AND password = %s",
            (data.email, data.password)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return {"message": "Login successful", "user": user}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.put("/users/forgot-password")
def forgot_password(data: ForgotPasswordModel):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Email not found")
        cursor.execute(
            "UPDATE users SET password = %s WHERE email = %s",
            (data.new_password, data.email)
        )
        db.commit()
        return {"message": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.put("/api/profile")
def update_profile(data: ProfileUpdateModel):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "UPDATE users SET name=%s, phone=%s, city=%s WHERE id=%s",
            (data.name, data.phone, data.city, data.id)
        )
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        # Return updated user
        cursor.execute(
            "SELECT id, name, email, phone, city FROM users WHERE id=%s",
            (data.id,)
        )
        updated_user = cursor.fetchone()
        return {"message": "Profile updated successfully", "user": updated_user}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.get("/api/my-bookings/{user_id}")
def my_bookings(user_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT
                b.id,
                b.car_id    AS carId,
                b.car_name  AS carName,
                b.car_type  AS carType,
                b.car_image AS carImage,
                b.car_brand AS carBrand,
                b.days,
                b.price,
                b.status,
                b.pickup,
                b.drop_loc  AS dropLoc,
                b.from_date AS fromDate,
                b.to_date   AS toDate,
                b.created_at AS date
               FROM bookings b
               WHERE b.user_id = %s
               ORDER BY b.created_at DESC""",
            (user_id,)
        )
        rows = cursor.fetchall()
        result = []
        for r in rows:
            result.append({
                "id":       r["id"],
                "carId":    r["carId"],
                "carName":  r["carName"]  or "",
                "carType":  r["carType"]  or "",
                "carImage": r["carImage"] or "",
                "days":     r["days"]     or 1,
                "price":    r["price"]    or 0,
                "status":   r["status"]   or "Booked",
                "pickup":   r["pickup"]   or "",
                "date":     safe_str(r["date"]) or str(date.today()),
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


# ══════════════════════════════════════════════════════════════
#  CARS ROUTES
# ══════════════════════════════════════════════════════════════

@app.get("/api/cars")
def get_cars(available: Optional[bool] = None):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        if available is None:
            cursor.execute("SELECT * FROM cars ORDER BY id")
        else:
            cursor.execute(
                "SELECT * FROM cars WHERE available=%s ORDER BY id",
                (1 if available else 0,)
            )
        cars = cursor.fetchall()
        result = []
        for c in cars:
            if isinstance(c.get("features"), str):
                c["features"] = [f.strip() for f in c["features"].split(",") if f.strip()]
            c["available"] = bool(c.get("available"))
            c["rating"]    = float(c.get("rating") or 4.5)
            result.append(c)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.get("/api/cars/{car_id}")
def get_car(car_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        if isinstance(car.get("features"), str):
            car["features"] = [f.strip() for f in car["features"].split(",") if f.strip()]
        car["available"] = bool(car.get("available"))
        car["rating"]    = float(car.get("rating") or 4.5)
        return car
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.post("/api/cars")
def add_car(data: CarModel):
    db = get_db()
    cursor = db.cursor()
    try:
        features_str = data.features if isinstance(data.features, str) else ",".join(data.features or [])
        cursor.execute(
            """INSERT INTO cars
               (name,brand,type,fuel,seats,transmission,price,status,
                plate,year,img,rating,reviews,available,features,image,description)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (data.name, data.brand, data.type, data.fuel, data.seats,
             data.transmission, data.price, data.status, data.plate,
             data.year, data.img, data.rating, data.reviews,
             1 if data.available else 0,
             features_str, data.image, data.description)
        )
        db.commit()
        return {"message": "Car added", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.put("/api/cars/{car_id}")
def update_car(car_id: int, data: CarModel):
    db = get_db()
    cursor = db.cursor()
    try:
        features_str = data.features if isinstance(data.features, str) else ",".join(data.features or [])
        cursor.execute(
            """UPDATE cars SET
               name=%s, brand=%s, type=%s, fuel=%s, seats=%s,
               transmission=%s, price=%s, status=%s, plate=%s,
               year=%s, img=%s, rating=%s, reviews=%s,
               available=%s, features=%s, image=%s, description=%s
               WHERE id=%s""",
            (data.name, data.brand, data.type, data.fuel, data.seats,
             data.transmission, data.price, data.status, data.plate,
             data.year, data.img, data.rating, data.reviews,
             1 if data.available else 0,
             features_str, data.image, data.description, car_id)
        )
        db.commit()
        return {"message": "Car updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.delete("/api/cars/{car_id}")
def delete_car(car_id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
        db.commit()
        return {"message": "Car deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


# ══════════════════════════════════════════════════════════════
#  BOOKINGS ROUTES
# ══════════════════════════════════════════════════════════════

@app.get("/api/bookings")
def get_bookings():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT
                b.id,
                b.user_id,
                b.car_id,
                b.user_name  AS customer,
                b.user_email AS userEmail,
                b.user_phone AS phone,
                b.car_name   AS car,
                b.car_type   AS carType,
                b.car_image  AS carImage,
                b.car_brand  AS carBrand,
                b.pickup,
                b.drop_loc   AS dropLoc,
                b.from_date  AS fromDate,
                b.to_date    AS toDate,
                b.days,
                b.price      AS amount,
                b.status,
                b.created_at AS createdAt
               FROM bookings b
               ORDER BY b.created_at DESC"""
        )
        rows = cursor.fetchall()
        result = []
        for r in rows:
            result.append({
                "id":         r["id"],
                "user_id":    r["user_id"],
                "car_id":     r["car_id"],
                "customer":   r["customer"]  or "",
                "userEmail":  r["userEmail"] or "",
                "phone":      r["phone"]     or "",
                "car":        r["car"]       or "",
                "carType":    r["carType"]   or "",
                "carImage":   r["carImage"]  or "",
                "carBrand":   r["carBrand"]  or "",
                "pickup":     r["pickup"]    or "",
                "dropLoc":    r["dropLoc"]   or "",
                "fromDate":   safe_str(r["fromDate"]),
                "toDate":     safe_str(r["toDate"]),
                "days":       r["days"]      or 1,
                "amount":     r["amount"]    or 0,
                "status":     r["status"]    or "Booked",
                "createdAt":  safe_str(r["createdAt"]),
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.post("/api/bookings")
def create_booking(data: BookingModel):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        # 1. User fetch
        cursor.execute(
            "SELECT id, name, email, phone FROM users WHERE id = %s",
            (data.userId,)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 2. Car fetch
        cursor.execute(
            "SELECT id, name, type, image, brand, price, available FROM cars WHERE id = %s",
            (data.carId,)
        )
        car = cursor.fetchone()
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        if not car["available"]:
            raise HTTPException(status_code=400, detail="Car is not available")

        # 3. Duplicate check
        cursor.execute(
            "SELECT id FROM bookings WHERE user_id=%s AND car_id=%s AND status='Booked'",
            (data.userId, data.carId)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Already booked this car")

        # 4. Calculate price
        days        = max(1, data.days or 1)
        total_price = int(car["price"]) * days

        # 5. Insert booking
        cursor.execute(
            """INSERT INTO bookings
               (user_id, car_id,
                user_name, user_email, user_phone,
                car_name, car_type, car_image, car_brand,
                pickup, drop_loc,
                from_date, to_date,
                days, price, status)
               VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s, %s,%s, %s,%s, %s,%s,%s)""",
            (
                data.userId, data.carId,
                user["name"]  or "", user["email"] or "", user["phone"] or "",
                car["name"]   or "", car["type"]   or "", car["image"]  or "", car["brand"] or "",
                data.pickup   or "Chennai",
                data.drop     or "Chennai",
                data.from_date or str(date.today()),
                data.to_date   or str(date.today()),
                days, total_price, "Booked"
            )
        )
        booking_id = cursor.lastrowid

        # 6. Mark car unavailable
        cursor.execute(
            "UPDATE cars SET available=0, status='Rented' WHERE id=%s",
            (data.carId,)
        )
        db.commit()

        # 7. Return EXACT fields frontend expects
        return {
            "id":       booking_id,
            "carId":    data.carId,
            "carName":  car["name"]  or "",
            "carImage": car["image"] or "",
            "carType":  car["type"]  or "",
            "price":    total_price,
            "days":     days,
            "status":   "Booked",
            "date":     str(date.today()),
            "message":  "Booking successful",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.patch("/api/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT car_id, status FROM bookings WHERE id = %s",
            (booking_id,)
        )
        booking = cursor.fetchone()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking["status"] == "Cancelled":
            raise HTTPException(status_code=400, detail="Already cancelled")

        cursor.execute(
            "UPDATE bookings SET status='Cancelled' WHERE id=%s",
            (booking_id,)
        )
        cursor.execute(
            "UPDATE cars SET available=1, status='Available' WHERE id=%s",
            (booking["car_id"],)
        )
        db.commit()
        return {"message": "Booking cancelled", "car_id": booking["car_id"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.patch("/api/bookings/{booking_id}")
def patch_booking_status(booking_id: int, data: StatusUpdateModel):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE bookings SET status=%s WHERE id=%s",
            (data.status, booking_id)
        )
        db.commit()
        return {"message": "Status updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.put("/api/bookings/{booking_id}")
def update_booking(booking_id: int, data: BookingUpdateModel):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """UPDATE bookings SET
               user_name=%s, user_phone=%s, car_name=%s,
               pickup=%s, drop_loc=%s,
               from_date=%s, to_date=%s,
               price=%s, status=%s
               WHERE id=%s""",
            (
                data.customer, data.phone, data.car,
                data.pickup, data.drop,
                data.from_, data.to,
                data.amount, data.status,
                booking_id
            )
        )
        db.commit()
        return {"message": "Booking updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT car_id FROM bookings WHERE id=%s", (booking_id,))
        row = cursor.fetchone()
        if row:
            cursor.execute(
                "UPDATE cars SET available=1, status='Available' WHERE id=%s",
                (row["car_id"],)
            )
        cursor.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
        db.commit()
        return {"message": "Booking deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


# ══════════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ══════════════════════════════════════════════════════════════

@app.get("/admin/users")
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email, phone, city, created_at FROM users ORDER BY id DESC"
        )
        users = cursor.fetchall()
        for u in users:
            if u.get("created_at"):
                u["created_at"] = safe_str(u["created_at"])
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.put("/admin/update-user")
def admin_update_user(data: AdminUserUpdateModel):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE users SET name=%s, email=%s, phone=%s, city=%s WHERE id=%s",
            (data.name, data.email, data.phone, data.city, data.id)
        )
        db.commit()
        return {"message": "User updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.delete("/admin/delete-user/{user_id}")
def admin_delete_user(user_id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        db.commit()
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close(); db.close()


@app.get("/")
def root():
    return {"status": "DriveEase Backend Running ✅", "port": 8000}