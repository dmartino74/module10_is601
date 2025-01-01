# **Module 9: Databases and Web Applications**

## **Module Overview**

In **Module 9**, you will learn how to integrate and manage a **PostgreSQL** database within a containerized environment using **Docker Compose**. You will interact with the database through **pgAdmin**, leveraging raw **SQL** commands to create tables and insert, query, update, and delete records. This approach ensures that you gain hands-on experience with fundamental SQL operations before transitioning to more advanced techniques (such as ORMs) in future modules.

By completing this module, you will fulfill the following **Course Learning Outcomes (CLOs)**:

- **CLO 10:** Apply containerization techniques to containerize applications using Docker.  
- **CLO 12:** Integrate Python programs with SQL databases to create and manipulate data.

---

## **Videos**

1. **Overview Video (on Canvas):**  
   - Explains how **Docker Compose** can spin up multiple services (FastAPI, PostgreSQL, pgAdmin).  
   - Introduces **pgAdmin** for visually inspecting and interacting with your database.

2. **Hands-On Video (on Canvas):**  
   - Demonstrates the process of running **SQL** commands in pgAdmin to create tables, insert data, and query results.  
   - Provides an example of verifying inserted records by running various **SELECT** statements.

---

## **Why Databases in a Containerized Environment?**

Running a database in a container alongside your application ensures **consistent, reproducible** setups for local development, testing, and potential deployment. Specifically:

- **Isolation and Portability:** Containers encapsulate all dependencies, making it easier for different team members to match development environments.  
- **pgAdmin Convenience:** A graphical interface allows you to easily write and execute SQL commands without installing PostgreSQL natively on your machine.

---

## **Learning Pathway**

### **Recall**

**Title:** SQL Basics in a Dockerized PostgreSQL  
**Grading Type:** Points  
**Instructions:**  

1. **Reflect on Any Past Database Experience:**  
   - Have you previously used SQL in a non-containerized setting?  
   - What benefits might containerization bring compared to running a local database install?

2. **Discussion Prompt:**  
   - Considering you’ll write raw SQL in pgAdmin, how might this experience deepen your understanding of relational database structures?

**Purpose:** These prompts will help you connect previous knowledge (if any) to the container-based setup you’ll be using in this module.

---

### **Step-by-Step Guide: Docker Compose, pgAdmin, and SQL**

1. **Inspect and Run Docker Compose**  
   - Ensure `docker-compose.yml` defines:  
     - A **web** service (FastAPI).  
     - A **db** service (PostgreSQL).  
     - Optionally, a **pgadmin** service for graphical DB management.  
   - Run `docker-compose up --build` to start all containers.

