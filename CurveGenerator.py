from os.path import join, dirname


class Curve:
    def __init__(self, data,
                 font_color="white",
                 title=None,
                 width_factor =1,
                 x_labels=None,
                 curve_it=0):

        self.data = data
        self.font_color = font_color
        self.title = title
        self.width_factor = width_factor
        self.width = f"(window.innerWidth*{width_factor}).toString() + \"px\""
        self.x_labels = x_labels
        self.curve_it = curve_it
        self.instance_number = 0
        self.colors = ["#c0392b", "#2980b9", "#27ae60"]

    def __str__(self):
        self.instance_number += 1
        out_string = ""

        data_real_dict = {"type": "line",
                          "datasets": [{"data": v, 'label': k, "lineTension": 0,
                                        "xLabels": [x + 1 for x in
                                                    range(len(self.data[[x for x in self.data.keys()][0]]))],
                                        'borderColor': self.colors[i % len(self.colors)]}
                                       for i, (k, v) in enumerate(self.data.items())]}
        if self.x_labels is None:
            data_real_dict["labels"] = [x + 1 for x in range(len(self.data[[x for x in self.data.keys()][0]]))]
        else:
            data_real_dict["labels"] = self.x_labels
        mini, maxi = min([min(v) for k, v in self.data.items()]), max([max(v) for k, v in self.data.items()])
        scales_dict = {"yAxes": [{"display": "true",
                                  "ticks": {"fontColor": self.font_color, "suggestedMin": mini, "suggestedMax": maxi}}],
                       "xAxes": [{"ticks": {"autoSkip": 'false', "fontColor": self.font_color}}]}
        options_dict = {"scales": scales_dict, "legend": {"labels": {"fontColor": self.font_color}}}
        if self.title is not None:
            options_dict["title"] = {"display": "false", "text": self.title, "fontColor": self.font_color}
        options = str(options_dict)
        out_string += "  <canvas id=\"line-chart-%i-%i\"></canvas>\n" % (self.curve_it, self.instance_number)
        ctx = f"document.getElementById(\"line-chart-{self.curve_it}-{self.instance_number}\")"
        out_string += "  <script>\n"
        out_string += f"    {ctx}.parentNode.style.maxWidth = {self.width};\n"
        out_string += "    var myLineChart = new Chart(%s, {type: 'line', data: %s, options: %s});\n" % \
                      (ctx, str(data_real_dict), options)
        out_string += "  </script>\n"

        return out_string


class CurveGenerator:
    def __init__(self):
        self.curve_it = 0
        self.chart_path = join(dirname(__file__), "js/Chart.bundle.min.js")

    def make_header(self):
        with open(self.chart_path, "r") as charjs_file:
            ret_str = "  <script type=\"text/javascript\">\n  " + charjs_file.read().replace("\n", "\n  ")
            ret_str += "Chart.defaults.global.elements.line.fill = false;\n  </script>\n"
            return ret_str

    def make_curve(self, data,
                   font_color="white",
                   title=None,
                   width_factor=1.,
                   x_labels=None):
        self.curve_it += 1
        return Curve(data, font_color, title, width_factor, x_labels, self.curve_it)
