def hook_right(left_node, right_node):
    left_node.right.left = right_node
    right_node.right = left_node.right
    left_node.right = right_node
    right_node.left = left_node


def hook_down(up_node, down_node):
    up_node.down.up = down_node
    down_node.down = up_node.down
    up_node.down = down_node
    down_node.up = up_node


def unhook_right(node):
    node.right.left = node.left
    node.left.right = node.right


def unhook_down(node):
    node.down.up = node.up
    node.up.down = node.down


def cover(column):
    # Unhook the column header.
    unhook_right(column)

    # Unhook all rows in this column.
    i = column.down
    while i != column:
        j = i.right
        while j != i:
            unhook_down(j)
            j = j.right
        i = i.down


def uncover(column):
    # Re-hook all rows in this column.
    i = column.up
    while i != column:
        j = i.left
        while j != i:
            hook_down(j.up, j)
            j = j.left
        i = i.up

    # Re-hook the column header.
    hook_right(column.left, column)


class Node:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = None


class DancingLinks:
    def __init__(self, columns, max_solution=float('inf')):
        self.head = Node()
        self.columns = []
        for i in range(columns):
            column = Node()
            column.column = column
            self.columns.append(column)
            hook_right(self.head.left, column)

        self.max_solution = max_solution

    def append_row(self, row):
        start_node = None
        for j in row:
            node = Node()
            column = self.columns[j]

            node.column = j
            column.up.down = node

            node.up = column.up
            node.down = column

            column.up = node
            if start_node:
                hook_right(start_node.left, node)
            else:
                start_node = node

    def search(self):
        if not self.head.right or self.head.right == self.head:
            yield []
            return

        # Choose a column deterministically.
        column = self.head.right.column

        # Cover the chosen column.
        cover(column)

        # Try each row in the chosen column.
        row_node = column.down
        solution_count = 0
        while row_node != column:
            # Add the row to the partial solution.
            solution_row_nodes = [row_node]

            # Cover all other columns with a 1 in this row.
            right_node = row_node.right
            while right_node != row_node:
                cover(self.columns[right_node.column])
                solution_row_nodes.append(right_node)
                right_node = right_node.right

            # Recurse to find more solutions.
            for solution in self.search():
                if solution_count == self.max_solution:
                    break
                solution_count += 1
                yield solution + [[node.column for node in solution_row_nodes]]

            # Uncover all other columns with a 1 in this row.
            left_node = row_node.left
            while left_node != row_node:
                uncover(self.columns[left_node.column])
                left_node = left_node.left

            # Move to the next row in the chosen column.
            row_node = row_node.down

        # Uncover the chosen column.
        uncover(column)


if __name__ == "__main__":
    # 创建一个 DancingLinks 对象，表示一个 7 列的矩阵。
    dlx = DancingLinks(7)

    # 向矩阵中添加四行。
    dlx.append_row([0, 1, 2, 5])
    dlx.append_row([0, 3, 6])
    dlx.append_row([0, 3])
    dlx.append_row([3, 4, 6])
    dlx.append_row([1, 2, 4, 5])

    # 搜索矩阵的所有精确覆盖解。
    for solution in dlx.search():
        print(solution)
