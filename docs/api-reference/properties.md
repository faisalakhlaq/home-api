# Properties API

The Properties API allows managing real estate listings, including:

- [Listing](#list-properties)
- [Creation](#create-property)
- [Retrieval](#retrieve-property)
- [Updating]()
- [Fetch user favorite properties](#fetch-user-favorite-properties)
- [Add to favorite](#add-to-favorite)
- [Remove from favorite](#remove-from-favorite)
- [Fetch the data required to create a new property](#get-create-property-form-data)

##### Not allowed
- **deletion**: It is not allowed to delete a property

---

## List Properties

`GET api/v1/properties/properties/`

Retrieves a list of all available properties.

##### Query Parameters

| Parameter | Type   | Description                                       | Default   |
| :-------- | :----- | :------------------------------------------------ | :-------- |
| `min_price` | integer | Filters properties with a price greater than or equal to this value. | None      |
| `max_price` | integer | Filters properties with a price less than or equal to this value. | None      |
| `total_rooms`| integer | Filters properties by number of rooms.         | None      |
| `genre`    | integer | genre is same as type but it works with ids e.g. genre=1 will return all the `Property` objects that have type=1       | None         |
| `type`| str |  type works with the string types      | None        |
| `city`| str |  Filters the properties by city      | None        |
| `country`| str |  Filters the properties by country      | None        |

##### Example Request

```bash
curl -X GET "[http://localhost:8000/api/v1/properties/properties/?min_price=100000&total_rooms=2](http://127.0.0.1:8000/api/properties/properties/?min_price=100000&city=copenhagen)" \
     -H "Accept: application/json"
```

##### Example Response (200 OK)

```JSON
[
    {
        "id": 37,
        "type": "",
        "description": "",
        "created_at": "2025-07-02T09:19:34.680534Z",
        "price": 662806.0,
        "price_currency": "USD",
        "address": {
            "postal_code": "1332",
            "street": "Goce Delčev",
            "city": "Čaška"
        },
        "favorite": false
    },
    // ... more properties
]
```

## Create Property

```POST /api/v1/properties/properties/```

Creates a new property listing. Requires authentication using `Bearer Token`.

| Field            | Type          | Description | Required |
|------------------|---------------|-------------|----------|
| favorite_user    | ManyToOneRel  |             | False    |
| property_images  | ManyToOneRel  |             | False    |
| id | BigAutoField | Auto generated | False |
| created_at | DateTimeField | Auto generated | False |
| updated_at | DateTimeField | Auto generated | False |
| price | DecimalField | Price of the property. | True |
| price_currency | CharField | Provide the currency abbreviations for the price. (3-letter acronym for the currency). | True |
| area | FloatField | Coverd area of the property in square meters.The covered area of a property typically refers to the total indoor living area, including all rooms, hallways, and any other enclosed spaces within the structure. | True |
| total_area | FloatField | Total ground area of the property. The total ground space available refers to the entire area of land upon which the house is built, including any outdoor spaces such as yards, gardens, driveways, etc. | True |
| measured_area | FloatField |  | False |
| total_rooms | FloatField | Total number of rooms in the property. | False |
| toilets | IntegerField | Total number of toilets in the property. | False |
| construction_year | IntegerField | Year in which the property was built. | False |
| renovation_year | IntegerField | Year in which the property was built. | False |
| total_floors | IntegerField | Total number of floors and stories the property conprises of. | False |
| heating | CharField | e.g. Heating installation. e.g. Central heating with one heating unit. | True |
| outer_walls | CharField | e.g. Brick. | True |
| roof_type | CharField | e.g. Tile. | True |
| description | TextField |  | True |
| address | ForeignKey | Address of the property. | True |
| type | ForeignKey | Type | Genre of the property. | False |
| status | ForeignKey | Status of the property. | False |
| owner | ForeignKey | The user who created the property. | False |


##### Example Request

```bash
curl -X POST 'http://localhost:8000/api/v1/properties/properties/' \
--header 'Authorization: Bearer JIUz' \
--header 'Cookie: messages=W1siX19qc29uXx' \
--form 'address.street="Maršal Tito"' \
--form 'address.city="Kičevo"' \
--form 'address.region="R12"' \
--form 'address.postal_code="6250"' \
--form 'address.country="North Mecedonia"' \
--form 'price="50000"' \
--form 'price_currency="Euro"' \
--form 'area="110"' \
--form 'total_rooms="4"' \
--form 'description="Комфорен стан на...."' \
--form 'type="2"' \
--form 'status="10"' \
--form 'total_area="130"'
--form 'property_images[0]image=@"/Desktop/home images/763eb29d-1881-87e3-7144-7165b6320a24.jpeg"' \
```

##### Example Response

- **201 Created**: The successfully created.

```JSON
{
    "id": 38,
    "address": {
        "id": 38,
        "created_at": "2025-07-03T11:32:25.745451Z",
        "updated_at": "2025-07-03T11:32:25.745468Z",
        "street": "Maršal Tito",
        "city": "Kičevo",
        "region": "R12",
        "postal_code": "6250",
        "country": "North Mecedonia"
    },
    "property_images": [],
    "created_at": "2025-07-03T11:32:25.748161Z",
    "updated_at": "2025-07-03T11:32:25.748175Z",
    "price": 50000.0,
    "price_currency": "Euro",
    "area": 110.0,
    "total_area": 130.0,
    "measured_area": null,
    "total_rooms": 4.0,
    "toilets": null,
    "construction_year": null,
    "renovation_year": null,
    "total_floors": null,
    "heating": "",
    "outer_walls": "",
    "roof_type": "",
    "description": "Комфорен стан на...",
    "type": 2,
    "status": 10,
    "owner": 1
}
```

- **401 Unauthorized**: If authentication is required and not provided.
```JSON
{
    "detail": "Authentication credentials were not provided."
}
```

- **400 Bad Request**: Invalid query parameters.
```JSON
{
    "detail": "Invalid 'min_price' value."
}
```

<!-- - **403 Forbidden**: If the user does not have permission.
```JSON
{
    "detail": "Authentication credentials were not provided."
}
``` -->

## Retrieve Property

Get details of a property. Does not require authentication.

##### Example Request

```bash
curl --location 'http://localhost:8000/api/v1/properties/properties/1' \
--header 'Cookie: messages=W1siX19q55x'
```

##### Example Response

- **200 OK**
```JSON
{
    "id": 1,
    "type": "",
    "address": {
        "id": 1,
        "created_at": "2025-07-02T09:19:34.453185Z",
        "updated_at": "2025-07-02T09:19:34.453202Z",
        "street": "Vasil Glavinov 9",
        "city": "Skopje",
        "region": null,
        "postal_code": "1000",
        "country": "North Macedonia"
    },
    "property_images": [],
    "created_at": "2025-07-02T09:19:34.553925Z",
    "updated_at": "2025-07-02T09:19:34.553953Z",
    "price": 740123.0,
    "price_currency": "USD",
    "area": 493.0,
    "total_area": 418.0,
    "measured_area": 411.0,
    "total_rooms": 2.0,
    "toilets": 3,
    "construction_year": 1952,
    "renovation_year": 2010,
    "total_floors": 2,
    "heating": "None",
    "outer_walls": "Stucco",
    "roof_type": "Hip",
    "description": "",
    "status": null,
    "owner": null
}
```

- **404 Not Found**: ID does not exist.
```JSON
{
    "detail": "Not found."
}
```

## Add to favorite

Add a property to favorite for a loged in user. Requires authentication.

##### Example Request

```bash
curl -X POST 'http://localhost:8000/api/v1/properties/properties/39/add_to_favorites/' \
--header 'Authorization: Bearer eyJA' \
--header 'Cookie: messages=Wds; sessionid=ewyq157moopepfx'
```

##### Example Response

- **200 OK**
```JSON
{
    "id": 39,
    "type": "Apartment",
    "description": "Комфорен стан на а...",
    "created_at": "2025-07-03T11:39:16.568389Z",
    "price": 0.0,
    "price_currency": "Euro",
    "address": {
        "postal_code": "6250",
        "street": "Maršal Tito",
        "city": "Kičevo"
    },
    "favorite": true
}
```

- **404 Not Found**: ID does not exist.
```JSON
{
    "detail": "Not found."
}
```

## Remove from favorite

Remove a property from the user favorites. Requires authentication.

##### Example Request

```bash
curl --location --request POST 'http://localhost:8000/api/v1/properties/properties/30/remove_from_favorites/' \
--header 'Authorization: Bearer eyJA' \
--header 'Cookie: messages=Wds; sessionid=ewyq157moopepfx'
```

##### Example Response

- **204 No Content**: If the property is successfully removed from the user favorite list.

- **400 Bad Request**: Property does not exist in the users favorite.
```JSON
{
    "detail": "The given property is not in user favorites."
}
```

- **401 Unauthorized**: If the property is successfully removed from the user favorite list.
```JSON
{
    "detail": "Authentication credentials were not provided."
}
```

## Fetch user favorite properties

Fetch a list of favorite properties for the loged in user. Requires authentication.

##### Example Request

```bash
curl --location 'http://localhost:8000/api/v1/properties/properties/user_favorite_properties/' \
--header 'Authorization: Bearer eyJA' \
--header 'Cookie: messages=Wds; sessionid=ewyq157moopepfx'
```

##### Example Response

- **200 OK**
```JSON
[
    {
        "id": 39,
        "type": "Apartment",
        "description": "Комфорен стан на...",
        "created_at": "2025-07-03T11:39:16.568389Z",
        "price": 0.0,
        "price_currency": "Euro",
        "address": {
            "postal_code": "6250",
            "street": "Maršal Tito",
            "city": "Kičevo"
        },
        "favorite": true
    }
]
```

## Fetch the data required to create a new property 
Get the data to populate the create property form. Requires authentication.

##### Example Request

```bash
curl --location 'http://localhost:8000/api/v1/properties/properties/get_create_property_form_data/'
```

```bash
curl --location 'http://localhost:8000/api/v1/properties/properties/get_create_property_form_data/' \
--header 'Authorization: Bearer eyJA' \
--header 'Cookie: messages=Wds; sessionid=ewyq157moopepfx'
```

##### Example Response

- **401 Unauthorized**: If the property is successfully removed from the user favorite list.
```JSON
{
    "detail": "Authentication credentials were not provided."
}
```

- **200 OK**
```JSON
{
    "types": [
        {
            "id": 2,
            "name": "Apartment"
        },
        {
            "id": 11,
            "name": "Boat house"
        }
    ],
    "status": [
        {
            "id": 1,
            "name": "Active"
        },
        {
            "id": 9,
            "name": "Auction"
        }
    ],
    "cities": [
        "Skopje",
        "Tetovo",
        "Bitola"
    ]
}
```