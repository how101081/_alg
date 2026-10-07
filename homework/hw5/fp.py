def my_map(f, xs):
    return [] if not xs else [f(xs[0])] + my_map(f, xs[1:])


def my_filter(f, xs):
    if not xs:
        return []
    rest = my_filter(f, xs[1:])
    return [xs[0]] + rest if f(xs[0]) else rest


def my_reduce(f, xs, init):
    return init if not xs else my_reduce(f, xs[1:], f(init, xs[0]))


def bubble_pass(xs):
    def step(acc, x):
        out, carry = acc
        if carry > x:
            return out + [x], carry
        return out + [carry], x

    out, carry = my_reduce(step, xs[1:], ([], xs[0]))
    return out + [carry]


def bubble_sort(xs):
    if len(xs) <= 1:
        return xs
    ys = bubble_pass(xs)
    return bubble_sort(ys[:-1]) + ys[-1:]


data = [5, 2, 9, 1, 5, 6, 3]

print("自製 map / filter / reduce\n")
print(f"  my_map(x*2)      = {my_map(lambda x: x * 2, data)}")
print(f"  my_filter(奇數)   = {my_filter(lambda x: x % 2 == 1, data)}")
print(f"  my_reduce(+)     = {my_reduce(lambda a, b: a + b, data, 0)}")

print("\n禁止迴圈的泡沫排序（只用 map/filter/reduce + 遞迴）\n")
print(f"  排序前: {data}")
print(f"  排序後: {bubble_sort(data)}")
