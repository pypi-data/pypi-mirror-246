import IPython
import numpy as np
from base64 import b64encode
from io import BytesIO
from matplotlib import pyplot
from typing import Union
from glidergun.core import Grid, Stack

ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(obj: Union[Grid, Stack]):
        with BytesIO() as buffer:
            figure = pyplot.figure(frameon=False)
            axes = figure.add_axes((0, 0, 1, 1))
            axes.axis("off")
            if isinstance(obj, Grid):
                pyplot.imshow(obj.data, cmap=obj._cmap)
                extent = obj.extent
            elif isinstance(obj, Stack):
                pyplot.imshow(
                    np.dstack([obj.grids[i - 1].type("uint8").data for i in obj._rgb])
                )
                extent = obj.grids[0].extent
            pyplot.savefig(buffer)
            pyplot.close(figure)
            description = str(obj).replace("|", "<br />")
            image = b64encode(buffer.getvalue()).decode()
            return f'<div>{description}</div><img src="data:image/png;base64, {image}" /><div>{extent}</div>'

    formatter = ipython.display_formatter.formatters["text/html"]  # type: ignore
    formatter.for_type(Grid, html)
    formatter.for_type(Stack, html)
    formatter.for_type(
        tuple,
        lambda items: f"""
            <table>
                <tr style="text-align: left">
                    {"".join(f"<td>{html(item)}</td>" for item in items)}
                </tr>
            </table>
        """
        if all(isinstance(item, Grid) or isinstance(item, Stack) for item in items)
        else f"{items}",
    )
