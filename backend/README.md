# API Documentation

## Search Courses by Criteria

**Method:** `POST`
**Endpoint:** `/courses/search`
**Tags:** `courses`

---

#### Description

Find courses based on the user’s specified domain, current skill level, and desired skills.

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
| `current_level`  | string | yes      | The user’s current skill level: `"beginner"`, `"intermediate"`, or `"advanced"`. |
| `desired_skills` | string | yes      | Specific skills the user wants to acquire (e.g., `"FastAPI"`, `"illustration"`). |

<details>
<summary><strong>Example Request</strong></summary>

```json
POST /courses/search
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

A JSON array of matching courses (may be empty).

**Course Object**

| Field        | Type      | Description                                                                  |
| ------------ | --------- | ---------------------------------------------------------------------------- |
| `id`         | integer   | Unique identifier of the course.                                             |
| `cover_url`  | string    | URL to the course cover image.                                               |
| `title`      | string    | Course title.                                                                |
| `duration`   | integer   | Course duration in hours.                                                    |
| `difficulty` | string    | Difficulty level: `"easy"`, `"medium"`, or `"hard"`.                         |
| `price`      | integer   | Price of the course in the specified currency.                               |
| `pupils_num` | integer   | Number of enrolled pupils.                                                   |
| `authors`    | string\[] | List of author names. May be empty if author details are fetched separately. |
| `rating`     | integer   | Course rating on a scale of 0–5.                                             |
| `url`        | string    | URL to the course page.                                                      |

<details>
<summary><strong>Example Response</strong></summary>

```json
[
  {
    "id": 1,
    "cover_url": "https://example.com/images/course1.jpg",
    "title": "FastAPI for Beginners",
    "duration": 5,
    "difficulty": "easy",
    "price": 0,
    "pupils_num": 120,
    "authors": ["Ivan Ivanov"],
    "rating": 5,
    "url": "https://example.com/course/1"
  },
  {
    "id": 2,
    "cover_url": "https://example.com/images/course2.jpg",
    "title": "Complete Python Course",
    "duration": 40,
    "difficulty": "medium",
    "price": 12000,
    "pupils_num": 850,
    "authors": ["Maria Petrova", "Sergey Sidorov"],
    "rating": 4,
    "url": "https://example.com/course/2"
  }
]
```

</details>

---

##### 422 Unprocessable Entity

Validation error in the request body (e.g., missing required field or wrong data type).

<details>
<summary><strong>Example Error Response</strong></summary>

```json
{
  "detail": [
    {
      "loc": ["body", "current_level"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

</details>

## Fetch popular courses


**Method:** `GET`
**Endpoint:** `/courses/popular`
**Tags:** `courses`

---

#### Description

Returns several popular courses.


#### Example Response

```json
[
        {
            "id": 10,
            "cover_url": "https://avatars.mds.yandex.net/i?id=a5be1a85e5edf3a1d698f82857ed4926_l-5332940-images-thumbs&n=13",
            "title": "Mastering Python",
            "duration": 40,
            "difficulty": "medium",
            "price": 2500,
            "pupils_num": 1200,
            "authors": ["Alice Ivanova"],
            "rating": 5,
            "url": "https://example.com/course/10"
        },
        {
            "id": 22,
            "cover_url": "https://avatars.mds.yandex.net/i?id=a5be1a85e5edf3a1d698f82857ed4926_l-5332940-images-thumbs&n=13",
            "title": "Advanced FastAPI",
            "duration": 16,
            "difficulty": "hard",
            "price": 3500,
            "pupils_num": 800,
            "authors": ["Bob Petrov", "Carol Smirnov"],
            "rating": 5,
            "url": "https://example.com/course/22"
        }
    ]
```

##### 200 OK

---
