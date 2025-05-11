## Setup
Based on: https://gist.github.com/reltuk/8a97771e8b46dd32e47c80ef0c3645f7

The manifests expect a secret named dolt-credentials to exist in the dolt-cluster-example namespace:
```
kubectl \
  -n dolt-cluster-example \
  create secret generic \
  dolt-credentials \
  --from-literal=admin-user=root \
  --from-literal=admin-password=hunter2
```

Install MySQL client within Dolt pod.
```
apt-get update
apt-get install default-mysql-client
```

## [Hello world](https://docs.dolthub.com/introduction/getting-started/database)

Get the password for DB and connect to it.
```
kubectl -n dolt-cluster-example get secret dolt-credentials -o jsonpath="{.data.admin-password}" 
mysql --host 127.0.0.1 --port 3306 -u root -p
```

Create schema.
```
create database getting_started;
use getting_started;
create table employees (
    id int,
    last_name varchar(255),
    first_name varchar(255),
    primary key(id));
create table teams (
    id int,
    team_name varchar(255),
    primary key(id));
create table employees_teams(
    team_id int,
    employee_id int,
    primary key(team_id, employee_id),
    foreign key (team_id) references teams(id),
    foreign key (employee_id) references employees(id));
show tables;
```

Commit schema.
```
call dolt_add('teams', 'employees', 'employees_teams');
call dolt_commit('-m', 'Created initial schema');
select * from dolt_log;
```

Insert data.
```
insert into employees values
    (0, 'Sehn', 'Tim'),
    (1, 'Hendriks', 'Brian'),
    (2, 'Son','Aaron'),
    (3, 'Fitzgerald', 'Brian');
insert into teams values
    (0, 'Engineering'),
    (1, 'Sales');
insert into employees_teams(employee_id, team_id) values
    (0,0),
    (1,0),
    (2,0),
    (0,1),
    (3,1);
select first_name, last_name, team_name from employees
    join employees_teams on (employees.id=employees_teams.employee_id)
    join teams on (teams.id=employees_teams.team_id)
    where team_name='Engineering';
```

Examine the diff.
```
select * from dolt_status;
select * from dolt_diff_employees;
```

Commit all modified tables.
```
call dolt_commit('-am', 'Populated tables with data');
select * from dolt_log;
select * from dolt_diff;
```

Make changes on a branch.
```
call dolt_checkout('-b','modifications');
update employees SET first_name='Timothy' where first_name='Tim';
insert INTO employees (id, first_name, last_name) values (4,'Daylon', 'Wilkins');
insert into employees_teams(team_id, employee_id) values (0,4);
delete from employees_teams where employee_id=0 and team_id=1;
call dolt_commit('-am', 'Modifications on a branch')
```



## Required features (not presented in the demo)

#### Checkout to a commit?
```
use `getting_started/lmo75ku2vecfdhpn5f2uk8fkti0o989q`
```

#### Create a branch in detached head mode?
```
mysql> call dolt_checkout('-b','modifications');
ERROR 1105 (HY000): fatal: Unexpected error creating branch 'modifications' : this operation is not supported while in a detached head state

When you're in detached HEAD (after checking out a commit directly), CALL dolt_checkout('-b', 'branch') internally tries to both create and checkout a new branch — but creating a branch via SQL in detached HEAD is not allowed.

This restriction is specific to the SQL interface. In contrast, the CLI allows it just fine.
```

#### JSON support?
- https://www.dolthub.com/blog/2021-04-14-JSON-type-support/
- https://www.dolthub.com/blog/2022-06-30-working-with-json/
- https://www.dolthub.com/blog/2023-06-07-better-json-support/