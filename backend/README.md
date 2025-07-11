# API Documentation

## Configuration

### Deepseek API Setup

To enable enhanced search functionality with AI-generated queries, you need to configure the Deepseek API key.

Set the following environment variable:
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

If the API key is not configured, the system will use fallback queries based on the user input.

### Similarity Threshold

The system uses a similarity threshold to filter search results and ensure only relevant courses are returned.

**Default threshold:** 0.7 (70% similarity)

**Configuration options:**
1. **Environment variable:** Set `SIMILARITY_THRESHOLD=0.8` for 80% similarity
2. **Config file:** Modify `similarity_threshold` in `app/config.py`

**Threshold values:**
- `0.0` - No filtering (all results returned)
- `0.5` - Moderate filtering (50% similarity required)
- `0.7` - Default filtering (70% similarity required)
- `0.8` - Strict filtering (80% similarity required)
- `1.0` - Maximum filtering (100% similarity required)

**How it works:**
- Each search query generates a vector representation
- Course descriptions are also vectorized
- Cosine similarity is calculated between query and course vectors
- Only courses with similarity scores >= threshold are returned
- Results are logged to `logs/generated_queries.log` with similarity scores

## Search Courses by Criteria

**Method:** `POST`
**Endpoint:** `/courses/search`
**Tags:** `courses`

---

#### Description

Find courses based on the user's specified domain, current skill level, and desired skills. Results are filtered by similarity threshold to ensure relevance.

---

#### Request

**Headers**

```http
Content-Type: application/json
```

**JSON Body**

| Field            | Type   | Required | Description                                                                      |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------- |
| `area`           | string | yes      | The knowledge area the user wants to master (e.g., `"Python"`, `"Design"`).      |
| `current_level`  | string | yes      | The user's current skill level: `"beginner"`, `"intermediate"`, or `"advanced"`. |
| `desired_skills` | string | yes      | Specific skills the user wants to acquire (e.g., `"FastAPI"`, `"illustration"`). |

<details>
<summary><strong>Example Request</strong></summary>

```json
POST /api/courses/search
Content-Type: application/json

{
  "area": "Python",
  "current_level": "beginner",
  "desired_skills": "FastAPI"
}
```

</details>

---

#### Response

##### 200 OK

A JSON array of matching courses that meet the similarity threshold (may be empty if no courses are similar enough).

**Course Object**

| Field        | Type      | Description                                                                  |
| ------------ | --------- | ---------------------------------------------------------------------------- |
| `id`         | integer   | Unique identifier of the course.                                             |
| `title`      | string    | Course title.                                                                |
| `cover_url`  | string    | URL to course cover image.                                                   |
| `duration`   | integer   | Course duration in hours.                                                    |
| `difficulty` | string    | Course difficulty level.                                                     |
| `price`      | number    | Course price.                                                                |
| `currency_code` | string | Currency code for the price.                                             |
| `pupils_num` | integer   | Number of students enrolled.                                                 |
| `authors`    | string    | Course author(s).                                                            |
| `rating`     | integer   | Course rating (1-5).                                                         |
| `url`        | string    | Course URL.                                                                  |
| `description` | string   | Course description.                                                          |
| `summary`    | string    | Course summary.                                                              |
| `target_audience` | string | Target audience description.                                             |
| `acquired_skills` | string | Skills that will be acquired.                                            |
| `acquired_assets` | string | Assets that will be acquired.                                            |
| `title_en`   | string    | Course title in English.                                                     |
| `learning_format` | string | Learning format (e.g., "video", "text").                                |

<details>
<summary><strong>Example Response</strong></summary>

```json
[
  {
    "id": 12345,
    "title": "Python для начинающих",
    "cover_url": "https://stepik.org/media/cache/images/courses/12345/cover.jpg",
    "duration": 20,
    "difficulty": "beginner",
    "price": 0,
    "currency_code": "RUB",
    "pupils_num": 15000,
    "authors": "Иван Петров",
    "rating": 4,
    "url": "https://stepik.org/course/12345/promo",
    "description": "Курс по основам Python...",
    "summary": "Изучите основы Python...",
    "target_audience": "Начинающие программисты",
    "acquired_skills": "Python, программирование, алгоритмы",
    "acquired_assets": "Сертификат об окончании",
    "title_en": "Python for Beginners",
    "learning_format": "video"
  }
]
```

</details>

##### 404 Not Found

No courses found that meet the similarity threshold.

```json
{
  "detail": "Курсы не найдены"
}
```

##### 500 Internal Server Error

Server error occurred during search.

```json
{
  "detail": "Internal Server Error"
}
```

---

#### Logging

All search operations are logged to `logs/generated_queries.log` with:
- Generated search queries
- Similarity scores for each result
- Whether results passed the threshold
- Timestamps and user input

This helps with debugging and monitoring search quality.

## Fetch popular courses


**Method:** `GET`