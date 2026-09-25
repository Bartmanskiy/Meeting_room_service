def test_create_booking(client):
    response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["room_id"] == 1
    assert data["organizer_name"] == "Test User"


def test_create_overlapping_booking(client):
    first_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "First User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Second User",
            "start_time": "2030-01-10T10:30:00",
            "end_time": "2030-01-10T11:30:00",
        },
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Room is already booked for this time"
    )


def test_create_adjacent_booking(client):
    first_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "First User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Second User",
            "start_time": "2030-01-10T11:00:00",
            "end_time": "2030-01-10T12:00:00",
        },
    )

    assert second_response.status_code == 201


def test_create_booking_for_nonexistent_room(client):
    response = client.post(
        "/api/bookings",
        json={
            "room_id": 999,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Room not found"


def test_start_time_in_past(client):
    response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2020-01-10T10:00:00",
            "end_time": "2020-01-10T11:00:00",
        },
    )

    assert response.status_code == 422


def test_end_time_before_start_time(client):
    response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T11:00:00",
            "end_time": "2030-01-10T10:00:00",
        },
    )

    assert response.status_code == 422


def test_end_time_equal_start_time(client):
    response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T11:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert response.status_code == 422


def test_get_bookings(client):
    create_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert create_response.status_code == 201

    response = client.get("/api/bookings")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_bookings_by_room(client):
    create_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/bookings",
        params={"room_id": 1},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_bookings_by_date(client):
    create_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/bookings",
        params={"date": "2030-01-10"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_booking(client):
    create_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "organizer_name": "Test User",
            "start_time": "2030-01-10T10:00:00",
            "end_time": "2030-01-10T11:00:00",
        },
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/bookings/{booking_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get("/api/bookings")

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_delete_nonexistent_booking(client):
    response = client.delete("/api/bookings/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_get_rooms(client):
    response = client.get("/api/rooms")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Test Room"
    assert data[0]["capacity"] == 6