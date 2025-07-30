$("#id_province").change(function () {
      var province = $(this).val();
      $.ajax({
        url: '/ajax/get_towns/',
        data: {
          'province': province
        },
        dataType: 'json',
        success: function (data) {
          console.log(data.towns[1])
          var towns_data = data.towns
          var town_id = data.id
          $("#drop_town option").remove();
          for(var i=0; i< towns_data.length;i++){
            //creates option tag
              jQuery('<option/>', {
                    value: towns_data[i],
                    html: towns_data[i]
                    }).appendTo('#drop_town select'); //appends to select if parent div has id dropdown
           }
        }
      });
});
$("#id_power_limit").change(function () {
        var pwlimit = $(this).val();
        //Better to construct options first and then pass it as a parameter
        var options1 = {
            title: {
                text: "Night Consumer"
            },
            animationEnabled: true,
            exportEnabled: false,
            data: [
            {
                type: "line", //change it to line, area, column, pie, etc
                dataPoints: [
                    { x: 00, y: pwlimit*0.85 },
                    { x: 01, y: pwlimit*0.75 },
                    { x: 02, y: pwlimit*0.7 },
                    { x: 03, y: pwlimit*0.5 },
                    { x: 04, y: pwlimit*0.4 },
                    { x: 05, y: pwlimit*0.35 },
                    { x: 06, y: pwlimit*0.3 },
                    { x: 07, y: pwlimit*0.4 },
                    { x: 08, y: pwlimit*0.35 },
                    { x: 09, y: pwlimit*0.45 },
                    { x: 10, y: pwlimit*0.3 },
                    { x: 11, y: pwlimit*0.2 },
                    { x: 12, y: pwlimit*0.25 },
                    { x: 13, y: pwlimit*0.35 },
                    { x: 14, y: pwlimit*0.2 },
                    { x: 15, y: pwlimit*0.45 },
                    { x: 16, y: pwlimit*0.35 },
                    { x: 17, y: pwlimit*0.65 },
                    { x: 18, y: pwlimit*0.85 },
                    { x: 20, y: pwlimit*0.9 },
                    { x: 21, y: pwlimit*0.75 },
                    { x: 22, y: pwlimit*0.8 },
                    { x: 23, y: pwlimit*0.9 },
                ]
            }
            ]
        };
        var options2 = {
            title: {
                text: "Morning Consumer"
            },
            animationEnabled: true,
            exportEnabled: false,
            data: [
            {
                type: "line", //change it to line, area, column, pie, etc
                dataPoints: [
                    { x: 00, y: pwlimit*0.3 },
                    { x: 01, y: pwlimit*0.3 },
                    { x: 02, y: pwlimit*0.3 },
                    { x: 03, y: pwlimit*0.4 },
                    { x: 04, y: pwlimit*0.4 },
                    { x: 05, y: pwlimit*0.35 },
                    { x: 06, y: pwlimit*0.4 },
                    { x: 07, y: pwlimit*0.55 },
                    { x: 08, y: pwlimit*0.75 },
                    { x: 09, y: pwlimit*0.9 },
                    { x: 10, y: pwlimit*0.85 },
                    { x: 11, y: pwlimit*0.9 },
                    { x: 12, y: pwlimit*0.75 },
                    { x: 13, y: pwlimit*0.8 },
                    { x: 14, y: pwlimit*0.7 },
                    { x: 15, y: pwlimit*0.65 },
                    { x: 16, y: pwlimit*0.5 },
                    { x: 17, y: pwlimit*0.55 },
                    { x: 18, y: pwlimit*0.4 },
                    { x: 19, y: pwlimit*0.45 },
                    { x: 20, y: pwlimit*0.4 },
                    { x: 21, y: pwlimit*0.35 },
                    { x: 22, y: pwlimit*0.3 },
                    { x: 23, y: pwlimit*0.3 }
                ]
            }
            ]
        };
        var options3 = {
            title: {
                text: "Steady Consumer"
            },
            animationEnabled: true,
            exportEnabled: false,
            data: [
            {
                type: "line", //change it to line, area, column, pie, etc
                dataPoints: [
                    { x: 00, y: pwlimit*0.8 },
                    { x: 01, y: pwlimit*0.75 },
                    { x: 02, y: pwlimit*0.9 },
                    { x: 03, y: pwlimit*0.75 },
                    { x: 04, y: pwlimit*0.8 },
                    { x: 05, y: pwlimit*0.75 },
                    { x: 06, y: pwlimit*0.9},
                    { x: 07, y: pwlimit*0.8 },
                    { x: 08, y: pwlimit*0.85 },
                    { x: 09, y: pwlimit*0.9 },
                    { x: 10, y: pwlimit*0.85 },
                    { x: 11, y: pwlimit*0.75 },
                    { x: 12, y: pwlimit*0.8 },
                    { x: 13, y: pwlimit*0.9 },
                    { x: 14, y: pwlimit*0.85 },
                    { x: 15, y: pwlimit*0.75 },
                    { x: 16, y: pwlimit*0.8 },
                    { x: 17, y: pwlimit*0.95 },
                    { x: 18, y: pwlimit*0.85 },
                    { x: 19, y: pwlimit*0.75 },
                    { x: 20, y: pwlimit*0.8 },
                    { x: 21, y: pwlimit*0.85 },
                    { x: 22, y: pwlimit*0.9 },
                    { x: 23, y: pwlimit*0.75 }
                ]
            }
            ]
        };

        $("#chartContainer1").CanvasJSChart(options1);
        $("#chartContainer2").CanvasJSChart(options2);
        $("#chartContainer3").CanvasJSChart(options3);

});
///    province_id = $(this).val();
///    request_url = '/refood_app/get_towns/' + province_id + '/';
///        $.ajax({
///            url: request_url,
///            success: function(data){
///                $.each(data, function(index, text){
///                    $('#town').append(
///                    $('<option></option>').val(index).html(text)
///                    );
///                });
///            };
///        });
///});
