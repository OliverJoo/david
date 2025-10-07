# 아래의 클래스 2개 작성 (자동채점은 지정 class와 method시그니처와 반환 규약을 따라야 한다.)
# 1. Python 코드로 단순 연결 리스트 구조를 완성한다.
# 단순 연결 리스트의 이름은 linkedlist로 만든다.
# 단순 연결 리스트에 새로운 항목을 임의 위치에 추가 할 수 있도록 추가 함수를 insert() 로 추가한다.
# 단순 연결 리스트의 특정 항목을 삭제 할 수 있도록 삭제 함수를 delete()로 추가한다. -> 삭제완료시 삭제된 데이터 값을 리턴한다.
# 값은 숫자나 영어문자열 등의 값을 받아 저장할 수 있도록 만든다.
# 추가 함수의 경우 첫번째 항목으로도 추가 할 수 있어야 하고 마지막 항목으로도 추가가 가능해야 한다.
# 처음부터 끝까지 순차적으로 가져오는 to_list() 함수를 추가한다.
# 전체 데이타의 항목의 갯수를 가져오는 __len__(self) 함수를 추가한다.
# Error 종류는 IndexError 케이스를 에러 처리를 적절히 해줘야하고, 그 외엔 Exception 으로 처리 하거나 해당 관련 Error 처리를 하도록 한다.(단, 출제 문제에는 IndexError만 언급됨)

# 2. Python 코드로 원형 연결 리스트(Circular Linked List)를 구현한다 - 커서 기반 원형 연결 리스트/단일 구조 리스트
# 이때 원형 연결 리스트의 이름은 circularlist로 만든다.
# 원형 연결 리스트에 임의의 위치에 새로운 원소를 추가 할 수 있도록 추가 함수를 insert()로 만든다.
# - insert(value) -> None: 기존 노드가 0 개 일 경우, 단일 노드 원형을 구성하여 리턴 / 기존 노드 n개 일 경우, 커서 뒤 삽입 후 커서를 새 노드로 이동
# 원형 연결 리스트에서 특정 원소를 삭제하는 delete() 함수를 만든다
# - delete(value) -> bool: 값이 같은 첫 노드 삭제(성공시 True, 실패시 False). 삭제 노드가 커서면 이전 노드로 이동한다. 만약 노드가 1개 있고 삭제되면 빈 상태가 된다.
# 원형 연결 리스트에서 다음 항목으로 넘어 가서 항목을 가져오는 get_next() 함수를 추가한다.
# - get_next() -> Object | None: 기존 노드가 0개 일 경우, None 리턴 / n개 일 경우, 커서 다음 노드 이동후 그 값을 반환(리스트 순환)
# 데이타/값을 입력해서 검색하는 search() 함수를 추가하고 구현
# - search(value) -> bool: 해당 value의 데이타 존재 여부(True/False)를 반환
# Error 종류는 IndexError 케이스를 에러 처리를 적절히 해줘야하고, 그 외엔 Exception 으로 처리 하거나 해당 관련 Error 처리를 하도록 한다.(원형 연결 리스트에서는 Exception 처리 언급없음)

class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class linkedlist:
    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def to_list(self):
        out = []
        cur = self._head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def insert(self, index, value):
        if not isinstance(index, int):
            raise TypeError("index must be int")
        if index < 0 or index > self._size:
            raise IndexError(f"insert index out of range: {index}")

        new_node = _Node(value)
        if index == 0:
            new_node.next = self._head
            self._head = new_node
        else:
            prev = self._head
            for _ in range(index - 1):
                if prev is None:
                    raise RuntimeError("internal state corrupted")
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node

        self._size += 1

    def delete(self, index):
        if not isinstance(index, int):
            raise TypeError("index must be int")
        if index < 0 or index >= self._size:
            raise IndexError(f"index out of range: {index}")

        if index == 0:
            deleted = self._head
            self._head = self._head.next
        else:
            prev = self._head
            for _ in range(index - 1):
                if prev is None:
                    raise RuntimeError("internal state corrupted")
                prev = prev.next
            if prev is None or prev.next is None:
                raise RuntimeError("internal state corrupted")
            deleted = prev.next
            prev.next = deleted.next

        self._size -= 1
        return deleted.value


