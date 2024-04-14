# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency


def test_get_editor_should_list_all_editors(client, agency):
    # send request
    response = client.get('/editor/')

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["editor"]) == len(agency.editors)


def test_add_editor(client, agency):
    # prepare
    editors_count_before = len(agency.editors)

    # act
    response = client.post('/editor/',
                           json={
                               "editor_id": 10000,
                               "editor_name": "Ana",
                               "address": "San Francisco"
                           })

    assert response.status_code == 200

    # verify
    assert len(agency.editors) == editors_count_before + 1

    # parse response and check that the correct data is here
    parsed = response.get_json()
    editor_response = parsed["editor"]

    # verify that the response contains the editor data
    assert editor_response["editor_name"] == "Ana"


def test_get_editor(client, agency):
    # Add the editor
    new_editor = client.post('/editor/',
                             json={
                                 "editor_id": 10000,
                                 "editor_name": "Ana",
                                 "address": "San Francisco"
                             })
    parsed = new_editor.get_json()
    editor_response = parsed["editor"]

    # send request
    response = client.get(f'/editor/{editor_response["editor_id"]}')

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    editor_response = parsed["editor"]
    assert editor_response["editor_name"] == "Ana"

    # Try for a non-existing editor
    response = client.get("/editor/1")
    assert response.status_code == 404


def test_update_editor(client, agency):
    # Add the editor
    new_editor = client.post('/editor/',
                             json={
                                 "editor_id": 10000,
                                 "editor_name": "Ana",
                                 "address": "San Francisco"
                             })
    parsed = new_editor.get_json()
    editor_response = parsed["editor"]

    update_response = client.post(f'/editor/{editor_response["editor_id"]}',
                                  json={"editor_name": "Radulescu"})

    # test status code
    assert update_response.status_code == 200

    # parse response and check that the correct data is here
    parsed = update_response.get_json()
    editor_response = parsed["editor"]
    assert editor_response["editor_name"] == "Radulescu"
    assert editor_response["address"] == "San Francisco"

    # Try for a non-existing editor
    response = client.post("/editor/1")
    assert response.status_code == 404

def test_no_update_editor(client, agency):
    # Add the editor
    new_editor = client.post('/editor/',
                             json={
                                 "editor_id": 10000,
                                 "editor_name": "Ana",
                                 "address": "San Francisco"
                             })
    parsed = new_editor.get_json()
    editor_response = parsed["editor"]

    update_response = client.post(f'/editor/{editor_response["editor_id"]}',
                                  json={})

    # test status code
    assert update_response.status_code == 400

    # parse response and check that the correct data is here
    parsed = update_response.get_json()

    assert "No updates have been made" == parsed["message"]


def test_delete_editor(client, agency):
    # Add the editor
    new_editor = client.post('/editor/',
                             json={
                                 "editor_id": 10000,
                                 "editor_name": "Ana",
                                 "address": "San Francisco"
                             })
    parsed = new_editor.get_json()
    editor_response = parsed["editor"]

    # Delete the editor
    delete_response = client.delete(f'/editor/{editor_response["editor_id"]}')

    # test status code
    assert delete_response.status_code == 200

    # obtain the response data as a plain string!!!
    assert "was removed" in delete_response.get_data(as_text=True)

    # Try to delete the same editor
    delete_response = client.delete(f"/newspaper/{editor_response['editor_id']}")
    assert "was not found" in delete_response.get_data(as_text=True)
