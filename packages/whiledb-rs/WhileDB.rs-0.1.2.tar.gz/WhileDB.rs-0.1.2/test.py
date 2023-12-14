import whiledb_rs
from pprint import pprint
pprint(whiledb_rs.parse("""
class list {
    fn __init__(self) {
        
    }
    fn append(self, elem) {
        
    }
}
                        
x = list();
x.append(20);
x.append(50);
print(x == [20, 50]);
"""))