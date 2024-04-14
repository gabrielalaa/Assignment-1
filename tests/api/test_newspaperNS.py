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
