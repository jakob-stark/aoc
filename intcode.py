arities = {
    1: 4, #Take x, y, z write x+y to pos z
    2: 4, #" " x*y to pos z
    3: 2, #Write input to pos x
    4: 2, #Print item at pos x
    5: 3, #If pos x == 0: jump to pos y
    6: 3, #If pos x != 0: jump to pos y
    7: 4, #Write x < y to pos z
    8: 4, #Write x == y to pos z
    9: 2, #Change relative position
    99:0 #End of execution
} #Default arity is 1

functions = {
    1: lambda stack, lhs, rhs, location, modes: stack.set_item(location,
    stack.get_data(lhs, modes.pop()) + stack.get_data(rhs, modes.pop())),

    2: lambda stack, lhs, rhs, location, modes: stack.set_item(location,
    stack.get_data(lhs, modes.pop()) * stack.get_data(rhs, modes.pop())),

    3: lambda stack, location, modes: stack.set_item(location, int(input())),

    4: lambda stack, location, modes: print(stack.get_data(location,
                                                           modes.pop())),

}

def extract_command(integer):
    command = str(integer)
    if len(command) <= 2:
        return (integer, Stack())
    else:
        op = command[-2:]
        modes = command[:-2]
        return (int(op), Stack([int(char) for char in modes]))
 
 
class Stack:
    def __init__(self, iterable=[]):
        if iterable:
            self.stack = iterable
        else:
            self.stack = []

        self.rel_base = 0
        self.ip = 0

    def __len__(self):
        return len(self.stack)

    def __setitem__(self, index, value):
        if type(index) == slice:
            idx = index.stop + 1
        else:
            idx = index + 1
        if idx > len(self.stack):
            for _ in range(idx - len(self.stack)):
                self.stack.append(0)
        self.stack[index] = value

    def __getitem__(self, index):
        if type(index) == slice:
            idx = index.stop + 1
        else:
            idx = index + 1
        if idx >= len(self.stack):
            for _ in range(idx - len(self.stack)):
                self.stack.append(0)
        return self.stack[index]

    def __delitem__(self, what):
        del self.stack[what]

    def get_data(self, pos, mode):
        if mode == 0: #Position mode:
            return self.__getitem__(pos)
        elif mode == 1: #Immediate
            return pos
        elif mode == 2:
            x = self.rel_base + pos
            return self.__getitem__(x)

    def opcode_9(self, value):
        self.rel_base += value

    def pop(self):
        if len(self.stack):
            return self.stack.pop()
        else:
            return 0

    def set_item(self, location, value):
        self.__setitem__(location, value)

def main(program):
    prog = Stack([int(tkn) for tkn in program.split(",")])
    ip = 0

    while ip < len(prog):
        opcode, modes = extract_command(prog[ip])
        arity = arities[opcode]

        if opcode in [1, 2]:
            command = functions[opcode]
            lhs = prog[ip + 1]
            rhs = prog[ip + 2]
            location = prog[ip + 3]
            
            if len(modes) == 3 and modes[0] == 2:
                location += prog.rel_base

            command(prog, lhs, rhs, location, modes)
            ip += arity

        elif opcode == 3:
            command = functions[opcode]
            if len(modes) and modes[0] == 2:
                command(prog, prog[ip + 1] + prog.rel_base, modes)
            else:
                command(prog, *prog[ip+1 : ip + arity], modes)
            ip += arity
        elif opcode == 4:
            command = functions[opcode]
            command(prog, *prog[ip+1 : ip + arity], modes)
            ip += arity

        elif opcode == 5:
            condition = prog.get_data(prog[ip + 1], modes.pop())
            if condition:
                jump_position = prog.get_data(prog[ip + 2], modes.pop())
                ip = jump_position
            else:
                ip += arity

        elif opcode == 6:
            condition = prog.get_data(prog[ip + 1], modes.pop())
            if not condition:
                jump_position = prog.get_data(prog[ip + 2], modes.pop())
                ip = jump_position
            else:
                ip += arity

        elif opcode == 7:
            lhs = prog.get_data(prog[ip + 1], modes.pop())
            rhs = prog.get_data(prog[ip + 2], modes.pop())
            location = prog[ip + 3]

            if modes.pop() == 2:
                location += prog.rel_base

            if lhs < rhs:
                prog[location] = 1
            else:
                prog[location] = 0

            ip += arity

        elif opcode == 8:
            lhs = prog.get_data(prog[ip + 1], modes.pop())
            rhs = prog.get_data(prog[ip + 2], modes.pop())
            location = prog[ip + 3]

            if modes.pop() == 2:
                location += prog.rel_base

            if lhs == rhs:
                prog[location] = 1
            else:
                prog[location] = 0

            ip += arity

        elif opcode == 9:
            value = prog.get_data(prog[ip + 1], modes.pop())
            prog.opcode_9(value)
            ip += arity

        elif opcode == 99:
            break

    return "Final value: ", prog.stack

if __name__ == "__main__":
    program = input()
    main(program)
