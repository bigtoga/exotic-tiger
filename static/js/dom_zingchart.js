d3.csv("static/data/grouped_month_day.csv").then(function (data) {

  //console.log(data[0]);
  data.forEach(function (parse) {
    parse.month_total_crimes = +parse.month_total_crimes;
  });

  //console.log(data[1]);
  var domestic_20 = []
  var domestic_19 = []
  var domestic_18 = []
  var dates = []

  for (var j = 0; j < data.length; j++) {
    dates.push(data[j].month_day)
  }

  let unique = [...new Set(data.map(item => item.month_day))];
  //console.log(unique);

  for (var i = 0; i < data.length; i++) {
    if (data[i].domestic === "True" && data[i].year === '2020') {
      domestic_20.push(data[i].month_total_crimes)
    }
    else if (data[i].domestic === "True" && data[i].year === '2019') {
      domestic_19.push(data[i].month_total_crimes)
    }
    else if (data[i].domestic === "True" && data[i].year === '2018') {
      domestic_18.push(data[i].month_total_crimes)
    }
  }

  //console.log(domestic_20)

  // Chart Configuration
  let chartConfig = {
    type: 'area',
    globals: {
      fontFamily: 'Poppins',
      fontColor: '#333'
    },
    title: {
      text: 'Comparison between Domestic Crimes 2018 - 2020',
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
      values: '0:200:1'
    },
    series: [
      {
        values: domestic_20,
        text: 'Domestic 2020',
        zIndex: 6,
        alphaArea: 1,
        lineColor: '#ffffff',
        lineWidth: '1.5px',
        backgroundColor: '#6ba1ff',
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
        values: domestic_19,
        text: 'Domestic 2019',
        zIndex: 5,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#ff6b6e',
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
        values: domestic_18,
        text: 'Domestic 2018',
        zIndex: 4,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#fff49e',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
    ]
  }

  // Render Method
  zingchart.render({
    id: 'myChart',
    data: chartConfig,
    height: '100%',
    width: '100%',

  });
});
