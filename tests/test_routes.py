import pytest
from fastapi.testclient import TestClient

def register_user(client, email, password, first_name="Test", constituency_id=1):
    return client.post("/auth/register", json={
        "first_name": first_name,
        "last_name": "User",
        "email": email,
        "password": password,
        "constituency_id": constituency_id
    })

def login_user(client, email, password):
    return client.post("/auth/login", data={
        "username": email,
        "password": password
    })

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

class TestAuth:
    def test_register_success(self, client):
        res = register_user(client, "a@b.com", "test123")
        assert res.status_code == 201
        assert res.json()["email"] == "a@b.com"

    def test_register_duplicate_email(self, client):
        register_user(client, "dup@b.com", "test123")
        res = register_user(client, "dup@b.com", "test123")
        assert res.status_code == 409

    def test_login_success(self, client):
        register_user(client, "login@b.com", "test123")
        res = login_user(client, "login@b.com", "test123")
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_bad_password(self, client):
        register_user(client, "bad@b.com", "test123")
        res = login_user(client, "bad@b.com", "wrong")
        assert res.status_code == 401


class TestIssues:
    def get_token_for_user(self, client, email):
        register_user(client, email, "pass")
        res = login_user(client, email, "pass")
        return res.json()["access_token"]

    def test_create_issue(self, client):
        token = self.get_token_for_user(client, "issuer@b.com")
        res = client.post("/issues/", json={
            "title": "Broken road",
            "content": "Potholes everywhere",
            "latitude": 12.34,
            "longitude": 56.78
        }, headers=auth_header(token))
        assert res.status_code == 200  # Your route returns 200, though 201 might be more typical
        data = res.json()
        assert data["title"] == "Broken road"
        assert data["status"] == "open"
        assert data["vote_count"] == 0

    def test_list_issues(self, client):
        token = self.get_token_for_user(client, "lister@b.com")
        # Create two issues
        client.post("/issues/", json={
            "title": "Issue 1", "content": "desc", "latitude": 1.0, "longitude": 2.0
        }, headers=auth_header(token))
        client.post("/issues/", json={
            "title": "Issue 2", "content": "desc", "latitude": 1.0, "longitude": 2.0
        }, headers=auth_header(token))
        res = client.get("/issues/", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) == 2

    def test_delete_own_issue(self, client):
        token = self.get_token_for_user(client, "deleter@b.com")
        issue = client.post("/issues/", json={
            "title": "Delete me", "content": "desc", "latitude": 1.0, "longitude": 2.0
        }, headers=auth_header(token)).json()
        res = client.delete(f"/issues/{issue['id']}", headers=auth_header(token))
        assert res.status_code == 204

    def test_update_issue(self, client):
        token = self.get_token_for_user(client, "updater@b.com")
        issue = client.post("/issues/", json={
            "title": "Old", "content": "desc", "latitude": 1.0, "longitude": 2.0
        }, headers=auth_header(token)).json()
        res = client.put(f"/issues/{issue['id']}", json={"title": "New title"}, headers=auth_header(token))
        assert res.status_code == 200
        assert res.json()["title"] == "New title"


class TestComments:
    def get_token_and_issue(self, client):
        register_user(client, "commenter@b.com", "pass")
        token = login_user(client, "commenter@b.com", "pass").json()["access_token"]
        issue = client.post("/issues/", json={
            "title": "For comments", "content": "...", "latitude": 1.0, "longitude": 2.0
        }, headers=auth_header(token)).json()
        return token, issue["id"]

    def test_add_comment(self, client):
        token, issue_id = self.get_token_and_issue(client)
        res = client.post(f"/issues/{issue_id}/comments/", json={
            "content": "I agree"
        }, headers=auth_header(token))
        assert res.status_code == 201
        data = res.json()
        assert data["content"] == "I agree"
        assert data["issue_id"] == issue_id

    def test_list_comments(self, client):
        token, issue_id = self.get_token_and_issue(client)
        client.post(f"/issues/{issue_id}/comments/", json={"content": "First"}, headers=auth_header(token))
        client.post(f"/issues/{issue_id}/comments/", json={"content": "Second"}, headers=auth_header(token))
        res = client.get(f"/issues/{issue_id}/comments/", headers=auth_header(token))
        assert res.status_code == 200
        assert len(res.json()) == 2


class TestVotes:
    def test_vote_flow_and_threshold(self, client):
        # Create two users in same constituency
        register_user(client, "voter1@b.com", "pass")
        token1 = login_user(client, "voter1@b.com", "pass").json()["access_token"]
        register_user(client, "voter2@b.com", "pass")
        token2 = login_user(client, "voter2@b.com", "pass").json()["access_token"]
        # Create issue as user1
        issue = client.post("/issues/", json={
            "title": "Test threshold", "content": "...", "latitude": 1.0, "longitude": 2.0
        }, headers=auth_header(token1)).json()
        issue_id = issue["id"]

        # User1 votes
        res = client.post(f"/issues/{issue_id}/vote", headers=auth_header(token1))
        assert res.status_code == 201
        # User1 tries to vote again → conflict
        res = client.post(f"/issues/{issue_id}/vote", headers=auth_header(token1))
        assert res.status_code == 409
        # User2 votes
        res = client.post(f"/issues/{issue_id}/vote", headers=auth_header(token2))
        assert res.status_code == 201

        # Check issue vote_count (should be 2, threshold 5 not reached yet)
        issue_data = client.get(f"/issues/{issue_id}", headers=auth_header(token1)).json()
        assert issue_data["vote_count"] == 2
        assert issue_data["threshold_reached"] == False

        # We need 3 more votes to reach threshold. Register and vote 3 more users.
        for i in range(3, 6):
            email = f"voter{i}@b.com"
            register_user(client, email, "pass")
            token = login_user(client, email, "pass").json()["access_token"]
            res = client.post(f"/issues/{issue_id}/vote", headers=auth_header(token))
            assert res.status_code == 201

        # Now threshold should be reached (5 votes) after background task runs.
        # Since background task runs asynchronously, we need to give it a moment.
        import time
        time.sleep(0.5)  # small delay to let background task complete

        issue_data = client.get(f"/issues/{issue_id}", headers=auth_header(token1)).json()
        assert issue_data["vote_count"] == 5
        assert issue_data["threshold_reached"] == True
        assert issue_data["status"] == "escalated"