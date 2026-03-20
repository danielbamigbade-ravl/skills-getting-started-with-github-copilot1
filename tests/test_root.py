"""Tests for the root endpoint"""

import pytest


def test_root_redirects_to_index(client):
    """
    Arrange: Prepare a TestClient
    Act: Make a GET request to the root endpoint
    Assert: Verify response redirects to /static/index.html
    """
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follow(client):
    """
    Arrange: Prepare a TestClient with follow_redirects
    Act: Make a GET request to the root endpoint following redirects
    Assert: Verify final response is successful (though static file may not exist in test)
    """
    response = client.get("/", follow_redirects=True)
    
    # After following redirect to static file, we expect 404 (file not served in test)
    # or similar, but the redirect itself should work
    assert response.status_code in [200, 404]
