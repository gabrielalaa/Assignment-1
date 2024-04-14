# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency


def test_get_subscribers_should_list_all_papers(client, agency):
    # send request
    response = client.get("/subscriber/")  # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["subscriber"]) == len(agency.subscribers)


def test_add_subscriber(client, agency):
    # prepare
    sub_count_before = len(agency.subscribers)

    # act
    response = client.post("/subscriber/",  # <-- note the slash at the end!
                           json={
                               "subscriber_name": "Gabriela",
                               "subscriber_address": "San Francisco"
                           })

    # test status code
    assert response.status_code == 200

    # verify
    assert len(agency.subscribers) == sub_count_before + 1

    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["subscriber"]

    # verify that the response contains the newspaper data
    assert paper_response["subscriber_name"] == "Gabriela"


def test_get_subscriber(client, agency):
    # Add the subscriber
    new_sub_response = client.post("/subscriber/",
                                   json={
                                       "subscriber_name": "Gabriela",
                                       "subscriber_address": "San Francisco"
                                   })
    parsed = new_sub_response.get_json()
    sub_response = parsed["subscriber"]

    # send request
    response = client.get(f'/subscriber/{sub_response["subscriber_id"]}')

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    sub_response = parsed["subscriber"]
    assert sub_response["subscriber_name"] == "Gabriela"
    assert sub_response["subscriber_address"] == "San Francisco"

    # Try for a non-existing subscriber
    response = client.get("/subscriber/1")
    assert response.status_code == 404


def test_update_subscriber(client, agency):
    # Add the subscriber
    new_sub_response = client.post("/subscriber/",
                                   json={
                                       "subscriber_name": "Gabriela",
                                       "subscriber_address": "San Francisco"
                                   })
    parsed = new_sub_response.get_json()
    sub_response = parsed["subscriber"]
    update_response = client.post(f"/subscriber/{sub_response['subscriber_id']}",
                                  json={"subscriber_name": "Carla"})

    # test status code
    assert update_response.status_code == 200

    # parse response and check that the correct data is here
    parsed = update_response.get_json()
    sub_response = parsed["subscriber"]
    assert sub_response["subscriber_name"] == "Carla"
    assert sub_response["subscriber_address"] == "San Francisco"

    # Try for a non-existing newspaper
    response = client.post("/subscriber/1")
    assert response.status_code == 404

def test_no_update_subscriber(client, agency):
    # Add the subscriber
    new_sub_response = client.post("/subscriber/",
                                   json={
                                       "subscriber_name": "Gabriela",
                                       "subscriber_address": "San Francisco"
                                   })
    parsed = new_sub_response.get_json()
    sub_response = parsed["subscriber"]
    update_response = client.post(f"/subscriber/{sub_response['subscriber_id']}",
                                  json={})

    # test status code
    assert update_response.status_code == 400

    # parse response and check that the correct data is here
    parsed = update_response.get_json()

    assert "No updates have been made" == parsed["message"]

def test_delete_subscriber(client, agency):
    # Add the subscriber
    new_sub_response = client.post("/subscriber/",
                                   json={
                                       "subscriber_name": "Gabriela",
                                       "subscriber_address": "San Francisco"
                                   })
    parsed = new_sub_response.get_json()
    sub_response = parsed["subscriber"]

    # Delete the subscriber
    delete_response = client.delete(f"/subscriber/{sub_response['subscriber_id']}")

    # test status code
    assert delete_response.status_code == 200

    # obtain the response data as a plain string!!!
    assert "was removed" in delete_response.get_data(as_text=True)

    # Try to delete the same subscriber
    delete_response = client.delete(f"/newspaper/{sub_response['subscriber_id']}")
    assert "was not found" in delete_response.get_data(as_text=True)
