from decimal import (
    Decimal,
)


def test_call_to_self_struct(w3, get_contract):
    code = """
struct MyStruct:
    e1: decimal
    e2: timestamp

@public
@constant
def get_my_struct(_e1: decimal, _e2: timestamp) -> MyStruct:
    return MyStruct({e1: _e1, e2: _e2})

@public
@constant
def wrap_get_my_struct_WORKING(_e1: decimal) -> MyStruct:
    testing: MyStruct = self.get_my_struct(_e1, block.timestamp)
    return testing

@public
@constant
def wrap_get_my_struct_BROKEN(_e1: decimal) -> MyStruct:
    return self.get_my_struct(_e1, block.timestamp)
    """
    c = get_contract(code)
    assert c.wrap_get_my_struct_WORKING(Decimal('0.1')) == (
        Decimal('0.1'), w3.eth.getBlock(w3.eth.blockNumber)['timestamp']
    )
    assert c.wrap_get_my_struct_BROKEN(Decimal('0.1')) == (
        Decimal('0.1'), w3.eth.getBlock(w3.eth.blockNumber)['timestamp']
    )