# -------------- 커서 기반 원형 연결 리스트: circularlist ---------------
class _CNode:
    __slots__ = ("value", "next")

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class circularlist:
    def __init__(self):
        self._cursor = None
        self._size = 0

    def __len__(self):
        return self._size  # 데이터 모델 규약 준수

    def insert(self, value):
        new_node = _CNode(value)
        if self._cursor is None:
            new_node.next = new_node
            self._cursor = new_node
        else:
            new_node.next = self._cursor.next
            self._cursor.next = new_node
            self._cursor = new_node
        self._size += 1

    def get_next(self):
        if self._cursor is None:
            return None
        self._cursor = self._cursor.next
        return self._cursor.value

    def search(self, value):
        if self._cursor is None:
            return False
        cur = self._cursor
        for _ in range(self._size):  # 원형이므로 최대 한 바퀴
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def delete(self, value):
        if self._cursor is None:
            return False

        prev = self._cursor
        cur = self._cursor.next
        for _ in range(self._size):
            if cur.value == value:
                if self._size == 1:
                    self._cursor = None
                else:
                    prev.next = cur.next
                    if self._cursor is cur:
                        self._cursor = prev
                self._size -= 1
                return True
            prev, cur = cur, cur.next

        return False


def _test_circularlist_spec():
    cl = circularlist()
    assert len(cl) == 0
    assert cl.get_next() is None

    # 삽입 3개
    for v in (1, 2, 3):
        cl.insert(v)
    assert len(cl) == 3
    assert cl.search(2) is True
    assert cl.search(999) is False

    # 순환 확인
    s1 = cl.get_next()
    s2 = cl.get_next()
    assert s1 in (1, 2, 3) and s2 in (1, 2, 3)

    # 삭제: 존재 값 -> True
    assert cl.delete(2) is True
    assert len(cl) == 2
    assert cl.search(2) is False

    # 커서가 가리키는 노드를 삭제했을 경우 커서는 이전 노드로 이동해야 함
    # 커서를 충분히 회전시켜 현재 커서를 특정 값으로 만든 뒤 그 값을 삭제
    cl.insert(4)  # [?, ?, 4] (cursor=4)
    assert cl.delete(4) is True  # cursor가 4였으므로 이전 노드로 이동
    assert len(cl) == 2

    # 실패: 미존재 값 -> False
    assert cl.delete(42) is False

    # 단일 노드 삭제 전이
    cl2 = circularlist()
    cl2.insert("x")
    assert cl2.delete("x") is True
    assert len(cl2) == 0
    assert cl2.get_next() is None


if __name__ == "__main__":
    # Linkedlist Test
    # ll = linkedlist()
    # ll.insert(0, "a")  # ["a"]
    # ll.insert(1, "b")  # ["a","b"]
    # ll.insert(1, "X")  # ["a","X","b"]
    # print(ll.to_list())  # ['a', 'X', 'b']
    # print(len(ll))  # 3
    # print(ll.delete(1))  # 'X' -> ["a","b"]
    # print(ll.to_list())  # ['a', 'b']
    # print(len(ll))  # 2
    #
    # print('=' * 40)
    # # Circularlist Test
    # cl = circularlist()
    # print(cl.get_next())        # None (빈 리스트)
    # cl.insert('A')              # 내부상태 - [A]
    # cl.insert('B')              # 내부상태 - [A,B] (cursor는 2)
    # cl.insert('C')              # 내부상태 - [A,B,C] (cursor는 3)
    # print(len(cl))              # 3
    # print(cl.get_next())        # A (3의 다음)
    # print(cl.get_next())        # B
    # print(cl.search('B'))       # True
    # print(cl.search(999))       # False
    # print(cl.delete('A'))       # True ('A' 삭제, cursor가 2였다면 이전 노드(1 또는 3)로 이동)
    # print(cl.delete(2))         # False
    # print(len(cl))              # 2
    # print([cl.get_next() for _ in range(4)])  # 예: ['C', 'B', 'C', 'B']
    # print(cl.delete(42))        # False (미존재)

    _test_circularlist_spec()
    print("ok_circularlist_spec")
