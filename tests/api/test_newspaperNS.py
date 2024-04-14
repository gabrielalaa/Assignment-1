# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency


def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")  # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14


def test_get_newspaper(client, agency):
    # Add the newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })

    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    # send request
    response = client.get(f'/newspaper/{paper_response["paper_id"]}')

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed2 = response.get_json()
    paper_response2 = parsed2["newspaper"]
    assert paper_response2["name"] == "Simpsons Comic"
    assert paper_response2["frequency"] == 7
    assert paper_response2["price"] == 3.14

    # Try for a non-existing newspaper
    response = client.get("/newspaper/9999")
    assert response.status_code == 404


def test_update_newspaper(client, agency):
    # Add the newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })

    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    update_response = client.post(f"/newspaper/{paper_response['paper_id']}",
                                  json={"name": "Simpsons Comic 2",
                                        "frequency": 3})

    # test status code
    assert update_response.status_code == 200

    # parse response and check that the correct data is here
    parsed = update_response.get_json()
    paper_response = parsed["newspaper"]
    assert paper_response["name"] == "Simpsons Comic 2"
    assert paper_response["frequency"] == 3
    assert paper_response["price"] == 3.14

    # Try for a non-existing newspaper
    response = client.post("/newspaper/9999")
    assert response.status_code == 404


def test_no_update_newspaper(client, agency):
    # Add the newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })

    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    update_response = client.post(f"/newspaper/{paper_response['paper_id']}",
                                  json={})

    # test status code
    assert update_response.status_code == 400

    # parse response and check that the correct data is here
    parsed = update_response.get_json()

    assert "No updates have been made" == parsed["message"]


def test_delete_newspaper(client, agency):
    # Add the newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    # Delete the newspaper
    delete_response = client.delete(f"/newspaper/{paper_response['paper_id']}")

    # test status code
    assert delete_response.status_code == 200

    # obtain the response data as a plain string!!!
    assert "was removed" in delete_response.get_data(as_text=True)

    # Try to delete the same newspaper
    delete_response = client.delete(f"/newspaper/{paper_response['paper_id']}")
    assert "was not found" in delete_response.get_data(as_text=True)


def test_get_issues_should_list_all_issues(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    # Add issues to the newspaper
    client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                json={
                    "release_date": "14.04.2024",
                    "number_of_pages": 10,
                    "released": False
                })
    client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                json={
                    "release_date": "14.03.2024",
                    "number_of_pages": 5,
                    "released": False
                })

    # send request
    response = client.get(f"/newspaper/{paper_response['paper_id']}/issue")

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["issue"]) == 2

    # Try for a non-existing newspaper
    response = client.get("/newspaper/9999/issue")
    assert response.status_code == 404


def test_add_issue(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    # act
    response = client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                           json={
                               "release_date": "14.04.2024",
                               "number_of_pages": 10,
                               "released": False
                           })

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    issue_response = parsed["issue"]
    assert issue_response["release_date"] == "14.04.2024"
    assert issue_response["number_of_pages"] == 10
    assert not issue_response["released"]

    # Try for a non-existing newspaper
    response = client.post(f"/newspaper/9999/issue",
                           json={
                               "release_date": "14.04.2024",
                               "number_of_pages": 10,
                               "released": False
                           })

    assert response.status_code == 404


def test_get_issue(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    # Add an issue to the newspaper
    client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                json={
                    "release_date": "14.04.2024",
                    "number_of_pages": 10,
                    "released": False
                })

    # Get all issues for the newspaper
    response = client.get(f"/newspaper/{paper_response['paper_id']}/issue")
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    # The respose has to be a list
    assert isinstance(parsed['issue'], list)
    # Make sure that there is at least one issue
    assert len(parsed['issue']) > 0

    # Access the first issue in the list
    issue_data = parsed['issue'][0]
    assert issue_data["release_date"] == "14.04.2024"
    assert issue_data["number_of_pages"] == 10

    # Try for a non-existing newspaper issue
    response = client.get("/newspaper/100/issue/9999")
    assert response.status_code == 404


