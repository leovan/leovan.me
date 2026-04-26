chart.options({
  type: "point",
  autoFit: true,
  data: {
    type: "fetch",
    value: "/data/cn/2026-04-25-how-to-save-token-for-llm/benchmark.json",
  },
  encode: {
    x: "input_price",
    y: "success_rate",
    size: "size",
    color: "region_type",
    shape: "license_type",
    name: "name",
    date: "date",
    output_price: "output_price",
    cache_price: "cache_price",
    license_type: "license_type",
  },
  labels: [
    {
      text: "name",
      position: "left",
      style: {
        dx: (d) => (d.size > 100 ? 25 : 15),
      }
    }
  ],
  scale: {
    x: {
      min: 0,
      max: 5,
      nice: true,
    },
    y: {
      min: 0.6,
      max: 1.0,
      nice: true,
    },
    size: {
      type: "log",
      range: [5, 10],
    },
    shape: {
      range: ["point", "triangle"],
    }
  },
  style: {
    fillOpacity: 0.3,
    lineWidth: 1,
  },
  axis: {
    x: {
      title: "输入价格（美元）",
      tickCount: 6,
    },
    y: {
      title: "成功率（%）",
      labelFormatter: (d) => `${(d * 100).toFixed(0)}%`,
      tickCount: 5,
    },
  },
  tooltip: {
    title: "",
    items: [
      {
        name: "名称",
        channel: "name",
      },
      {
        name: "发布日期",
        channel: "date",
      },
      {
        name: "参数",
        channel: "size",
        valueFormatter: (d) => `${d}B`,
      },
      {
        name: "输入价格",
        channel: "x",
        valueFormatter: (d) => `\$${d}`,
      },
      {
        name: "输出价格",
        channel: "output_price",
        valueFormatter: (d) => `\$${d}`,
      },
      {
        name: "缓存读取价格",
        channel: "cache_price",
        valueFormatter: (d) => `\$${d}`,
      },
      {
        name: "缓存读取价格",
        channel: "cache_price",
        valueFormatter: (d) => `\$${d}`,
      },
      {
        name: "成功率",
        channel: "y",
        valueFormatter: (d) => `${(d * 100).toFixed(0)}%`,
      }
    ],
  },
  legend: {
    size: false,
    color: {
      title: "地域",
      position: "bottom",
      layout: {
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "row",
      }
    },
    shape: {
      title: "许可",
      position: "bottom",
      layout: {
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "row",
      }
    },
  },
});

chart.options({
  type: "view",
  labelTransform: [
    {
      type: "overlapDodgeY",
    },
    {
      type: "exceedAdjust",
      bounds: "main",
      offsetX: 15,
    },
  ],
});
