from argparse import ArgumentParser


class FlexParser(ArgumentParser):
    target_str: str

    def __init__(self) -> None:
        super().__init__(add_help=False)
        self.add_argument("target_str")
        self.__parse()

    def __parse(self) -> None:
        args = self.parse_args()
        self.target_str = args.target_str
