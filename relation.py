from collections import namedtuple

# type alias
Schema = namedtuple

class Relation:
    def __init__(self, schema, tuples=None):
        self.schema = schema
        self.tuples = tuples if tuples is not None else set()

    def add(self, **kwargs):
        t = self.schema(**kwargs)
        self.tuples.add(t)

    def __str__(self):
        l = [
            self.schema.__name__,
            "\t" + "\t".join(map(str, self.schema._fields)),
            *map(lambda t: "\t" + str(t),
                map(lambda d: "\t".join(map(str, d.values())),
                    map(lambda t: t._asdict(),
                        self.tuples
                    )
                )
            )
        ]
        return "\n".join(l)


def main():
    customer = Relation(Schema("Customer", "id, fname, lname, age, height"))
    customer.add(id=18392, fname="Frank", lname="Smith", age=45, height="5'8")
    customer.add(id=48921, fname="Jane", lname="Doe", age=42, height="5'6")

    print(customer)
    # output:
    #
    # Customer
    #     id      fname   lname   age     height
    #     18392   Frank   Smith   45      5'8
    #     48921   Jane    Doe     42      5'6

if __name__ == '__main__':
    main()
