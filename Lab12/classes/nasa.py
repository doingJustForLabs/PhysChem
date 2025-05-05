class NASA:
    def __init__(self):
        super().__init__()
        self._NASA: dict = {}

    def get_NASA(self) -> dict:
        return self._NASA

    def add_NASA_data(self, data: list[str] | str) -> None:
        if isinstance(data, str):
            substance, *coefficients = data.split()
            self._NASA[substance] = [float(i) for i in coefficients]
        else:
            for i in range(len(data)):
                substance, *coefficients = data[i].split()
                self._NASA[substance] = [float(i) for i in coefficients]


nasa_db = NASA()
