from typing import Optional

from matplotlib import pyplot as plt


class BaseGraphic:
    def __init__(self, figsize: Optional[tuple[int, int]] = None):
        self._fig, self._ax = plt.subplots(figsize=figsize)

    def set_title(self, title: str) -> None:
        self._ax.set_title(title)

    def set_labels(self, xlabel: str, ylabel: str) -> None:
        self._ax.set_xlabel(xlabel)
        self._ax.set_ylabel(ylabel)

    def add_grid_and_axes(self) -> None:
        self._ax.grid()

    @staticmethod
    def show_and_save(filepath: str = None) -> None:
        """Отображает и сохраняет график, если указан файл"""
        if filepath:
            plt.savefig(filepath)
        plt.show()


class DependencyGraphic(BaseGraphic):

    def __init__(
        self,
        x: list[float],
        y: list[float],
        title: str = "",
        grid: bool = True,
        figsize: Optional[tuple[int, int]] = None,
        filepath: Optional[str] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
    ):
        super().__init__(figsize=figsize)
        self._x = x
        self._y = y
        self._title = title
        self._grid = grid
        self._figsize = figsize
        self._filepath = filepath
        self._labels = (xlabel, ylabel)
        self.create_graphic()

    def create_graphic(self) -> None:
        self._ax.plot(self._x, self._y, label="График зависимости H от T")
        self.set_title(self._title)
        self.set_labels(*self._labels)
        if self._grid:
            self.add_grid_and_axes()

    def add_plot(self, x, y, label: str = ""):
        self._ax.plot(x, y, label=label)
        self._ax.legend()
