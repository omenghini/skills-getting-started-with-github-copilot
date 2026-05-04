class TestGetActivities:
    def test_get_all_activities_returns_200(self, client):
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Yoga Club",
            "Art Club",
            "Drama Workshop",
            "Science Club",
            "Debate Team",
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert set(expected_activities) == set(data.keys())

    def test_activity_contains_required_fields(self, client):
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert required_fields.issubset(activity_data.keys()), (
                f"Activity '{activity_name}' is missing required fields"
            )

    def test_participants_list_is_returned(self, client):
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert activity_name in data
        assert "michael@mergington.edu" in data[activity_name]["participants"]
        assert "daniel@mergington.edu" in data[activity_name]["participants"]
