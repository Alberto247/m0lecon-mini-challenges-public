db.createUser({
  user: 'th3pwn3r',
  pwd: '<REDACTED>',
  roles: [
    {
      role: 'read',
      db: 'test',
    },
  ],
});

db.createCollection('posts', {capped: false});
db.posts.insert([
	{"content": "<REDACTED>", visible: false},
	{"content": "You man you cool post", visible: true},
	{"content": "Very interesting post, thanks for sharing it.", visible: true},
	{"content": "This is garbage mate, just remove it.", visible: true},
]);
