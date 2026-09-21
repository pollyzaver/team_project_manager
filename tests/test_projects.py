from projects import add_member, find_member, is_project_active


def test_add_member():
    members = []
    add_member(members, "Анна Иванова", "Аналитик")
    assert len(members) == 1
    assert members[0]["name"] == "Анна Иванова"


def test_find_member():
    members = []
    add_member(members, "Иван Иванов", "Разработчик")
    result = find_member(members, "иван")
    assert len(result) == 1


def test_is_project_active_true():
    project = {"status": "Активен"}
    assert is_project_active(project)


def test_is_project_active_false():
    project = {"status": "Завершен"}
    assert not is_project_active(project)
