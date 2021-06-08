from random import randint, choice

OUTCOMES = {'You': 'You won!', 'Robot': 'The robot won!', 'Draw': 'It\'s a draw!'}


class ExitGameError(Exception):
    pass


class NumberGame:
    def __init__(self, lower=0, upper=1000000, overheat=0):
        self._lower = lower
        self._upper = upper
        self._overheat = overheat
        self._table = {'You': 0, 'Robot': 0, 'Draw': 0}

    def _number_validation(self, number: int) -> bool:
        if self._lower > number:
            print('The number can\'t be negative!\n')
            return False
        if number > self._upper:
            print(f'Invalid input! The number can\'t be bigger than {self._upper}.\n')
            return False
        return True

    def _take_input(self):
        while True:
            number = input('What is your number?\n')
            try:
                number = int(number)
                if self._number_validation(number):
                    return number
            except ValueError:
                if number.lower() == 'exit game':
                    raise ExitGameError
                else:
                    print('A string is not a valid input!\n')

    def _game(self, you_number: int) -> None:
        robot_number = randint(self._lower, self._upper)
        print(f'The robot entered the number {robot_number}.')
        goal_number = randint(self._lower, self._upper)
        print(f'The goal number is {goal_number}.')
        result = abs(goal_number - you_number) - abs(goal_number - robot_number)
        winner = 'You' if result < 0 else 'Robot' if result > 0 else 'Draw'
        print(OUTCOMES[winner])
        self._table[winner] += 1

    def play(self):
        try:
            while True:
                self._game(self._take_input())
        except ExitGameError:
            result_printer(self._table, self._overheat)


class RockPS:
    def __init__(self, overheat=0):
        self._table = {'You': 0, 'Robot': 0, 'Draw': 0}
        self._lose_dict = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock',
        }
        self._overheat = overheat

    def _game(self, you_move: str) -> None:
        robot_move = choice(list(self._lose_dict))
        print(f'The robot chose {robot_move}')
        winner = 'Draw' if robot_move == you_move \
            else 'You' if self._lose_dict[robot_move] == you_move else 'Robot'
        print(OUTCOMES[winner])
        self._table[winner] += 1

    def _take_input(self) -> str:
        while True:
            you_move = input('What is your move?\n').lower()
            if you_move in self._lose_dict:
                return you_move
            else:
                if you_move == 'exit game':
                    raise ExitGameError
                else:
                    print('No such option! Try again!')

    def play(self) -> None:
        try:
            while True:
                self._game(self._take_input())
        except ExitGameError:
            result_printer(self._table, self._overheat)


def result_printer(result: dict, overheat=0) -> None:
    if overheat < 90:
        print(
            f'You won: {result["You"]}',
            f'The robot won: {result["Robot"]}',
            f'Draws: {result["Draw"]}.',
            sep=',\n'
              )
    else:
        pass


if __name__ == '__main__':
    game = RockPS()
    game.play()
