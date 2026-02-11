import pytest


async def test_create_seashell_success(client):
	payload = {
		"name": "Test Shell Create",
		"species": "Specius testus",
		"description": "A test seashell",
		"personal_notes": "No notes",
		"date_found": "2026-02-23"
	}

	r = await client.post("/seashells/", json=payload)
	assert r.status_code == 200
	data = r.json()
	assert isinstance(data, dict)
	assert "id" in data
	for k in ["name", "species", "description", "personal_notes", "date_found"]:
		assert data.get(k) == payload[k]


@pytest.mark.parametrize("bad_payload,missing_field", [
	({}, "name"),
	({"species": "X"}, "name"),
	({"name": "OnlyName"}, "species"),
	({"name": "", "species": "Y"}, "name"),
])
async def test_create_seashell_bad_payloads(client, bad_payload, missing_field):
	r = await client.post("/seashells/", json=bad_payload)
	assert r.status_code == 422


async def test_create_seashell_invalid_date_format(client):
	payload = {
		"name": "Bad Date",
		"species": "Spec",
		"date_found": "not-a-date"
	}
	r = await client.post("/seashells/", json=payload)
	assert r.status_code == 422


async def test_create_seashell_extra_fields_ignored_or_rejected(client):
	payload = {
		"name": "Extra Field",
		"species": "Spec",
		"unknown_field": "surprise",
		"date_found": "2026-02-23"
	}
	r = await client.post("/seashells/", json=payload)

	assert r.status_code in (200, 422)
	if r.status_code == 200:
		data = r.json()
		assert data.get("name") == payload["name"]

