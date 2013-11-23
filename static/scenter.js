
function convertPolygonForApi(polygon_coords) {
    // Add start point to the polygon to close it
    polygon_coords.push(polygon_coords[0]);
    res = '{ \"type\": \"Polygon\", \"coordinates\": [ [';
    res += polygon_coords;
    res = res + '] ] }';
    return res.replace(/\(/g,'[').replace(/\)/g,']')
}

function populateMessages(fencePolygon){
        $.ajax({
        // TODO: need to use url Django tag?
        url: 'api/scents/' + fencePolygon.id + '/',
        cache: false,
        type: 'GET',
                dataType: "json",
                success: function(data){
                        messagelist = data;

                        $('#messagelist').html("");
                        
                        $.each(messagelist, function(index, message) {
                                appendMessage(messagelist[index].content);
                        });
                },
                error: function(){
                        $('#messagelist').html("Nothing is scenting here.");
                }
        });
}


function postMessage(fencePolygon, text) {
    scent = null;
    var due = new Date();
    due.setDate(due.getDate() + 2);

    $.ajax({
        url: 'api/scents/' + fencePolygon.id + '/',
        cache: false,
        type: 'POST',
        data:  {"author": "Ghost", "type": "1", "title": "Scent title", "content": text,
               "due": due.toISOString(), "fence": fencePolygon.id},
        dataType: "json",
        success: function(data){
            return data.id;
        },
        error: function(){
            alert("FUCK!");
        }
    });
    return -1;
}