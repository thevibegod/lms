from tqdm import tqdm

EASY = 0
MEDIUM = 1
HARD = 2
MODES = {EASY: 300, MEDIUM: 750, HARD: 1000}

MINIMUM = 1

file = open('dataset.csv', 'w')
file.write('Mode,Expected Time,Actual Time,Correct Answers,Next Mode\n')


def write_data(*args):
    data = [str(arg) for arg in args]
    file.write(','.join(data) + '\n')


def generate_modes():
    for mode, time in tqdm(MODES.items()):
        generate_time(mode, time)


def generate_time(mode, expected_time):
    for i in range(MINIMUM, expected_time * 2):
        generate_correct_answers(mode, expected_time, i)


def generate_correct_answers(mode, expected_time, actual_time):
    for i in range(0, 6):
        generate_next_mode(mode, expected_time, actual_time, i)


def generate_next_mode(mode, expected_time, actual_time, correct_answers):
    deviation = actual_time - expected_time
    sign = int(deviation >= 0)
    modulus = abs(deviation)

    if correct_answers >= 4:
        if sign:
            if modulus > (expected_time // 2):
                next_mode = mode - 1 if mode > 0 else mode
            else:
                next_mode = mode
        else:
            next_mode = mode + 1 if mode < 2 else mode
    else:
        next_mode = mode - 1 if mode > 0 else mode

    write_data(mode, expected_time, actual_time, correct_answers, next_mode)


generate_modes()
print('Dataset generated.')
file.close()
