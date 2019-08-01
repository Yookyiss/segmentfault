# -*- coding:utf-8 -*-
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
class Solution:
    def HasSubtree(self, pRoot1, pRoot2):
        # write code here
        self.res = False

        def dp(r1, r2):
            print(r1, r2)
            if not r1 and r2:
                return False
            if not r2:
                return True
            if r1 and r2 and r1.val == r2.val:
                return dp(r1.left, r2.left) and dp(r1.right, r2.right)
            return False

        def pre(root):
            if not root:return None
            if root.val == pRoot2.val:
                if dp(root, pRoot2):
                    self.res = True
                    return
            pre(root.left)
            pre(root.right)

        pre(pRoot1)

        return self.res

d1 = TreeNode(8)
d2 = TreeNode(8)
d3 = TreeNode(7)
d4 = TreeNode(9)
d5 = TreeNode(2)
d6 = TreeNode(4)
d7 = TreeNode(7)

d11 = TreeNode(8)
d12 = TreeNode(9)
d13 = TreeNode(2)

d1.left = d2
d1.right = d3
d2.left = d4
d2.right = d5
d5.left = d6
d5.right = d7

d11.left = d12
d11.right = d13

Solution().HasSubtree(d1,d11)
