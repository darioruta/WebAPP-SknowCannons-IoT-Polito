function renderHumHist(loc,slope, sec, filter){

  var hum_hist_options = {
    series: [],
  title: {
    text: 'Humidity',
    align: 'center',
  },
    chart: {
    id: 'area-datetime',
    type: 'area',
    height: 300,
    zoom: {
      autoScaleYaxis: true
    }
  },
  noData: {
    text: 'Loading...'
  },
  dataLabels: {
    enabled: false
  },
  markers: {
    size: 0,
    style: 'hollow',
  },
  xaxis: {
    type: 'datetime',
    tickAmount: 6,
  },
  yaxis: {
      title: {
        text: 'Percentage (%)'
      }
  },
  tooltip: {
    x: {
      format: 'dd MMM yyyy hh:mm'
    }
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.7,
      opacityTo: 0.9,
      stops: [0, 100]
    }
  },
  };

  var hum_hist_chart = new ApexCharts(document.querySelector("#graph-hum-landing"), hum_hist_options);
  hum_hist_chart.render();

//POPOLAZIONE DINAMICA SECTION

//PRENDERE Kit_Name.
var uri_f1_hist = "/data_v2/getMeasure?loc="+loc+"&slo="+slope+"&sec="+sec+"&ns="+filter+"&measure=field2";


  $.ajax(
    {
        url: uri_f1_hist, //ID devi metterlo dopo
        method: 'GET',
        contentType: "application/json",
        dataType: "json",
        success: function(risposta){	
      console.log(risposta.data);
        var dati = risposta.data.map(function (data) {
          return {
            x: new Date(data[1]), // converte il timestamp in una data JavaScript
            y: data[0]
          }
        });
        hum_hist_chart.updateSeries([{
          data: dati
        }])
        },
    }
  );

  

}

