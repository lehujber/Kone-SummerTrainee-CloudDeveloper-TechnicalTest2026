async def test_delete_seashell_success(client):
	# create and delete
	r = await client.post("/seashells/", json={"name": "ToDelete", "species": "Del"})
	assert r.status_code == 200
	sid = r.json()["id"]

	r = await client.delete(f"/seashells/{sid}")
	assert r.status_code == 204

	# ensure gone
	r = await client.get(f"/seashells/{sid}")
	assert r.status_code == 404


async def test_delete_seashell_not_found(client):
	r = await client.delete("/seashells/999999")
	assert r.status_code == 404


async def test_bulk_delete_seashells(client):
	# create multiple
	ids = []
	for i in range(3):
		r = await client.post("/seashells/", json={"name": f"Bulk{i}", "species": "B"})
		assert r.status_code == 200
		ids.append(r.json()["id"])

	# delete them
	r = await client.request("DELETE", "/seashells/", json=ids)
	assert r.status_code == 200
	body = r.json()
	assert isinstance(body, dict)
	assert body.get("deleted_count") == len(ids)

	# confirm one is gone
	r = await client.get(f"/seashells/{ids[0]}")
	assert r.status_code == 404
