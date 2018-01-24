# relational-algebra
Functions and types for working with mathematical relations.

## Example

```python
from relation import Relation, Schema
from operators import Pi, Sigma, Rho

customer = Relation(Schema("Customer", "id, fname, lname, age, height"))

customer.add(id=18392, fname="Frank", lname="Smith", age=45, height="5'8")
customer.add(id=48921, fname="Jane", lname="Doe", age=42, height="5'6")

print(customer)
proj = Pi["fname", "id"](customer)
print(proj)
print(Sigma[lambda tup: tup.age > 43](customer))
print(Rho["MySchema"](proj))
```

Output:
```
Customer
    id      fname   lname   age     height
    48921   Jane    Doe     42      5'6
    18392   Frank   Smith   45      5'8

Customer__fname_id
    fname   id
    Frank   18392
    Jane    48921

Customer
    id      fname   lname   age     height
    18392   Frank   Smith   45      5'8

MySchema
    fname   id
    Frank   18392
    Jane    48921
```