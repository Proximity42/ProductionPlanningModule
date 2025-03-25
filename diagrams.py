import datetime
import plotly.express as px
import pandas as pd

from colors import ColorPalette


class DiagramCreator:

    @classmethod
    def create_gantt_diagram(
        cls, matrix: list[list[float | int]], machines: int, details: int
    ) -> None:
        tasks_list: list[dict[str, datetime.datetime]] = []
        now = datetime.datetime.now()
        planning_matrix = [
            [datetime.timedelta() for _ in range(machines)]
            for _ in range(details)
        ]
        planning_matrix[0][0] = now + datetime.timedelta(hours=matrix[0][0])
        cls._append_gantt_task(
            tasks_list, 1, int(matrix[0][-2]), now, planning_matrix[0][0]
        )

        for machine_index in range(1, machines):
            time = planning_matrix[0][machine_index - 1] + datetime.timedelta(
                hours=matrix[0][machine_index]
            )
            planning_matrix[0][machine_index] = time
            cls._append_gantt_task(
                tasks_list,
                machine_index + 1,
                int(matrix[0][-2]),
                planning_matrix[0][machine_index - 1],
                time,
            )

        for detail_index in range(1, details):
            time = planning_matrix[detail_index - 1][0] + datetime.timedelta(
                hours=matrix[detail_index][0]
            )
            planning_matrix[detail_index][0] = time
            cls._append_gantt_task(
                tasks_list,
                1,
                int(matrix[detail_index][-2]),
                planning_matrix[detail_index - 1][0],
                time,
            )

        for detail_index in range(1, details):
            for machine_index in range(1, machines):
                start_time = max(
                    planning_matrix[detail_index - 1][machine_index],
                    planning_matrix[detail_index][machine_index - 1],
                )
                finish_time = start_time + datetime.timedelta(
                    hours=matrix[detail_index][machine_index]
                )
                planning_matrix[detail_index][machine_index] = finish_time
                cls._append_gantt_task(
                    tasks_list,
                    machine_index + 1,
                    int(matrix[detail_index][-2]),
                    start_time,
                    finish_time,
                )
        fig = px.timeline(
            tasks_list,
            x_start="Начало",
            x_end="Конец",
            y="Станок",
            color="Деталь",
            color_discrete_sequence=ColorPalette.generate_color_palette(
                details
            ),
        )
        fig.update_yaxes(autorange="reversed", title="")
        fig.update_layout(showlegend=False)
        fig.write_html("gantt.html")

    @classmethod
    def create_bi_diagrams(
        cls,
        planning_matrix: list[list[float | int]],
        machines: int,
        details: int,
    ) -> None:
        diagram_data: dict[str, list[str | float]] = {
            "Станок": [],
            "Простой станка": [],
            "Загруженность станка": [],
        }

        diagram_data["Станок"].append("Станок 1")
        diagram_data["Простой станка"].append(
            planning_matrix[-1][-1] - planning_matrix[-1][0]
        )
        diagram_data["Загруженность станка"].append(planning_matrix[-1][0])
        for machine_index in range(1, machines):
            diagram_data["Станок"].append(f"Станок {machine_index + 1}")
            diagram_data["Загруженность станка"].append(
                planning_matrix[-1][machine_index]
                - planning_matrix[0][machine_index]
            )
            machine_downtime = planning_matrix[0][machine_index - 1] + (
                planning_matrix[-1][-1] - planning_matrix[-1][machine_index]
            )
            for detail_index in range(1, details):
                if (
                    planning_matrix[detail_index][machine_index - 1]
                    > planning_matrix[detail_index - 1][machine_index]
                ):
                    machine_downtime += (
                        planning_matrix[detail_index][machine_index - 1]
                        - planning_matrix[detail_index - 1][machine_index]
                    )
            diagram_data["Простой станка"].append(machine_downtime)
        df = pd.DataFrame(diagram_data)
        fig1 = px.bar(
            df,
            x="Станок",
            y="Простой станка",
            color="Станок",
            color_discrete_sequence=ColorPalette.generate_color_palette(
                machines
            ),
        )
        fig1.update_layout(
            yaxis_title="Простой станков (в часах)", xaxis_title=""
        )
        fig1.write_html("downtime.html")
        fig2 = px.bar(
            df,
            x="Станок",
            y="Загруженность станка",
            color="Станок",
            color_discrete_sequence=ColorPalette.generate_color_palette(
                machines
            ),
        )
        fig2.update_layout(
            yaxis_title="Загруженность станков (в часах)", xaxis_title=""
        )
        fig2.write_html("workload.html")

    @classmethod
    def _append_gantt_task(
        cls,
        tasks_list: list[dict],
        machine_number: int,
        detail_number: int,
        start_time: datetime.timedelta,
        finish_time: datetime.timedelta,
    ) -> None:
        tasks_list.append(
            {
                "Станок": f"Станок {machine_number}",
                "Начало": start_time,
                "Конец": finish_time,
                "Деталь": f"Деталь {detail_number}",
            }
        )
