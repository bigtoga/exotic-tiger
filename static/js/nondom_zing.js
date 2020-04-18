d3.csv("static/data/grouped_month_day.csv").then(function (data) {

  //console.log(data[0]);
  data.forEach(function (parse) {
    parse.month_total_crimes = +parse.month_total_crimes;
  });

  //console.log(data[1]);

  var non_domestic_20 = []
  var non_domestic_19 = []
  var non_domestic_18 = []
  var dates = []

  for (var j = 0; j < data.length; j++) {
    dates.push(data[j].month_day)
  }

  let unique = [...new Set(data.map(item => item.month_day))];
  //console.log(unique);

  for (var i = 0; i < data.length; i++) {
    if (data[i].domestic === "False" && data[i].year === '2020') {
      non_domestic_20.push(data[i].month_total_crimes)
    }
    else if (data[i].domestic === "False" && data[i].year === '2019') {
      non_domestic_19.push(data[i].month_total_crimes)
    }
    else if (data[i].domestic === "False" && data[i].year === '2018') {
      non_domestic_18.push(data[i].month_total_crimes)
    }
  }

  //console.log(non_domestic_20)

  // Chart Configuration
  let chartConfig = {
    type: 'area',
    globals: {
      fontFamily: 'Poppins',
      fontColor: '#333'
    },
    title: {
      text: 'Comparison between Non-domestic crimes 2018 - 2020',
      align: 'center',
      padding: '5px'
    },
    subtitle: {
      text:
        '',
      align: 'center',
      fontColor: '#505050',
      padding: '10px'
    },
    legend: {
      align: 'center',
      verticalAlign: 'bottom',
      layout: '3x2',
      border: 'none',
      item: {
        fontSize: '18px'
      },
      marker: {
        type: 'circle'
      }
    },
    tooltip: {
      callout: true,
      text: `%t:<br>%v Incidents reported<br>`,
      backgroundColor: '#F7F9FA',
      fontColor: '#505050',
      fontSize: '18px',
      padding: '20px 35px',
      borderRadius: '4px'
    },
    plot: {
      aspect: 'spline'
    },
    scaleX: {
      values: unique
    },
    scaleY: {
      values: '0:700:1'
    },
    series: [
      {
        values: non_domestic_20,
        text: 'Non-Domestic 2020',
        zIndex: 3,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#354CA1',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: non_domestic_19,
        text: 'Non-Domestic 2019',
        zIndex: 2,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#CC0035',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: non_domestic_18,
        text: 'Non-Domestic 2018',
        zIndex: 1,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#edda4a',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      }
    ]
  };

  // Render Method
  zingchart.render({
    id: 'yourChart',
    data: chartConfig,
    height: '100%',
    width: '100%',
  });
});