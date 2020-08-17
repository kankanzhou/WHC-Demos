# IHIS-WHC
Source code for WHC Project Demos

# Project File Structure
```
./
└── src/                                    < Source codes goes here
   ├── requirements.txt                     
   ├── api/                                 < FastAPI code
   │  ├── __init__.py
   │  ├── main.py                           < Barebones FastAPI stubs (to be filled in)
   │  └── models.py                         < Definitions of data schemas
   └── demos/
      ├── __init__.py
      ├── Mock.py                           < Container for methods to mock data
      └── SOCWorkloadValidationDemo.py      < Streamlit demo for WHC-POC4
```

# Running in development mode
- Start streamlit demos:
```
streamlit run src/demos/SOCWorkloadValidationDemo.py
```

- Start FastAPI Server
```
uvicorn src.api.main:app --reload
```
