import serial

arduino = serial.Serial('COM5', 9600)
bit_num = 2**10


def get_data(arduino: serial.Serial) -> list[int]:
    while True:
        p1 = arduino.read_until(b'\n').decode().split()
        p2 = arduino.read_until(b'\n').decode().split()
        p1 = [int(s) for s in p1]
        p2 = [int(s) for s in p2]
        match len(p1):
            case 3:
                return p1
            case 2:
                return [p2[0]]+p1
            case 1:
                return [p2[0], p2[1]]+p1
            case 0:
                return p2


def parse_data(data: list[int],
               x_num: int = 2, y_num: int = 2,
               x_seg: list[int] = None, y_seg: list[int] = None,
               x_dir: str = 'r', y_dir: str = 'd') -> list[int]:
    '''
    x_dir = 'r' / 'l', y_dir = 'd' / 'u'
    '''
    data_par: list[int] = []
    if not x_seg:
        data[0] -= 512
        x_seg = ([-i*(bit_num/2)/x_num for i in range(x_num, 0, -1)]
                 + [i*(bit_num/2)/x_num for i in range(1, x_num+1)])
    match x_dir:
        case 'r':
            pass
        case 'l':
            x_seg.reverse()
    for i in range(len(x_seg)-1):
        if data[0] >= x_seg[i] and data[0] < x_seg[i+1]:
            data_par.append(i)
            break
    if not y_seg:
        data[1] -= 512
        y_seg = ([-i*(bit_num/2)/y_num for i in range(y_num, 0, -1)]
                 + [i*(bit_num/2)/y_num for i in range(1, y_num+1)])
    match y_dir:
        case 'd':
            pass
        case 'u':
            y_seg.reverse()
    for i in range(len(y_seg)-1):
        if data[1] >= y_seg[i] and data[1] < y_seg[i+1]:
            data_par.append(i)
            break
    data_par.append(data[2])
    return data_par

if __name__ == '__main__':
    while True:
        print(parse_data(get_data(arduino)))
