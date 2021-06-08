from games import NumberGame, RockPS
from random import randint


class GameOverError(Exception):
    pass


class RoboPet:
    def __init__(self, name: str) -> None:
        self._name = name
        self._games = {}
        self._stats = {
            'the battery': 100,
            'overheat': 0,
            'skill': 0,
            'boredom': 0,
            'rust': 0,
        }
        self._interactions = {
            'exit': {'description': 'Exit', 'call': self._exit},
            'info': {'description': 'Check the vitals', 'call': self._print_info},
            'work': {'description': 'Work', 'call': self._work},
            'play': {'description': 'Play', 'call': self._play_game},
            'oil': {'description': 'Oil', 'call': self._oil},
            'recharge': {'description': 'Recharge', 'call': self._recharge},
            'sleep': {'description': 'Sleep mode', 'call': self._sleep},
            'learn': {'description': 'Learn skills', 'call': self._learn},
        }

    def _input_interaction(self) -> str:
        while True:
            print(f'Available interactions with {self._name}:')
            for name, value in self._interactions.items():
                print(f'{name} - {value["description"]}')
            action = input('Choose:\n').lower()
            if self._stats['the battery'] == 0 and action != 'recharge':
                print(f'The level of the battery is 0, {self._name} needs recharging!\n')
                continue
            if self._stats['boredom'] == 100 and action != 'play':
                print(f'{self._name} is too bored! {self._name} needs to have fun!.')
                continue
            if action in self._interactions:
                return action
            else:
                print('Invalid input, try again!\n')

    def add_game(self, game_name: str, game_class: object) -> None:
        self._games[game_name] = game_class

    def play(self) -> None:
        try:
            while True:
                self._interactions[self._input_interaction()]['call']()
        except GameOverError:
            pass

    def _play_game(self) -> None:
        chosen_game = input('Which game would you like to play?\n')
        while True:
            if chosen_game.lower() in self._games:
                self._games[chosen_game]().play()
                self._print_stat_with_changes('rust', self._unpleasant_event())
                self._print_stat_with_changes('boredom', -20)
                self._print_stat_with_changes('overheat', 10)
                if self._stats['boredom'] == 0:
                    print(f'{self._name} is in a great mood!')
                break
            else:
                print(f'\nPlease choose a valid option: {" or ".join(self._games)}?\n')
                chosen_game = input()

    def _print_info(self) -> None:
        result = f'{self._name}\'s stats are: '
        result += ',\n'.join([f'{stat if stat != "skill" else stat + " level"} is {val}'
                              for stat, val in self._stats.items()]) + '.\n'
        print(result)

    def _print_stat_with_changes(self, stat_name: str, value: int) -> None:
        old_value = self._stats[stat_name]
        new_value = self._stats[stat_name] + value
        new_value = 100 if new_value > 100 else 0 if new_value < 0 else new_value
        self._stats[stat_name] = new_value
        if new_value == 100:
            if stat_name == 'overheat':
                print(f'The level of overheat reached 100, {self._name} has blown up! Game over. Try again?')
                raise GameOverError
            if stat_name == 'rust':
                print(f'{self._name} is too rusty! Game over. Try again?')
                raise GameOverError
        if stat_name == 'boredom' or new_value != old_value:
            print(f'{self._name}\'s level of {stat_name} was {old_value}.'
                  f' Now it is {self._stats[stat_name]}.')

    def _recharge(self) -> None:
        if self._stats['the battery'] != 100:
            self._print_stat_with_changes('overheat', -5)
            self._print_stat_with_changes('the battery', 10)
            self._print_stat_with_changes('boredom', 5)
            print(f'{self._name} is recharged!')
            return
        if self._stats['the battery'] == 100:
            print(f'{self._name} is charged!')

    def _sleep(self) -> None:
        if self._stats['overheat'] > 0:
            print(f'\n{self._name} cooled off!\n')
            self._print_stat_with_changes('overheat', -20)
        if self._stats['overheat'] == 0:
            print(f'{self._name} is cool!')

    def _work(self) -> None:
        if self._stats['skill'] < 50:
            print(f'{self._name} has got to learn before working!\n')
        else:
            rust = self._unpleasant_event()
            self._print_stat_with_changes('rust', rust)
            self._print_stat_with_changes('boredom', 10)
            self._print_stat_with_changes('overheat', 10)
            self._print_stat_with_changes('the battery', -10)
            print(f'\n{self._name} did well!\n')

    def _learn(self) -> None:
        if self._stats['skill'] == 100:
            print(f'There\'s nothing for {self._name} to learn!')
        else:
            self._print_stat_with_changes('skill', 10)
            self._print_stat_with_changes('overheat', 10)
            self._print_stat_with_changes('the battery', -10)
            self._print_stat_with_changes('boredom', 5)
            print(f'\n{self._name} has become smarter!\n')

    def _oil(self) -> None:
        if self._stats['rust'] == 0:
            print(f'{self._name} is fine, no need to oil!\n')
        else:
            self._print_stat_with_changes('rust', -20)
            print(f'{self._name} is less rusty.\n')

    def _unpleasant_event(self) -> int:
        cases = {0: self._puddle, 1: self._sprinkler, 2: self._pool, 3: lambda: 0}
        return cases[randint(0, 3)]()

    def _puddle(self) -> int:
        print(f'Oh no, {self._name} stepped into a puddle!\n')
        return 10

    def _sprinkler(self) -> int:
        print(f'Oh, {self._name} encountered a sprinkler!\n')
        return 30

    def _pool(self) -> int:
        print(f'Guess what! {self._name} fell into the pool!\n')
        return 50

    @staticmethod
    def _exit() -> None:
        print('Game over.')
        raise GameOverError


if __name__ == '__main__':
    game = RoboPet(input('How will you call your robot?\n'))
    game.add_game('numbers', NumberGame)
    game.add_game('rock-paper-scissors', RockPS)
    game.play()
