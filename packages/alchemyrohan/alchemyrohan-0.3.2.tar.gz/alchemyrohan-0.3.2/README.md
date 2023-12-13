


# Alchemyrohan

 ![pypi v22.0.3](https://img.shields.io/badge/pypi-v22.0.3-yellow) ![Python 3.9 | 3.10 | 3.11](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11-blue) ![SqlAlchemy](https://img.shields.io/badge/SqlAlchemy-2.0-red)


Alchemyrohan is an extension package for **[SqlAlchemy](https://www.sqlalchemy.org/)** which automatically creates the database models according to the database schema.

---

## 📖 Content

- [How to Install](#-How-to-Install)
- [Database Support](#-Database-Support)
- [How to use](#-How-to-use)
  - [Functions](#-Functions)
  - [Models](#-Models)
- [Example](#-Example)
- [Dependencies](#-Dependencies)
- [Important Note](#Important-Note)
- [Release Notes](#-Release-Notes)
- [License](#-License-and-Third-Party-Licenses)

---


## 🔧 How to Install

With pip package installer from **[PyPI](https://pypi.org/project/pip/)** directly:

```
pip install alchemyrohan
```

or from source:

```
git clone --recursive https://github.com/wamberger/alchemyrohan.git
cd alchemyrohan
python3 setup.py install
```


## 🗄 Database Support

This project is currently designed to work with the following databases:

- **SqLite**
- **Oracle**


## 🔨 How to use

Import in your code:

`import alchemyrohan` 

or 

`import alchemyrohan as ar`

### 🪄 Functions

- **assemble_model()** is the main function. This function is used to create a SqlAlchemy database model and is accepting the following arguments:
    | argument | description |
    | --------- | --------- |
    | *engine* | this is SqlAlchemy engine  `from sqlalchemy import create_engine` |
    | *table_name* | this is the name of the database table |
    | *abs_os_path_to_model* | absolute path to the model's folder |
    | *py_path_to_model* | pythonic path to the models |

- **reload_module()** when the code and file are created, the new code needs to be compiled - if the function <*assemble_model*> is called inside a program which will use the new created models. Thus you need to call the *reload* function. You will need to add pythonic path/import:

    ~~~python
    import tests.test_model

    ...some code...

    reload_module(tests.test_model)
    ~~~

- **is_model()** this function is used to check if the model was created. You need to pass the <*table_name*> and <*abs_os_path_to_model*> arguments.

- **get_model()** you will retrieve the wanted database object of the SqlAlchemy model. It needs the <*table_name*> and <*py_path_to_model*> arguments.

- **is_module()** this is optional function if you want to check the pythonic path. It needs <*py_path_to_model*> argument.

### 🗂 Models

Created SqlAlchemy models have some additional features:

- default values
- parent-child relationships
- <*_post_init_*> method is used as validation
- when 'printing' the string will contain the model/object name and attributes names with their values.

All models are named with the same naming convention as they are in the database with one difference, they are capitalized (python class naming convention).


## 📝 Example

**Simple example how to use the code:**

~~~python
import os
from sqlalchemy import create_engine

from alchemyrohan.assemble import assemble_model
from alchemyrohan.utils import is_model
from alchemyrohan.utils import get_model
from alchemyrohan.utils import reload_module

import tests.test_model

dir = os.path.dirname(__file__)
conn = f"sqlite:///{dir}{os.sep}test_sqlite{os.sep}test.db"

engine = create_engine(conn)
table_name = 'child' # all names will be capitilized
abs_os_path_to_model = os.path.join(dir, 'test_model') # path
py_path_to_model = 'tests.test_model' # pythonic path

try:
    assemble_model(
        engine, 
        table_name, 
        abs_os_path_to_model,
        py_path_to_model
        )
except Exception as e:
    print(e)
    exit(1)

reload_module(tests.test_model) # compile the new code

if is_model(table_name, abs_os_path_to_model):
    model = get_model(table_name, py_path_to_model)
    print(f'SqlAlchemy model exist: {model}')
    
    exit(0)

print(f'Something unexpected went wrong')
exit(-1)

~~~

**Example of one created model**:

~~~python

from sqlalchemy import Column
from tests.test_model import Base
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import relationship


class Child(Base):
    __tablename__ = 'child'


    id = Column(INTEGER, primary_key=True)
    parent_id = Column(INTEGER, nullable=True, default=None)
    name = Column(TEXT, nullable=True, default=None)
    grade = Column(INTEGER, nullable=True, default=None)


    parent_Parent = relationship("Parent", back_populates="children_Child", lazy="joined")

    def __post_init__(self):

        if not isinstance(self.id, int):
            try:
                self.id = int(self.id)
            except:
                raise SyntaxError(f'< {self.id} > is not integer')
        
        if not isinstance(self.parent_id, int):
            try:
                self.parent_id = int(self.parent_id)
            except:
                raise SyntaxError(f'< {self.parent_id} > is not integer')
        
        if not isinstance(self.name, str):
            try:
                self.name = str(self.name)
            except:
                raise SyntaxError(f'< {self.name} > is not string')
        
        if not isinstance(self.grade, int):
            try:
                self.grade = int(self.grade)
            except:
                raise SyntaxError(f'< {self.grade} > is not integer')
        
    
    def __str__(self):

        return f'User(id={self.id},'\
			f'parent_id={self.parent_id},'\
			f'name={self.name},'\
			f'grade={self.grade})'

~~~ 


## 📚 Dependencies

- **sqlalchemy** (version 2.0.x) is an ORM and provides code for its models,
- **oracledb** (version 1.4.x) is used to shape a database table model with an oracle table schema.


## ❗Important Note

In some cases you will need to correct the code manually. 
This will be in case when:

- Your are creating only one model which has relationship to other tables, thus you will need to create also those models or delete the part of the code

- Your tables have no primary keys. SqlAlchemy needs one primary key

- Your database has some datatypes or features which were not yet been testet


## 📋 Release Notes


* ***v0.1.0*** - creation of the initial code and tested with SqLite database
* ***v0.2.0*** - tested with Oracle database
* ***v0.3.0*** - added additional functions
* ***v0.3.1*** - bug fixing
* ***v0.3.2*** - text fixing and adding third party licenses


## 📄 License and Third-Party Licenses

Alchemyrohan is MIT licensed, as found in the [LICENSE][1] file.

The following software components are included in this project:

* SqlAlchemy (MIT License)
* python-oracledb (Apache License 2.0) 

[THIRD PARTY LICENSES][2]


[1]: https://github.com/wamberger/alchemyrohan/blob/master/LICENSE
[2]: https://github.com/wamberger/alchemyrohan/blob/master/THIRD_PARTY_LICENSES