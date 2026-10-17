# DocPro — Asynchronous Document Processing API

DocPro is a backend-focused document-processing API built with Django REST Framework. It allows clients to upload documents and process them asynchronously using Celery and Redis, while PostgreSQL stores document metadata, processing status, and results.

The project focuses on practical backend engineering concepts, including REST API development, background jobs, database management, error handling, and reliable task processing.

## Features

- **Document Upload:** Accept files through a REST API.
- **File Validation:** Validate uploaded file size using Django REST Framework serializers.
- **Asynchronous Processing:** Delegate document processing to Celery workers.
- **Word Count:** Calculate the total number of words in supported text files.
- **Word Frequency Analysis:** Count the occurrences of individual words.
- **Processing Status:** Track document lifecycle states.
- **Error Handling:** Record processing errors for failed jobs.
- **Database Persistence:** Store document metadata and processing results in PostgreSQL.
- **Background Job Monitoring:** Track processing timestamps and develop recovery mechanisms for stuck jobs.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST API development |
| PostgreSQL | Persistent database |
| Celery | Asynchronous task execution |
| Redis | Celery message broker |
| Docker | Containerized development environment |
| Git | Version control |

## Architecture

```text
                Client / Postman
                       |
                       v
             Django REST Framework
                       |
                       v
               File Validation
                       |
                       v
            Save Document in Database
                       |
                       v
               Queue Celery Task
                       |
                       v
                 Redis Broker
                       |
                       v
                Celery Worker
                       |
                       v
             Read and Process File
                       |
                       v
           Calculate Word Frequencies
                       |
                       v
            Update PostgreSQL Record
                       |
                       v
             Retrieve Processing Result
```

PostgreSQL stores document metadata and processing results, while the uploaded file is stored through Django's file-storage system. Redis transports task messages to Celery workers; it is not the primary database for document records.

## Document Lifecycle

A document moves through the following states:

| Status | Description |
|---|---|
| `QUEUED` | The document has been saved and is awaiting processing. |
| `PROCESSING` | A worker has started processing the document. |
| `DONE` | Processing completed successfully, according to the current model's status choices. |
| `FAILED` | Processing failed and the error can be recorded. |

The processing start timestamp should be recorded when the Celery worker begins executing the task, rather than when the upload request is received.

## Project Setup

### Prerequisites

Install the following tools:

- Python and `venv`
- Git
- Docker
- PostgreSQL, either locally or through Docker
- Redis
- A REST API client such as Postman

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd docpro
```

### 2. Create and activate a virtual environment

On Linux or WSL Ubuntu:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If the project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Ensure Django, Django REST Framework, Celery, the Redis client, and the PostgreSQL database adapter are installed as required by the project.

### 4. Configure the database

Configure the PostgreSQL connection in Django settings or through environment variables, depending on the existing implementation.

Example environment variables:

```env
DB_NAME=docpro
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

These are example variable names; adjust them to match the project's actual settings.

If using the existing Docker PostgreSQL setup, start the appropriate database container before running migrations.

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Django development server

```bash
python manage.py runserver
```

### 7. Start Redis

Ensure Redis is running and accessible at the broker URL configured for Celery.

For a local Redis installation, the typical default URL is:

```text
redis://localhost:6379/0
```

### 8. Start the Celery worker

From the project root:

```bash
celery -A config worker --loglevel=info
```

This command assumes `config` is the Django project package and the Celery application is configured there.

Keep the worker running in a separate terminal. Django can accept requests while Celery processes tasks in the background.

## API Usage

### Upload a document

**Endpoint:** `POST /documents/upload/`

Confirm the exact URL in the project's URL configuration.

In Postman:

1. Select `POST`.
2. Enter the upload endpoint.
3. Open **Body → form-data**.
4. Add a key named `file`.
5. Change its type from Text to File.
6. Select a supported text file and send the request.

Allow Postman to set the multipart `Content-Type` header automatically.

Example response structure:

```json
{
  "id": 42,
  "status": "QUEUED",
  "message": "File uploaded; processing is queued."
}
```

This is an illustrative response for the intended upload flow. The actual response depends on the current view implementation.

### Processing Results

The Celery task reads the saved file, calculates the word count and word frequencies, and persists the results to the document record.

Example result structure:

```json
{
  "word_count": 4,
  "word_frequencies": {
    "hello": 2,
    "world": 1,
    "django": 1
  }
}
```

For the input:

```text
hello world
hello django
```

The expected total is four words.

The example shows the intended result structure; use the actual model field names when implementing or documenting a result-retrieval endpoint.

## Error Handling and Reliability

DocPro explores several important background-processing concerns:

- Tracking processing status and timestamps.
- Recording errors when tasks fail.
- Detecting jobs that remain in `PROCESSING` beyond an expected timeout.
- Understanding the difference between database transactions and message-broker delivery.
- Using Django's `transaction.on_commit()` to enqueue tasks after a successful database commit.
- Exploring scheduled recovery with Celery Beat.

A database transaction and a Redis message publication are not one atomic operation. For stronger delivery guarantees, a transactional outbox pattern can be introduced in a future iteration.

Automatic recovery, task retries, and monitoring should be considered complete only after they have been implemented and tested.

## Current Scope and Limitations

- Initial processing focuses on text files; PDF and other binary document formats require dedicated extraction logic.
- The upload size limit is intended to be 20 MB; verify the current serializer validation before relying on it.
- Redis and the Celery worker must be available for background tasks to execute.
- Production deployment, persistent object storage, comprehensive automated tests, and stronger task-delivery guarantees require further implementation and verification.

## Future Improvements

- Add document status and result retrieval endpoints.
- Implement reliable stale-job detection and recovery.
- Add task retries and idempotent processing.
- Use Celery Beat for scheduled maintenance.
- Add automated tests for uploads, validation, processing, and failures.
- Introduce structured logging and monitoring.
- Containerize the application, database, Redis, and worker with Docker Compose.
- Explore object storage such as Amazon S3 for uploaded documents.
- Deploy the application with a production-ready web server and appropriate security settings.

## Learning Objectives

DocPro is also a practical backend engineering project designed to strengthen understanding of:

- REST API design and validation.
- Django ORM and relational database modeling.
- Asynchronous execution and message brokers.
- Database transactions and concurrency.
- Background job lifecycle management.
- Failure recovery and system reliability.
- Docker-based development and deployment.

