import pytest


async def test_update_seashell_success(client):
	create_payload = {
		"name": "Original",
		"species": "Origus",
		"description": "orig",
		"personal_notes": "none",
		"date_found": "2026-02-11"
	}
	r = await client.post("/seashells/", json=create_payload)
	assert r.status_code == 200
	created = r.json()
	sid = created["id"]

	update_payload = {
		"name": "Updated",
		"species": "Updatia",
		"description": "updated desc",
		"personal_notes": "notes",
		"date_found": "2026-02-12"
	}

	r = await client.put(f"/seashells/{sid}", json=update_payload)
	assert r.status_code == 200
	updated = r.json()
	assert updated["id"] == sid
	assert updated["name"] == update_payload["name"]


async def test_update_seashell_not_found(client):
	payload = {"name": "X", "species": "Y"}
	r = await client.put("/seashells/999999", json=payload)
	assert r.status_code == 404


@pytest.mark.parametrize("bad_payload", [
	{},
	{"species": "only"},
	{"name": "", "species": "x"},
])
async def test_update_seashell_bad_payloads(client, bad_payload):
	r = await client.post("/seashells/", json={"name": "A", "species": "B"})
	assert r.status_code == 200
	sid = r.json()["id"]

	r = await client.put(f"/seashells/{sid}", json=bad_payload)
	assert r.status_code == 422