def test_release_issue(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]

    # Add an issue to the newspaper and get the issue_id
    new_issue_response = client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                                     json={
                                         "release_date": "14.04.2024",
                                         "number_of_pages": 10,
                                         "released": False
                                     })
    issue_parsed = new_issue_response.get_json()
    issue_data = issue_parsed['issue']

    # Release the issue
    response = client.post(f"/newspaper/{paper_response['paper_id']}/issue/{issue_data['issue_id']}/release")

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    issue_response = parsed["issue"]
    assert issue_response["released"]

    # Try releasing the same issue
    repeat_response = client.post(f"/newspaper/{paper_response['paper_id']}/issue/{issue_data['issue_id']}/release")
    assert repeat_response.status_code == 400

    # Try for a non-existing newspaper
    no_newspaper = client.post(f"/newspaper/9999/issue/{issue_data['issue_id']}/release")
    assert no_newspaper.status_code == 404

    # Try for a non-existing issue
    no_issue = client.post(f"/newspaper/{paper_response['paper_id']}/issue/9999/release")
    assert no_issue.status_code == 404


def test_specify_editor(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]
    # Extract the ID of the newspaper
    paper_id = paper_response['paper_id']

    new_issue_response = client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                                     json={
                                         "release_date": "14.04.2024",
                                         "number_of_pages": 10,
                                         "released": False
                                     })
    parsed = new_issue_response.get_json()
    issue_response = parsed["issue"]
    # Extract the ID of the issue
    issue_id = issue_response['issue_id']

    # Create the editor
    new_editor_response = client.post("/editor/",
                                      json={
                                          "editor_id": 10000,
                                          "editor_name": "Ana",
                                          "address": "San Francisco"
                                      })
    parsed = new_editor_response.get_json()
    editor_response = parsed["editor"]
    # Extract the id of the editor
    editor_id = editor_response['editor_id']

    # act
    # Because I use reqparse to parse and validate incoming request data (editor_id),
    # I need to provide the expected data in a JSON format
    response = client.post(f"/newspaper/{paper_id}/issue/{issue_id}/editor", json={"editor_id": editor_id})

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    issue_response = parsed["issue"]
    assert issue_response['editor_id'] == editor_id

    # Try for a non-existing newspaper
    no_newspaper = client.post(f"/newspaper/1111/issue/{issue_id}/editor", json={"editor_id": editor_id})
    assert no_newspaper.status_code == 404

    # Try for a non-existing issue
    no_issue = client.post(f"/newspaper/{paper_id}/issue/1/editor", json={"editor_id": editor_id})
    assert no_issue.status_code == 404

    # Try for a non-existing editor
    no_editor = client.post(f"/newspaper/{paper_id}/issue/{issue_id}/editor", json={"editor_id": 1})
    assert no_editor.status_code == 404


def test_deliver_issue(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]
    # Extract the ID of the newspaper
    paper_id = paper_response['paper_id']

    new_issue_response = client.post(f"/newspaper/{paper_response['paper_id']}/issue",
                                     json={
                                         "release_date": "14.04.2024",
                                         "number_of_pages": 10,
                                         "released": False
                                     })
    parsed = new_issue_response.get_json()
    issue_response = parsed["issue"]
    # Extract the ID of the issue
    issue_id = issue_response['issue_id']

    # Release the issue
    client.post(f"/newspaper/{paper_response['paper_id']}/issue/{issue_response['issue_id']}/release")

    # Create the subscriber
    new_subscriber_response = client.post("/subscriber/",
                                          json={
                                              "subscriber_name": "Gabriela",
                                              "subscriber_address": "San Francisco"
                                          })
    parsed = new_subscriber_response.get_json()
    subscriber_response = parsed["subscriber"]
    # Extract the ID of the subscriber
    subscriber_id = subscriber_response['subscriber_id']

    # act
    # Because I use reqparse to parse and validate incoming request data (subscriber_id),
    # I need to provide the expected data in a JSON format
    response = client.post(f"/newspaper/{paper_id}/issue/{issue_id}/deliver",
                           json={"subscriber_id": subscriber_id})

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert parsed["delivered_to"] == subscriber_id


def test_newspaper_statistics(client, agency):
    # Create a newspaper
    new_paper_response = client.post("/newspaper/",
                                     json={
                                         "name": "Simpsons Comic",
                                         "frequency": 7,
                                         "price": 3.14
                                     })
    parsed = new_paper_response.get_json()
    paper_response = parsed["newspaper"]
    # Extract the ID of the newspaper
    paper_id = paper_response['paper_id']

    # act
    response = client.get(f"/newspaper/{paper_id}/stats")

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert "monthly_revenue" in parsed
    assert "annual_revenue" in parsed

    # Try for a non-existing newspaper
    no_newspaper = client.get("/newspaper/11111/stats")
    no_newspaper_response = no_newspaper.get_json()
    assert "A newspaper with ID 11111 doesn't exist!" in no_newspaper_response["error"]
