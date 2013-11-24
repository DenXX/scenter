function deleteMessages(mid){
        $.ajax({
        // TODO: need to use url Django tag?
        url: 'api/scent/' + mid + '/',
        cache: false,
        type: 'DELETE',
                dataType: "json",
                success: function(data){
			console.log('deleted');
                },
                error: function(){
			console.log('error delete');
                }
        });
}
