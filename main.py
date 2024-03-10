#Command to run the app
# python3 -m uvicorn main:myapp --reload
import json
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from pydantic import BaseModel

myofficeapp = FastAPI()


# BaseModel class is inherited for validation, parsing, etc
class People(BaseModel):
    id: Optional[int] = None
    firstname: str
    lastname: str
    Age: int
    Gender: str
    Dept: str
    Salary: str


with open("values.json", 'r') as file:
    allEmployees = json.load(file)["people"]


# Status code: 200 means success
@myofficeapp.get("/getAllEmployees", status_code=200)
def getallemployees():
    return list(allEmployees)


# Status code: 201 means resource is successfully created
@myofficeapp.post("/hireNewEmployee", status_code=201)
def hireSomeone(people: People):
    maxi = 0
    for p in allEmployees:
        maxi = max(maxi, p["id"])

    new_person = {
        "id": maxi + 1,
        "firstname": people.firstname,
        "lastname": people.lastname,
        "Age": people.Age,
        "Gender": people.Gender,
        "Dept": people.Dept,
        "Salary": people.Salary
    }
    allEmployees.append(new_person)
    new_json = {"people": []}
    new_json["people"] = allEmployees

    with open("values.json", "w") as file:
        json.dump(new_json, file)


@myofficeapp.put("/giveHike", status_code=201)
def giveHike(id: int, hike: int):
    matching_result = [p for p in allEmployees if p["id"] == id]
    if len(matching_result) > 0:
        new_entry = matching_result[0]
        old_Salary = int(new_entry["Salary"])
        new_entry["Salary"] = str(int(((100 + hike) / 100) * old_Salary))

        allEmployees.remove(matching_result[0])
        allEmployees.append(new_entry)
        new_json = {"people": []}
        new_json["people"] = allEmployees
        with open("values.json", "w") as file:
            json.dump(new_json, file)
        return [emp for emp in allEmployees if emp["id"] == id]

    return HTTPException(status_code=404, detail="There is no employee matching the id")


# Here mentioning the argument with datatype helps to eliminate the typecast error
@myofficeapp.get("/getPeople/{r_id}", status_code=200)
def getOfficePeople(r_id: int):
    return [p for p in allEmployees if p['id'] == r_id]


@myofficeapp.get("/searchPeople/", status_code=200)
def SearchPeople(name: Optional[str] = Query(default=None, description="Enter the name to search")):
    return [p for p in allEmployees if name.lower() in p['firstname'].lower() or name.lower() in p['lastname'].lower()]

@myofficeapp.delete("/fireSomeone/{id}",status_code=200)
def FireSomeone(id:int):
    person_fired=[p for p in allEmployees if p["id"]==id]
    if len(person_fired)==0:
        raise HTTPException(status_code=404, detail="Person not found")
    else:
        allEmployees.remove(person_fired[0])
        new_json = {"people": []}
        new_json["people"] = allEmployees
        with open("values.json", "w") as file:
            json.dump(new_json, file)






