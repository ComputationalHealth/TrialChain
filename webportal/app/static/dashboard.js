var socket = io.connect();
socket.on('status', function(msg) {
	$('#geth-status').html("<h4>"+msg.data+"</h4>");
	$('#balance').html("<h4>"+msg.balance+"</h4>");
	$('#cost').html("<h4>"+msg.cost+"</h4>");
});
