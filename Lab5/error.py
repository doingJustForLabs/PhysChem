from statistics import mean

T = 298.15
P = 1e5


def find_error(
    x1_exp: list[float], y1_exp: list[float], myT: list[float], flasher2, file_name
):
    x_errors = []
    y_errors = []

    with open(file_name, "w", encoding="utf-8") as file:

        for i in range(5):
            x_exp = x1_exp[i]
            y_exp = y1_exp[i]
            z = (x_exp + y_exp) / 2
            zs = [z, 1 - z]

            res = flasher2.flash(T=myT[i], P=P, zs=zs)

            file.write(f"--- T = {myT[i]} K ---\n")
            file.write(f"Phases: {res.phase_count}\n")

            # Предсказанные значения
            if res.phase_count == 1:
                # Если одна фаза, считаем вторую равной 0
                x_model = 0.0 if res.VF == 1 else res.liquid0.zs[0]
                y_model = 0.0 if res.VF == 0 else res.gas.zs[0]
            else:
                x_model = res.liquid0.zs[0]
                y_model = res.gas.zs[0]

            x_err = abs(x_model - x_exp)
            y_err = abs(y_model - y_exp)

            x_errors.append(x_err)
            y_errors.append(y_err)

            file.write(
                f"x_exp = {x_exp}, x_model = {x_model:.6f}, error = {x_err:.6f}\n"
            )
            file.write(
                f"y_exp = {y_exp}, y_model = {y_model:.6f}, error = {y_err:.6f}\n\n"
            )

        # Средняя абсолютная ошибка:
        mae_x = mean(x_errors)
        mae_y = mean(y_errors)
        file.write(f"Средняя абсолютная ошибка по x: {mae_x:.6f}\n")
        file.write(f"Средняя абсолютная ошибка по y: {mae_y:.6f}\n")
