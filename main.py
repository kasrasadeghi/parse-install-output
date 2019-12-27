#!/usr/bin/python3

def main():
    filename = 'output-ogre-build-install-1.9.1.txt'
    with open(filename) as f:
        content = f.read()

    install_content = content.split('Install the project...\n')[1]
    file_lines = install_content.splitlines()[1:]

    files = map(lambda l: l.split(": ")[1], file_lines)
    root = treeify(files)
    fold_lowest_folders(root)

    s = '\n'.join(l for l in root.repr_collapsed().splitlines() if '.' not in l)
    print(s)


def fold_lowest_folders(node):
    # if every child has no children

    if all(len(c.children) == 0 for c in node.children):
        node.collapsed = True
    
    for c in node.children:
        fold_lowest_folders(c)


def treeify(filenames):
    root = Node('/')
    for n in filenames:
        root.insert(n[1:].split('/'))
    return root
    


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def insert(self, path):
        head = path[0]
        rest = path[1:]

        if not rest:
            if not self.getName(head):
                self.children.append(Node(head))

        if rest:
            if self.getName(head):
                child = self.getName(head)
                child.insert(rest)
            else:
                child = Node(head)
                self.children.append(child)
                child.insert(rest)

    def paren(self):
        if self.children:
            return f"({self.name} " + (" ".join(list(map(lambda n: n.paren(), self.children)))) + ")"
        else:
            return self.name
        
    def __repr__(self):
        if self.children:
            me = self.name + '\n'
            acc = ''
            for c in self.children:
                acc += c.__repr__() + '\n'
            return me + indent(acc)
        else:
            return self.name
    
    def repr_collapsed(self):
        # if '.' in self.name:
            # return ''
        if self.children:
            me = self.name + '\n'
            acc = ''
            for c in self.children:
                acc += c.repr_collapsed() + '\n'
            return me + indent(acc)
        else:
            return self.name

    def getName(self, name):
        l = [x for x in self.children if x.name == name]
        if l:
            return l[0]
        else:
            return None
        

def indent(text):
    return "\n".join(map(lambda l: "| " + l, text.splitlines()))

if __name__ == '__main__':
    main()
