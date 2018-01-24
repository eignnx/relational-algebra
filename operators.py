from relation import Schema, Relation

class OperatorProducer:
    def __init__(self, producer_fn):
        self.producer_fn = producer_fn

    def __getitem__(self, *args):
        return self.producer_fn(args[0]) # Don't unpack. Pass as list. But do flatten.

def _pi_impl(attrs):
    def fn(relation: Relation):
        
        assert set(attrs) <= set(relation.schema._fields), \
        "Projection attributes must be a subset of relation's schema's attributes!"

        new_schema_name = relation.schema.__name__ + "__" + "_".join(attrs)
        new_schema = Schema(new_schema_name, attrs)
        new_relation = Relation(new_schema)

        for tup in relation.tuples:
            values = []
            for attr_name in new_schema._fields:
                values.append(getattr(tup, attr_name))
            new_tup = new_schema._make(values)
            new_relation.tuples.add(new_tup)

        return new_relation
    return fn

Pi = OperatorProducer(_pi_impl)

def _sigma_impl(pred):
    def fn(relation):
        new_relation = Relation(relation.schema)
        new_relation.tuples = set(filter(pred, relation.tuples))
        return new_relation
    return fn

Sigma = OperatorProducer(_sigma_impl)

def _rho_impl(new_name):
    def fn(relation):
        return Relation(Schema(new_name, relation.schema._fields), relation.tuples)
    return fn

Rho = OperatorProducer(_rho_impl)

def main():
    customer = Relation(Schema("Customer", "id, fname, lname, age, height"))
    customer.add(id=18392, fname="Frank", lname="Smith", age=45, height="5'8")
    customer.add(id=48921, fname="Jane", lname="Doe", age=42, height="5'6")

    print(customer)

    # output:
    #
    # Customer
    #     id      fname   lname   age     height
    #     48921   Jane    Doe     42      5'6
    #     18392   Frank   Smith   45      5'8

    print()
    print(Pi["fname", "id"](customer))

    # output:
    #
    # Customer__fname_id
    #     fname   id
    #     Frank   18392
    #     Jane    48921

    print()
    print(Sigma[lambda tup: tup.age > 43](customer))

    # output:
    #
    # Customer
    #     id      fname   lname   age     height
    #     18392   Frank   Smith   45      5'8

    print()
    print(Rho["MySchema"](Pi["fname", "id"](customer)))

    # output:
    #
    # MySchema
    #     fname   id
    #     Frank   18392
    #     Jane    48921

if __name__ == '__main__':
    main()
