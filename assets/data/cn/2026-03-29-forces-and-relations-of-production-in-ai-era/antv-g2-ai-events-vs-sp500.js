chart
  .line()
  .data({
    type: "fetch",
    value: "/data/cn/2026-03-29-forces-and-relations-of-production-in-ai-era/sp500.json",
  })
  .encode("x", (d) => new Date(d.date))
  .encode("y", "sp500")
  .encode("color", () => "标普500")
  .scale("x", {
    type: "time",
  })
  .tooltip({
    title: "date",
    items: [
      {
        name: "标普500",
        channel: "y",
      },
    ],
  })
  .axis("x", {
    title: "日期",
  })
  .axis("y", {
    title: "标普500",
  })
  .slider({
    x: {
      labelFormatter: (d) => d.toLocaleDateString(),
    },
  });

chart
  .point()
  .data({
    type: "fetch",
    value: "/data/cn/2026-03-29-forces-and-relations-of-production-in-ai-era/events.json",
    transform: [
      {
        type: "map",
        callback: (d) => ({ date: d.date, event: d.data.title }),
      },
    ]
  })
  .encode("x", (d) => new Date(d.date))
  .encode("y", () => 0)
  .encode("color", () => "事件")
  .encode("event", "event")
  .tooltip({
    title: "",
    items: [
      {
        name: "事件",
        channel: "event",
      },
    ],
  });

chart
  .legend({
    color: {
      position: "top",
      layout: {
        justifyContent: "center",
      },
      itemMarker: "circle",
    },
  });
