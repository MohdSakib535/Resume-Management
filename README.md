# 🚀 FastAPI Resume Management System

This is a **FastAPI-based Resume Management System** with PostgreSQL as the database and Alembic for handling migrations.

## 📌 Features
- User authentication & resume management
- PostgreSQL & Alembic for database migrations
- Dockerized setup for easy deployment
- API documentation with **Swagger UI** (`/docs`)

---

## 📌 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### **2️⃣ Create & Activate a Virtual Environment (Optional)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure `.env` File**
Create a `.env` file inside the project and add:

```ini
DATABASE_URL=postgresql://fastapi_user:fastapi_password@postgres_db:5432/fastapi_db
```



## 📌 Register PostgreSQL Server in pgAdmin  
To connect pgAdmin to the PostgreSQL database running in Docker, follow these steps:

### **1️⃣ Open pgAdmin**
- Go to **pgAdmin** in your browser:  
  👉 **[http://127.0.0.1:5050/browser/](http://127.0.0.1:5050/browser/)**
- **Log in** with the credentials from `docker-compose.yml`:
  - **Email:** `admin@example.com`
  - **Password:** `admin`

---

### **2️⃣ Register a New PostgreSQL Server**
1. In **pgAdmin**, right-click on **"Servers" → Click "Create" → "Server"**  
2. **Under the "General" tab**:
   - **Name:** `PostgreSQL-Docker` (or any name you prefer)

3. **Under the "Connection" tab**:
   - **Host name/address:** `postgres_db`  *(same as service name in `docker-compose.yml`)*
   - **Port:** `5432`
   - **Maintenance database:** `fastapi_db`
   - **Username:** `fastapi_user`
   - **Password:** `fastapi_password`
   - ✅ **Click "Save"**

---

### **3️⃣ Verify the Connection**
- If the connection is successful, you will see **PostgreSQL-Docker** listed in pgAdmin.  
- Expand the database to explore tables and schemas.

---

### **📌 Troubleshooting**
❌ **Getting a connection error?**  
✔ Ensure PostgreSQL is running inside Docker:
```bash
docker ps
---

## 📌 Running the Application with Docker

### **1️⃣ Start the Docker Containers**
```bash
docker-compose up --build -d
```
- **FastAPI runs on:** `http://localhost:8000`
- **Swagger API Docs:** `http://localhost:8000/docs`
- **PostgreSQL:** `localhost:5432`
- **pgAdmin:** `http://localhost:5050` (Login: `admin@example.com`, Password: `admin`)

### **2️⃣ Apply Alembic Migrations**
```bash
   if migrations file is deleted and start from initial
      docker exec -it fastapi_app alembic revision --autogenerate -m "Initial migration"
      docker exec -it fastapi_app alembic upgrade head
   
   if migrations files is not deleted so run only upgrade cmd
      docker exec -it fastapi_app alembic upgrade head  (use this if u not delete anything)
      
    


```

### **3️⃣ Verify Database Migrations**
Enter PostgreSQL:
```bash
docker exec -it postgres_db psql -U fastapi_user -d fastapi_db
```
Then, run:
```sql
\dt;  -- List tables
SELECT * FROM alembic_version;
```

---

## 📌 API Endpoints

| **Endpoint** | **Method** | **Description** |
|-------------|-----------|-----------------|
| `/docs` | `GET` | 📜 Swagger API Documentation |
| `/users/create` | `POST` | 📝 Register a new user |
| `/users/all` | `GET` | 📝  Get all  user |
| `/users/{user_id}` | `GET` | 📝  Get particular user data with id |
| `/auth/login` | `POST` | 🔑 User login & JWT token generation |
| `/resume/create` | `POST` | 📄 Create a new resume |
| `/resume/all-details` | `GET` | 📂 Get all resumes details |
| `/resume/skills` | `GET` | 📂 Get all resumes details with skills |
| `/resume/experience` | `GET` | 📂 Get all resumes details with Experience |
| `/resume/education` | `GET` | 📂 Get all resumes details with Education |

| `/resume/update/{resume_id}` | `PUT` | ✏️ Update an existing resume |
| `/resume/delete/{resume_id}` | `DELETE` | ❌ Delete a resume |
| `/resume/search?skill=Python&role=Software Engineer` | `GET` | 🔎 Search resumes with filters |

---

## 📌 Stopping and Removing Containers
```bash
docker-compose down -v
```


---

## 📌 Troubleshooting
❓ **Facing Alembic connection issues?**  
- Ensure `DATABASE_URL` **uses `postgres_db` instead of `localhost`**.
- Check if PostgreSQL is running:  
  ```bash
  docker ps
  ```

❓ **Cannot access Swagger UI?**  
- Ensure FastAPI is running:
  ```bash
  docker logs fastapi_app -f
  ```

---

## 📌 Contributing
- Fork this repository
- Create a feature branch (`git checkout -b feature-branch`)
- Commit your changes (`git commit -m "Add new feature"`)
- Push to GitHub (`git push origin feature-branch`)
- Open a **Pull Request (PR)** 🚀

---

## 📌 License
📜 This project is licensed under the **MIT License**.
