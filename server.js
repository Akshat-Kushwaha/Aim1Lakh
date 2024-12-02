const io = require('socket.io')(3000, {
    cors: {
        origin: '*', // Allow all origins (update for security in production)
        methods: ['GET', 'POST']
    }
});

io.on('connection', socket => {
    console.log('New client connected');

    // Listen for offers, answers, and ICE candidates
    socket.on('offer', data => {
        console.log('Offer received');
        socket.broadcast.emit('offer', data); // Broadcast the offer to all other clients
    });

    socket.on('answer', data => {
        console.log('Answer received');
        socket.broadcast.emit('answer', data); // Broadcast the answer to all other clients
    });

    socket.on('candidate', data => {
        console.log('ICE candidate received');
        socket.broadcast.emit('candidate', data); // Broadcast the ICE candidate to all other clients
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});
