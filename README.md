# Fivetran home assignment
This repository contains test task for Fivetran SDET position

### Overall description
This project contains an example of DDL/DDL operations verification.

### Infra
Infrastructure consists of docker container and corresponding docker compose file. 
.env file contains test database credentials.
Pipenv was chosen as dependency management tool.

### Continouos integration
This repository contains only one job which is pretty straighforward and consists for three steps:
 - environment setup for python
 - containter start
 - tests execution

### Test data
The data represents a tiny sample of Databricks Taxi trip dataset. Test data is loaded as a dictionary from CSV sample.

### Data management
Data management and creation is done using sqlalchemy and alembic.
alembic allows to have versioned python models for controlled and holistic data migration.
These two were chosen because they work very well together.

The project contains two migrations:
 - first populates database with one table;
 - second changes datatype with custom conversion from string to boolean.

### Tests 
There are three tests:
 - table creation;
 - table migration check with type verification;
 - table migration check with data populated and verification.

Few fixtures were developed to improve testing experience.

### Potential improvements
Here is a list of things which could have potentially be improved:
 - use raw psycopg as a driver - for example, for working with OLAP databases (probaly at cost of doing manual migration);
 - use polars for more convenient and not-so-nosy tabular data comparison
