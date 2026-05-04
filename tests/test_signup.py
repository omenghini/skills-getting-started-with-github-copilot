class TestSignup:
    def test_signup_new_student_returns_200(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_adds_student_to_participants(self, client):
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        get_response = client.get("/activities")
        participants = get_response.json()[activity_name]["participants"]
        assert email in participants

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_increases_participant_count(self, client):
        # Arrange
        activity_name = "Gym Class"
        email = "bob@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        final_count = len(client.get("/activities").json()[activity_name]["participants"])
        assert final_count == initial_count + 1
