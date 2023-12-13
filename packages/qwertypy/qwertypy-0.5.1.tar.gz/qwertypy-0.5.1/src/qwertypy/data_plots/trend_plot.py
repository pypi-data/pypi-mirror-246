import matplotlib.pyplot as plt

from . import plot_colors as plotColors

def trendPlot(xValues, yValues, xLabel, yLabel, plotTitle, **kwargs):
    midX = min(xValues) + (max(xValues) - min(xValues)) / 2
    midY = max(yValues) / 2

    fix, ax = plt.subplots(figsize=(10, 5))
    ax.bar(xValues, yValues, color = plotColors.YELLOW, width = 0.6)
    
    textColor = "#000000"
    if "trendValues" in kwargs:
        trendValues = kwargs["trendValues"]
        last = trendValues[-1]
        first = trendValues[0]
        if last > first: textColor = plotColors.GREEN
        elif last < first: textColor = plotColors.RED

        ax.plot(xValues, trendValues, c = textColor, lw = 2.5)
    
    ax.set_xlabel(xLabel, fontsize = 14)
    ax.set_ylabel(yLabel, fontsize = 14)
    ax.set_title(plotTitle, fontsize = 18)

    plt.xticks(xValues)

    if "legends" in kwargs:
        legends = kwargs["legends"]
        plt.legend(legends, loc ="upper left")

    if "text" in kwargs:
        text = kwargs["text"]
        textProps = dict(boxstyle='round', facecolor=textColor, alpha=0.25)
        plt.text(
            midX, midY, text, fontsize=14, 
            bbox=textProps, va="center", ha="center"
        )

    if "watermark" in kwargs:
        watermark = kwargs["watermark"]
        plt.text(
        midX, midY / 10, watermark, fontsize=8, 
        bbox=dict(boxstyle="round", facecolor=plotColors.LIGHT_GREY, alpha=0.1),
        va="center", ha="center", color="grey"
    )

    if "saveToFile" in kwargs:
        fileName = kwargs["saveToFile"]
        plt.savefig(fileName, bbox_inches="tight", dpi=150)

    if "showValues" in kwargs:
        showValues = kwargs["showValues"]
        if showValues:
            for bar in ax.patches:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() / 2 + bar.get_y(),
                    round(bar.get_height()), ha = 'center',
                    color = "black", size = 10
                )

    plt.show()