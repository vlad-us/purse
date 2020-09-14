//// AJAX экспорта в excel
var exportLink = document.getElementById('exportToExcel');

exportLink.addEventListener('click', function(event) {
    const request = new XMLHttpRequest();
    const url = exportLink.value;
    request.open('GET', url);
    request.addEventListener('readystatechange', () => {
        if (request.readyState == 4 && request.status == 200) {
            response = JSON.parse(request.responseText);
            response = response['details']
            //console.log(response);
            var myJson = JSON.stringify(response);
            //console.log(myJson);
            //
            var downloadLink = document.createElement("a");
            var file = new Blob([myJson], {type: 'application/json'});
            downloadLink.href = URL.createObjectURL(file);
            downloadLink.download = 'example.txt';
            downloadLink.click();
        }
    })
    request.send();
})



//var tableToExcel = (function() {
//          var uri = 'data:application/vnd.ms-excel;base64,'
//            , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
//            , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
//            , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
//          return function(table, name) {
//            if (!table.nodeType) table = document.getElementById(table)
//            var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
//            window.location.href = uri + base64(format(template, ctx))
//          }
//        })()

//var exportLink = document.getElementById('exportToExcel').value;
//const request = new XMLHttpRequest();
//const url = exportLink;
//console.log(url)
//request.open('GET', url);
//request.addEventListener('readystatechange', () => {
//    if (request.readyState == 4 && request.status == 200) {
//    response = JSON.parse(request.responseText);
//    console.log(response['guid']);
//    }
//    request.send();
//    })
//console.log(exportLink);
