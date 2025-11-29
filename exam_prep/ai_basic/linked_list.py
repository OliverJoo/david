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
# - delete(value) -> bool: 값이 같은 첫 노드 삭제(성공시 True, 실패시 False). 삭제 노드가 커서면 이전 노드로 이동한다. 만약 노드가 1개 있고 삭제되면 빈 상태가 된다.
# 원형 연결 리스트에서 다음 항목으로 넘어 가서 항목을 가져오는 get_next() 함수를 추가한다.
# - insert(value) -> None: 기존 노드가 0 개 일 경우, 단일 노드 원형을 구성하여 리턴 / 기존 노드 n개 일 경우, 커서 뒤 삽입 후 커서를 새 노드로 이동
# - get_next() -> Object | None: 기존 노드가 0개 일 경우, None 리턴 / n개 일 경우, 커서 다음 노드 이동후 그 값을 반환(리스트 순환)
# 데이타/값을 입력해서 검색하는 search() 함수를 추가하고 구현
# - search(value) -> bool: 해당 value의 데이타 존재 여부(True/False)를 반환
# 원형 연결 리스트에서 특정 원소를 삭제하는 delete() 함수를 만든다
# Error 종류는 IndexError 케이스를 에러 처리를 적절히 해줘야하고, 그 외엔 Exception 으로 처리 하거나 해당 관련 Error 처리를 하도록 한다.(원형 연결 리스트에서는 Exception 처리 언급없음)

class _Node:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class LinkedList:
    def __init__(self):
        self._head = None
        self._size = 0

    def insert(self, index, value):
        if not isinstance(index, int):
            raise TypeError('index must be int')
        if index < 0 or index > self._size:
            raise IndexError(f'insert index out of range: {index}')

        new_node = _Node(value)
        if index == 0:
            new_node.next = self._head
            self._head = new_node
        else:
            prev = self._head
            for _ in range(index - 1):
                if prev is None:
                    raise RuntimeError('internal state corrupted')
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node

        self._size += 1

    def delete(self, index):
        if not isinstance(index, int):
            raise TypeError('index must be int')
        if index < 0 or index >= self._size:
            raise IndexError('index out of range: %s' % index)

        if index == 0:
            deleted = self._head
            self._head = self._head.next
        else:
            prev = self._head
            for _ in range(index - 1):
                if prev is None:
                    raise RuntimeError('internal state corrupted')
                prev = prev.next
            if prev is None or prev.next is None:
                raise RuntimeError('internal state corrupted')
            deleted = prev.next
            prev.next = deleted.next
        self._size -= 1
        return deleted.value

    def to_list(self):
        out = []
        cur = self._head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def __len__(self):
        return self._size


# -------------- 커서 기반 원형 연결 리스트: circularlist ---------------
class _CNode:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt

class CircularList:
    def __init__(self):
        self._cursor = None
        self._size = 0

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

    # - delete(value) -> bool: 값이 같은 첫 노드 삭제(성공시 True, 실패시 False). 삭제 노드가 커서면 이전 노드로 이동한다. 만약 노드가 1개 있고 삭제되면 빈 상태가 된다.

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

    def get_next(self):
        if self._cursor is None:
            return None
        self._cursor = self._cursor.next
        return self._cursor.value

    def search(self, value):
        if self._cursor is None:
            return False
        cur = self._cursor
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def __len__(self):
        return self._size



if __name__ == "__main__":

    try:
        input_data = input().strip()
    except EOFError:
        input_data = '1'

    if input_data == '1':
        # LinkedList 테스트 (기존 + 추가)
        ll = LinkedList()

        # 기본 테스트
        ll.insert(0, 'a')
        ll.insert(1, 'b')
        ll.insert(1, 'X')
        print(ll.to_list())  # 예상: ['a', 'X', 'b']
        print(len(ll))  # 예상: 3
        print(ll.delete(1))  # 예상: X
        print(ll.to_list())  # 예상: ['a', 'b']
        print(len(ll))  # 예상: 2

        # 추가 테스트 (2배 확장)
        ll.insert(0, 'Z')  # 맨 앞 삽입
        print(ll.to_list())  # 예상: ['Z', 'a', 'b']
        ll.insert(3, 'Y')  # 맨 뒤 삽입
        print(ll.to_list())  # 예상: ['Z', 'a', 'b', 'Y']
        print(len(ll))  # 예상: 4
        print(ll.delete(0))  # 예상: Z (맨 앞 삭제)
        print(ll.delete(2))  # 예상: Y (맨 뒤 삭제)
        print(ll.to_list())  # 예상: ['a', 'b']

    else:
        # CircularList 테스트 (기존 + 추가)
        cl = CircularList()

        # 기본 테스트
        print(cl.get_next())  # 예상: None
        cl.insert('A')
        cl.insert('B')
        cl.insert('C')
        print(len(cl))  # 예상: 3
        print(cl.get_next())  # 예상: A
        print(cl.get_next())  # 예상: B
        print(cl.search('B'))  # 예상: True
        print(cl.search(999))  # 예상: False
        print(cl.delete('A'))  # 예상: True
        print(cl.delete(2))  # 예상: False
        print(len(cl))  # 예상: 2
        print([cl.get_next() for _ in range(4)])  # 예상: ['C', 'B', 'C', 'B']
        print(cl.delete(42))  # 예상: False

        # 추가 테스트 (2배 확장)
        cl.insert('D')  # 추가 삽입
        print(len(cl))  # 예상: 3
        print(cl.search('D'))  # 예상: True
        print(cl.get_next())  # 예상: B (순환 계속)
        print(cl.delete('C'))  # 예상: True
        print(len(cl))  # 예상: 2
        print([cl.get_next() for _ in range(4)])  # 예상: ['D', 'B', 'D', 'B']

# ===== linkedlist result =====
# ['a', 'X', 'b']
# 3
# X
# ['a', 'b']
# 2
# ['Z', 'a', 'b']
# ['Z', 'a', 'b', 'Y']
# 4
# Z
# Y
# ['a', 'b']

# ===== circularlist result =====
# None
# 3
# A
# B
# True
# False
# True
# False
# 2
# ['C', 'B', 'C', 'B']
# False
# 3
# True
# C
# True
# 2
# ['B', 'D', 'B', 'D']
