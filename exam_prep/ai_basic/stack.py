class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next


class Stack:
    MAX_SIZE = 10

    def __init__(self):
        self._top = None
        self._size = 0

    def empty(self) -> bool:
        return self._top is None

    def size(self):
        return self._size

    def push(self, item) -> bool:
        if self.size() >= self.MAX_SIZE:
            print(f'Stack is Full!')
            return False

        new_node = Node(item, self._top)
        self._top = new_node
        self._size += 1
        return True

    def pop(self) -> object | None:
        if self.empty():
            print('Empty Stack!')
            return None

        item = self._top.item
        self._top = self._top.next
        self._size -= 1
        return item

    def peek(self) -> object | None:
        if self.empty():
            print('Empty Stack!')
            return None
        return self._top.item

    def __str__(self):
        items = []
        cur = self._top
        while cur:
            items.append(cur.item)
            cur = cur.next
        return f'Stack({items[::-1]})'


def main():
    print('==' * 60)
    print('클래스 기반 스택 테스트')
    print('==' * 60)

    # 테스트 1: 초기 상태 검증
    print('\n[테스트 1] 초기 상태 검증')
    stack = Stack()
    print(f'empty() 결과: {stack.empty()}')  # 출력: True
    print(f'size() 결과: {stack.size()}')  # 출력: 0

    # 테스트 2: 단일 요소 push/pop
    print('\n[테스트 2] 단일 요소 push/pop')
    stack.push('항목#1')
    print(f'push 후 empty(): {stack.empty()}')  # 출력: False
    print(f'peek() 결과: {stack.peek()}')  # 출력: 항목#1
    print(f'pop() 결과: {stack.pop()}')  # 출력: 항목#1
    print(f'pop 후 empty(): {stack.empty()}')  # 출력: True

    # 테스트 3: LIFO 순서 검증 (고유 번호 사용)
    print('\n[테스트 3] LIFO 순서 검증')
    for i in range(1, 6):
        stack.push(f'데이터#{i}')
    print(f'5개 push 후 size: {stack.size()}')  # 출력: 5
    print('pop 순서:')
    while not stack.empty():
        print(f'-> {stack.pop()}')  # 출력: 데이터#5, 데이터#4, 데이터#3, 데이터#2, 데이터#1

    # 테스트 4: 최대 용량 체크 (10개 제한)
    print('\n[테스트 4] 최대 용량 체크')
    stack = Stack()  # 새 스택 생성
    for i in range(1, 12):  # 11개 시도
        result = stack.push(f'요소#{i}')
        if not result:
            print(f' {i}번째 push 실패')
    print(f'최종 size: {stack.size()}')  # 출력: 10

    # 테스트 5: 빈 스택에서 pop/peek 시도
    print('\n[테스트 5] 빈 스택 경계 조건')
    empty_stack = Stack()
    empty_stack.pop()  # 경고 메시지 출력
    empty_stack.peek()  # 경고 메시지 출력

    # 테스트 6: peek는 요소를 제거하지 않음
    print('\n[테스트 6] peek의 비파괴적 특성')
    stack = Stack()
    stack.push('확인용')
    print(f'1st peek: {stack.peek()}')  # 출력: 확인용
    print(f'2nd peek: {stack.peek()}')  # 출력: 확인용
    print(f'size 유지: {stack.size()}')  # 출력: 1

    # 테스트 7: 다양한 데이터 타입
    print('\n[테스트 7] 다양한 데이터 타입')
    stack = Stack()
    stack.push(42)  # int
    stack.push(3.14)  # float
    stack.push([1, 2, 3])  # list
    stack.push({'key': 'value'})  # dict
    print(f'pop: {stack.pop()}')  # 출력: {'key': 'value'}
    print(f'pop: {stack.pop()}')  # 출력: [1, 2, 3]
    print(f'pop: {stack.pop()}')  # 출력: 3.14
    print(f'pop: {stack.pop()}')  # 출력: 42

    # 테스트 8: 교대로 push/pop
    print('\n[테스트 8] 교대로 push/pop')
    stack = Stack()
    stack.push('A')
    stack.push('B')
    print(f'pop: {stack.pop()}')  # 출력: B
    stack.push('C')
    print(f'pop: {stack.pop()}')  # 출력: C
    print(f'pop: {stack.pop()}')  # 출력: A
    print(f'empty: {stack.empty()}')  # 출력: True
    print('\n' + '=' * 60)


if __name__ == '__main__':
    main()
