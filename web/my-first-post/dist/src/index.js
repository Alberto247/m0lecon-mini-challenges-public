const path = require('path');
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const app = express();
const port = process.env.PORT || 80;
const useDBG = process.env.DBG || false;

const opt = {
	database: {
		server: "my-first-post-mongo:27017",
		user: "th3pwn3r",
		password: "W2Zyr&Np",
		db: "test"
	}
};

app.use(express.static('__dirname'));
app.use(bodyParser.urlencoded({extended: true}))

mongoose.connect(`mongodb://${opt.database.server}/${opt.database.db}?authSource=${opt.database.db}`, {
	useNewUrlParser: true,
	useUnifiedTopology: true,
	user: opt.database.user,
	pass: opt.database.password
}).then(() => {
	console.log("MongoDB connected!");
}).catch(err => {
	console.log("Failed to connect to MongoDB", err);
});

const postSchema = new mongoose.Schema({
	content: String,
	visible: Boolean
});

const PostModel = mongoose.model('post', postSchema);


app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'static/index.html'));
	return;
});

app.post('/post', (req, res) =>{
	if(!req.body.content) res.send(418);
	var p = new PostModel({content: req.body.content, visible: true});
	//Not right now
	//p.save();
	res.header("Location: /");
	res.send("Your comment has been sent in for verification.");
});

app.get('/post', async (req, res) =>{
	var posts = await PostModel.find({visible: true});
	console.log(JSON.stringify(posts));
	res.send(posts);
	return;
});

app.get('/*', (req,res) => {
	if(useDBG) res.sendFile(path.join(__dirname + req.url));
	return;
});

app.listen(port);
console.log("Listening on port " + port + ".")
