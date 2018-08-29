from xml.dom import minidom
import argparse
import yaml

try:
    import seaborn as sns
except ImportError:
    pass
import matplotlib.pyplot as plt

def lmap(fn, iterable):
    return list(map(fn, iterable))

def extract_path(doc, id_):
    for el in doc.getElementsByTagName('path'):

        if el.getAttribute('id') == id_:
            return(el.getAttribute('d'))

    raise ValueError(f"path not found: {id_}")

def parse_path(path):
    x = 0
    y = 0

    coords = []
    path = path.split(' ')

    while len(path) > 0:
        i = path[0]
        path = path[1:]


        if len(i) == 0:
            continue
        elif i == 'M' or i == 'L':
            x,y = lmap(float, path[:2])
            path = path[2:]
            coords.append((x,y))
        else:
            raise NotImplementedError(i)

    return coords

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-x0', type=str, required=True, metavar='pathNNNN,0.2')
    parser.add_argument('-x1', type=str, required=True, metavar='pathNNNN,0.4')
    parser.add_argument('-y0', type=str, required=True, metavar='pathNNNN,0.2')
    parser.add_argument('-y1', type=str, required=True, metavar='pathNNNN,0.4')

    parser.add_argument('-path', type=str, required=True, nargs='+', metavar='name,pathNNNN')

    parser.add_argument('-svg', type=str, required=True)
    parser.add_argument('-output', type=str)

    parser.add_argument('--plot', action='store_true')

    return parser.parse_args()

def parse_ref(doc, arg0, arg1, coord):
    arg0_path, arg0_coord = arg0.split(',')
    arg0_coord = float(arg0_coord)

    arg1_path, arg1_coord = arg1.split(',')
    arg1_coord = float(arg1_coord)

    arg0_path = parse_path(extract_path(doc, arg0_path))
    arg1_path = parse_path(extract_path(doc, arg1_path))

    c0 = arg0_path[0][coord]
    c1 = arg1_path[0][coord]
    dc = (c1-c0) / (arg1_coord-arg0_coord)

    return c0, dc, arg0_coord

def plot_data(result):
    f = plt.figure()
    ax = f.add_subplot(111)

    for k, v in result.items():
        ax.plot(v['x'], v['y'], 'o-', label=k)

    ax.legend()
    plt.show()


def main():
    args = parse_args()

    doc = minidom.parse(args.svg)

    svg_y0, svg_dy, real_y0 = parse_ref(doc, args.y0, args.y1, 1)
    svg_x0, svg_dx, real_x0 = parse_ref(doc, args.x0, args.x1, 0)

    result = {}
    for path in args.path:
        name, id_ = path.split(',')

        x = []
        y = []
        coords = parse_path(extract_path(doc, id_))

        for cx, cy in coords:
            rx = real_x0 + (cx - svg_x0) / svg_dx
            ry = real_y0 + (cy - svg_y0) / svg_dy
            x.append(rx)
            y.append(ry)

        result[name] = {"x": x, "y": y}

        print(name)
        print(f"  x: {str(x)}")
        print(f"  y: {str(y)}")

    if args.plot:
        plot_data(result)

    if args.output:
        with open(args.output, "w") as f:
            f.write(yaml.dump(result))

    doc.unlink()

if __name__ == '__main__':
    main()