2. **Access pgAdmin**  
   - Usually available at [http://localhost:5050](http://localhost:5050).  
   - Login credentials and connection details are set in `docker-compose.yml` (commonly `postgres` / `postgres`).

3. **Create and Explore a Database**  
   - Use pgAdmin to connect to your PostgreSQL container.  
   - Confirm that you can see (or create) a database (e.g., `fastapi_db`).

4. **Execute SQL Commands**  
   - Open pgAdmin’s **Query Tool**.  
   - Run provided SQL statements to create tables, insert records, update records, query data, and delete data.

---

## **Hands-On Assignment**

**Title:** Working with Raw SQL in pgAdmin  
**Grading Type:** Points  

**Instructions**:  

1. **Set Up Your Environment**  
   - Clone the FastAPI Calculator repository (or project) with a `docker-compose.yml` already configured for FastAPI + PostgreSQL + (optional) pgAdmin.  
   - Run `docker-compose up --build`.  
   - Confirm you can access **pgAdmin** at [http://localhost:5050](http://localhost:5050).

2. **Open pgAdmin Query Tool**  
   - Connect to the PostgreSQL server (host `db`, user `postgres`, or as defined in Compose).  
   - Select your target database (e.g., `fastapi_db`).

3. **Follow These SQL Steps**  
   **(A) Create Tables**  
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       email VARCHAR(100) NOT NULL UNIQUE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE calculations (
       id SERIAL PRIMARY KEY,
       operation VARCHAR(20) NOT NULL,
       operand_a FLOAT NOT NULL,
       operand_b FLOAT NOT NULL,
       result FLOAT NOT NULL,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       user_id INTEGER NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
   );
   ```
   **(B) Insert Records**  
   ```sql
   INSERT INTO users (username, email) 
   VALUES 
   ('alice', 'alice@example.com'), 
   ('bob', 'bob@example.com');

   INSERT INTO calculations (operation, operand_a, operand_b, result, user_id)
   VALUES
   ('add', 2, 3, 5, 1),
   ('divide', 10, 2, 5, 1),
   ('multiply', 4, 5, 20, 2);
   ```
   **(C) Query Data**  
   ```sql
   -- Retrieve all users
   SELECT * FROM users;

   -- Retrieve all calculations
   SELECT * FROM calculations;

   -- Join users and calculations
   SELECT u.username, c.operation, c.operand_a, c.operand_b, c.result
   FROM calculations c
   JOIN users u ON c.user_id = u.id;
   ```
   **(D) Update a Record**  
   ```sql
   UPDATE calculations
   SET result = 6
   WHERE id = 1;  -- or whichever row you want to update
   ```
   **(E) Delete a Record**  
   ```sql
   DELETE FROM calculations
   WHERE id = 2;  -- example record to remove
   ```

4. **Document Your Outputs**  
   - For **each** SQL command above, take a **screenshot** of the pgAdmin output window showing the query and result (e.g., “Query returned successfully: X rows affected”).  
   - Compile these screenshots into a **Word document** (or PDF) with brief captions indicating what each screenshot shows.

5. **Submit**  
   - Your **Word document** (or PDF) containing screenshots of successful table creation, insertion, querying, update, and deletion steps.  
   - A short (2-3 paragraph) explanation of any challenges you encountered and how you solved them.

---

## **Reflect**

**Title:** Module 9 Reflection  
**Grading Type:** Points  
**Instructions:**  
Write **600-700 words** on the following:

1. **Containerization (CLO 10):** How did Docker Compose simplify running your database (PostgreSQL) alongside FastAPI?  
2. **Basic Database Integration (CLO 12):** Discuss your comfort with raw SQL operations in pgAdmin. Do you see the value in knowing SQL even if you later use an ORM?  
3. **Challenges and Insights:** Note any tricky aspects (e.g., port conflicts, user permissions, SQL syntax errors) and how you overcame them.  
4. **Looking Ahead:** How might this experience influence your approach to more advanced database tasks in later modules (e.g., migrations, advanced joins, indexing)?

---

## **Quiz**

**Title:** PostgreSQL & Raw SQL Quiz  
**Grading Type:** Points  

**Instructions**:

1. **Complete the Quiz on Canvas**, focusing on:  
   - Docker Compose fundamentals (managing multiple containers).  
   - Basic SQL operations (`CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`).  
   - Understanding of one-to-many relationships and foreign keys.  

2. **Question Types**:  
   - **Multiple Choice:** Identify correct Docker Compose or SQL usage.  
   - **Short Answer:** Write or explain simple SQL queries (e.g., join, insert).  

---

## **Supplementary Materials**

- **[Docker Documentation](https://docs.docker.com/compose/)**  
  *Refine your knowledge on multi-container orchestration.*  
- **[PostgreSQL Official Docs](https://www.postgresql.org/docs/)**  
  *Explore deeper into indexing, functions, and database performance.*  
- **[pgAdmin Documentation](https://www.pgadmin.org/docs/)**  
  *Leverage advanced pgAdmin features for backups, user management, etc.*  
- **[SQL Tutorial](https://www.w3schools.com/sql/)**  
  *Practice more advanced queries, subqueries, and joins.*  


---

## **Tips for Success**

1. **Follow the Queries Step-by-Step:** Running the SQL statements in order ensures you don’t miss any foreign key dependencies.  
2. **Check Query Outputs:** Watch for syntax errors or missed commas that can prevent queries from running.  
3. **Container Logs:** If PostgreSQL won’t start or connect, inspect logs via `docker-compose logs db`.  
4. **Organize Screenshots Clearly:** Label each screenshot (e.g., “Fig 1: CREATE TABLE users success output”).  
5. **Ask for Help:** If you’re unsure, consult official docs or your peers for quick guidance.

---

## **Submission Deadline**

Please upload your **Word document** (or PDF) with all required screenshots and your **Module 9 Reflection** by **[Insert Deadline Here]**. Late submissions may incur penalties in line with course policy.

---

**Congratulations!** You’ve successfully created and managed tables in a **containerized** PostgreSQL database, executing **raw SQL** commands via **pgAdmin**. These core skills will prove invaluable as you move on to more sophisticated database interactions in future modules.
