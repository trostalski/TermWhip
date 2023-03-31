# TermWhip

** This project is under development **

TermWhip is an extensible medical terminology servive.

### Terminologies

So far:
- ICD-9
- ICD-10
- Snomed CT

### Features

- Simple terminology look-up by code
- Retrieving Code Information content
- Retrieving Code(-set) Concept Similarity
- Inspecting parent child relationships

### Usage

First, make sure you have a postgres up and running. Clone the directory and install the requirements inside a virtual environment.

Next, you need to download the release files for the terminologies that you want to support ([snomed](https://www.nlm.nih.gov/healthit/snomedct/international.html), [ICD-9](https://www.cms.gov/Medicare/Coding/ICD9ProviderDiagnosticCodes/codes) ,[ICD-10](https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs)).
Store the respective folder inside [downloads](./src/downloads).

Change into the `src` directory and create the database with:

```shell
python -m app.scripts.create_db
```

Load the required data into the database by running the respevtive script using the same command.

Start the server on port 8000 with

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

you can inspect the api-endpoints at [http://localhost:8000/docs](http://localhost:8000/docs).
