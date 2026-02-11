async def test_list_seashells_empty(client):
    """GET /seashells/ returns 200 and an object with 'seashells' list (initially empty)."""
    r = await client.get("/seashells/")
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/json")
    data = r.json()
    assert isinstance(data, list)

async def test_list_seashells_structure(client):
    """Response keys and types are stable even after multiple requests."""
    for _ in range(2):
        r = await client.get("/seashells/")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

async def test_unknown_route_returns_404(client):
    r = await client.get("/this-route-does-not-exist")
    assert r.status_code == 404


async def test_create_and_list_and_get_seashells(client):
    payloads = [
        {
            "name": "Golden Lion Paw",
            "species": "Lyropecten nodosus",
            "description": "A heavy, thick-shelled scallop",
            "personal_notes": "Found at Low Tide",
            "date_found": "2026-02-21"
        },
        {
            "name": "Blue Button",
            "species": "Porpita porpita",
            "description": "Small blue float with tentacle-like structures",
            "personal_notes": "Washed ashore",
            "date_found": "2026-02-20"
        }
    ]

    created = []
    for p in payloads:
        r = await client.post("/seashells/", json=p)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)
        assert "id" in data
        for k in ["name", "species", "description", "personal_notes", "date_found"]:
            assert data.get(k) == p[k]
        created.append(data)

    r = await client.get("/seashells/")
    assert r.status_code == 200
    listed = r.json()

    ids = {c["id"] for c in created}
    returned_ids = {i["id"] for i in listed}
    assert ids.issubset(returned_ids)

    for c in created:
        r = await client.get(f"/seashells/{c['id']}")
        assert r.status_code == 200
        got = r.json()
        assert got["id"] == c["id"]
        assert got["name"] == c["name"]

    assert len(listed) == len(payloads)


async def test_get_single_seashell_by_id_returns_expected_fields(client):
    payload = {
        "name": "Test Shell",
        "species": "Testus examplus",
        "description": "Test description",
        "personal_notes": "Test notes",
        "date_found": "2026-02-22"
    }
    r = await client.post("/seashells/", json=payload)
    assert r.status_code == 200
    created = r.json()
    sid = created["id"]

    payload_2 = {
        "name": "Another Shell",
        "species": "Anotherus specimus",
        "description": "Another description",
        "personal_notes": "Another notes",
        "date_found": "2026-02-23"
    }
    r = await client.post("/seashells/", json=payload_2)
    assert r.status_code == 200

    r = await client.get(f"/seashells/{sid}")
    assert r.status_code == 200
    data = r.json()
    # ensure returned object has expected keys and values
    for k in ["id", "name", "species", "description", "personal_notes", "date_found"]:
        assert k in data
    assert data["name"] == payload["name"]
    assert data["species"] == payload["species"]


async def test_get_single_seashell_not_found_returns_404(client):
    # pick a high id that should not exist
    r = await client.get("/seashells/999999")
    assert r.status_code == 404
